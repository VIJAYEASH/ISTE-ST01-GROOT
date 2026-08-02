MODEL_PATH = "models/yolov8n.pt"

VIDEOS = {
    "RoadA": "videos/RoadA_H264.mp4",
    "RoadB": "videos/RoadB_H264.mp4",
    "RoadC": "videos/RoadC_H264.mp4",
    "RoadD": "videos/RoadD_H264.mp4"
}

VEHICLE_CLASSES = [
    "car",
    "motorcycle",
    "bus",
    "truck"
]

COLORS = {
    "car": (255,255,255),
    "motorcycle": (0,255,255),
    "bus": (255,0,0),
    "truck": (255,0,255)
}