import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_KEY = os.path.join(BASE_DIR, "serviceAccountKey.json")

if not firebase_admin._apps:

    cred = credentials.Certificate(SERVICE_KEY)

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://ai-traffic-signal-default-rtdb.firebaseio.com"
        }
    )

def update_firebase(vehicle_counts, green_signal):

    data = {
        "RoadA": vehicle_counts.get("RoadA", 0),
        "RoadB": vehicle_counts.get("RoadB", 0),
        "RoadC": vehicle_counts.get("RoadC", 0),
        "RoadD": vehicle_counts.get("RoadD", 0),
        "GreenSignal": green_signal
    }

    db.reference("Traffic").set(data)

    print("✅ Firebase Updated Successfully")