import cv2
import json
import numpy as np

# =====================================
# CHANGE THESE FOR EACH ROAD
# =====================================
ROAD_NAME = "RoadD"
VIDEO_PATH = "videos/RoadD_H264.mp4"
# =====================================

points = []

cap = cv2.VideoCapture(VIDEO_PATH)

ret, frame = cap.read()

if not ret:
    print("Cannot open video!")
    exit()

frame = cv2.resize(frame, (1280, 720))
original = frame.copy()


def mouse(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))


cv2.namedWindow("ROI Selector")
cv2.setMouseCallback("ROI Selector", mouse)

while True:

    display = original.copy()

    # Draw points
    for p in points:
        cv2.circle(display, p, 5, (0, 255, 0), -1)

    # Draw polygon
    if len(points) >= 2:
        pts = np.array(points, np.int32)
        cv2.polylines(display, [pts], True, (0, 255, 255), 2)

    cv2.putText(display,
                "Left Click : Add Point",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2)

    cv2.putText(display,
                "S : Save ROI",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2)

    cv2.putText(display,
                "R : Reset",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2)

    cv2.putText(display,
                "ESC : Exit",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2)

    cv2.imshow("ROI Selector", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        points.clear()

    elif key == ord("s"):

        try:
            with open("roi.json", "r") as f:
                data = json.load(f)
        except:
            data = {}

        data[ROAD_NAME] = points

        with open("roi.json", "w") as f:
            json.dump(data, f, indent=4)

        print("ROI Saved Successfully!")

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()