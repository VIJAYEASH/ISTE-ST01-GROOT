import cv2
import json
import numpy as np
from ultralytics import YOLO
from config import MODEL_PATH, VIDEOS

print("Loading YOLO...")
model = YOLO(MODEL_PATH)
print("YOLO Loaded Successfully!")

# Load ROI
with open("roi.json", "r") as f:
    roi_data = json.load(f)

caps = {}

for road, path in VIDEOS.items():
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print(f"Cannot Open {road}")
        exit()

    caps[road] = cap

print("All Videos Ready!")

while True:

    frames = []

    for road, cap in caps.items():

        ret, frame = cap.read()

        if not ret:
            exit()

        frame = cv2.resize(frame, (640, 360))

        # Scale ROI from 1280x720 to 640x360
        pts = []

        for x, y in roi_data[road]:
            pts.append((int(x / 2), int(y / 2)))

        pts = np.array(pts, np.int32)

        # Draw Polygon
        cv2.polylines(frame, [pts], True, (0, 255, 255), 3)

        # Road Name
        cv2.putText(
            frame,
            road,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
           

        frames.append(frame)

    top = np.hstack((frames[0], frames[1]))
    bottom = np.hstack((frames[2], frames[3]))

    final = np.vstack((top, bottom))

    cv2.imshow("ROI Preview", final)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

for cap in caps.values():
    cap.release()

cv2.destroyAllWindows()
}