import cv2
import json
import time
import numpy as np
from ultralytics import YOLO

from config import (
    MODEL_PATH,
    VIDEOS,
    VEHICLE_CLASSES,
    COLORS
)

from firebase_manager import update_firebase

# -----------------------------
# LOAD MODEL
# -----------------------------
model = YOLO(MODEL_PATH)

# -----------------------------
# LOAD ROI
# -----------------------------
with open("roi.json", "r") as f:
    roi_data = json.load(f)

# -----------------------------
# OPEN VIDEOS
# -----------------------------
caps = {}

for road, path in VIDEOS.items():

    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        raise Exception(f"Cannot open {path}")

    caps[road] = cap

# -----------------------------
# FIREBASE TIMER
# -----------------------------
last_update = time.time()

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    frames = []

    counts = {}

    for road, cap in caps.items():

        ret, frame = cap.read()

        if not ret:

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            ret, frame = cap.read()

        if not ret:
            continue

        frame = cv2.resize(
            frame,
            (640,360)
        )

        mask = np.zeros(
            frame.shape[:2],
            dtype=np.uint8
        )

        pts = np.array(
            [[
                (int(x/2), int(y/2))
                for x, y in roi_data[road]
            ]],
            dtype=np.int32
        )

        cv2.fillPoly(
            mask,
            pts,
            255
        )

        roi = cv2.bitwise_and(
            frame,
            frame,
            mask=mask
        )

        results = model(
            roi,
            verbose=False
        )

        vehicle_count = 0

        for r in results:

            for box in r.boxes:

                cls = int(box.cls[0])

                name = model.names[cls]

                if name not in VEHICLE_CLASSES:
                    continue

                vehicle_count += 1

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                color = COLORS.get(
                    name,
                    (0,255,0)
                )

                cv2.rectangle(
                    roi,
                    (x1,y1),
                    (x2,y2),
                    color,
                    2
                )

                cv2.putText(
                    roi,
                    name,
                    (x1, max(20, y1-5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )
                counts[road] = vehicle_count

        cv2.putText(
            roi,
            f"{road} : {vehicle_count}",
            (15,30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,255),
            2
        )

        cv2.polylines(
            roi,
            pts,
            True,
            (0,255,255),
            2
        )

        frames.append(roi)

    if len(frames) != 4:
        continue

    green_signal = max(
        counts,
        key=counts.get
    )

    if time.time() - last_update >= 1:

        update_firebase(
            counts,
            green_signal
        )

        last_update = time.time()

    top = np.hstack(
        (
            frames[0],
            frames[1]
        )
    )

    bottom = np.hstack(
        (
            frames[2],
            frames[3]
        )
    )

    final = np.vstack(
        (
            top,
            bottom
        )
    )

    cv2.putText(
        final,
        f"GREEN SIGNAL : {green_signal}",
        (20,35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        3
    )

    cv2.imshow(
        "AI Smart Traffic System",
        final
    )

    key = cv2.waitKey(1)

    if key == ord("q"):
        break
    # -----------------------------
# RELEASE RESOURCES
# -----------------------------

for cap in caps.values():
    cap.release()

cv2.destroyAllWindows()

print("\n================================")
print(" AI Smart Traffic System Closed ")
print("================================")