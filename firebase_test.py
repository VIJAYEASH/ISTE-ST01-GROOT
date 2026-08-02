from firebase_manager import update_firebase

vehicle_counts = {
    "RoadA": 5,
    "RoadB": 8,
    "RoadC": 2,
    "RoadD": 4
}

green_signal = "RoadB"

update_firebase(vehicle_counts, green_signal)