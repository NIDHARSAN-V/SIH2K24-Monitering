from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS
import cv2
import dlib
import numpy as np
import base64
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Allow requests from React app
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")

# Eye landmarks indices (from dlib's 68-point landmarks)
LEFT_EYE_IDX = list(range(36, 42))
RIGHT_EYE_IDX = list(range(42, 48))

# Constants
EAR_THRESHOLD = 0.25  # Adjust this threshold as needed
CLOSE_DURATION = 2.0  # Duration for which the eye should be closed (in seconds)
FACE_LOST_DURATION = 2.0  # Duration for which face should not be detected (in seconds)

# Initialize global variables
left_eye_closed_time = 0
right_eye_closed_time = 0
last_face_detected_time = 0

def get_eye_region(landmarks, eye_indices):
    points = [landmarks.part(i) for i in eye_indices]
    return np.array([[p.x, p.y] for p in points], dtype=np.int32)

def get_pupil_center(eye_frame):
    gray_eye = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    gray_eye = cv2.GaussianBlur(gray_eye, (7, 7), 0)
    _, thresh = cv2.threshold(gray_eye, 30, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        max_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(max_contour)
        return int(x), int(y), int(radius)
    return None

def detect_pupil_direction(pupil_center, eye_frame_width, eye_frame_height):
    eye_center_x = eye_frame_width // 2
    eye_center_y = eye_frame_height // 2
    
    horizontal_direction = ""
    vertical_direction = ""

    if pupil_center[0] < eye_center_x - 10:
        horizontal_direction = "Right"
    elif pupil_center[0] > eye_center_x + 10:
        horizontal_direction = "Left"
    
    if pupil_center[1] < eye_center_y - 5:
        vertical_direction = "up"
    elif pupil_center[1] > eye_center_y + 3:
        vertical_direction = "down"
    
    if horizontal_direction or vertical_direction:
        return f"{horizontal_direction} {vertical_direction}".strip()
    return None

def eye_aspect_ratio(eye_points):
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    C = np.linalg.norm(eye_points[0] - eye_points[3])
    return (A + B) / (2.0 * C)

def process_frame(frame):
    global left_eye_closed_time, right_eye_closed_time, last_face_detected_time

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    current_time = time.time()

    if len(faces) > 0:
        last_face_detected_time = current_time

        for face in faces:
            landmarks = predictor(gray, face)
            (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Keep In Rectangle", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            left_eye_region = get_eye_region(landmarks, LEFT_EYE_IDX)
            right_eye_region = get_eye_region(landmarks, RIGHT_EYE_IDX)

            left_eye_frame = frame[left_eye_region[:, 1].min():left_eye_region[:, 1].max(),
                                   left_eye_region[:, 0].min():left_eye_region[:, 0].max()]
            right_eye_frame = frame[right_eye_region[:, 1].min():right_eye_region[:, 1].max(),
                                    right_eye_region[:, 0].min():right_eye_region[:, 0].max()]

            left_ear = eye_aspect_ratio(left_eye_region)
            right_ear = eye_aspect_ratio(right_eye_region)

            if left_ear < EAR_THRESHOLD:
                if left_eye_closed_time == 0:
                    left_eye_closed_time = current_time
                elif (current_time - left_eye_closed_time) > CLOSE_DURATION:
                    cv2.putText(frame, " Eye Closed for > 2s", (x, y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                left_eye_closed_time = 0

            if right_ear < EAR_THRESHOLD:
                if right_eye_closed_time == 0:
                    right_eye_closed_time = current_time
                elif (current_time - right_eye_closed_time) > CLOSE_DURATION:
                    cv2.putText(frame, "Eye Closed for > 2s", (x, y - 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                right_eye_closed_time = 0

            left_pupil = get_pupil_center(left_eye_frame)
            right_pupil = get_pupil_center(right_eye_frame)

            if left_pupil is not None:
                direction = detect_pupil_direction(left_pupil, left_eye_frame.shape[1], left_eye_frame.shape[0])
                if direction:
                    print(f" moving {direction}")
                cv2.circle(left_eye_frame, (left_pupil[0], left_pupil[1]), left_pupil[2], (0, 255, 0), 2)

            if right_pupil is not None:
                direction = detect_pupil_direction(right_pupil, right_eye_frame.shape[1], right_eye_frame.shape[0])
                if direction:
                    print(f" moving {direction}")
                cv2.circle(right_eye_frame, (right_pupil[0], right_pupil[1]), right_pupil[2], (0, 255, 0), 2)

    else:
        if (current_time - last_face_detected_time) > FACE_LOST_DURATION:
            cv2.putText(frame, "Face not detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    frame = cv2.resize(frame, (640, 480))
    return frame

@app.route('/')
def index():
    return render_template('face.html')

@socketio.on('frame')
def video_feed(image_data):
    img_data = base64.b64decode(image_data.split(',')[1])
    img_array = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    processed_frame = process_frame(frame)

    _, buffer = cv2.imencode('.jpg', processed_frame)
    processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

    emit('processed_frame', {'image': f'data:image/jpeg;base64,{processed_image_base64}'})

if __name__ == '__main__':
    app.run(debug=True)
