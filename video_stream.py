from flask import Flask, Response
import cv2

app = Flask(__name__)

print("VIDEO STREAM STARTED")

camera = cv2.VideoCapture("videos/RoadA_H264.mp4")

@app.route("/")
def home():
    return "Server Running"

@app.route("/video_feed")
def video_feed():

    def generate():

        while True:

            success, frame = camera.read()

            if not success:
                camera.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            ret, buffer = cv2.imencode(".jpg", frame)

            if not ret:
                continue

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                buffer.tobytes() +
                b'\r\n'
            )

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)