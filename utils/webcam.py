from logging import log
from os import path, mkdir
from datatime import datetime as dt
import cv2

def detect_bodies(frame):
    face_detection_cascade = cv2.CascadeClassifier( cv2.data.haarcascades + "haarcascade_frontalface_default.xml" )
    body_detection_cascade = cv2.CascadeClassifier( cv2.data.haarcascades + "haarcascade_fullbody.xml" )
    gray_color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection_cascade.detectMultiScale(gray_color, 1.3, 5)
    bodies = body_detection_cascade.detectMultiScale(gray_color, 1.3, 5)
    objects = len(faces) + len(bodies)

    return objects

def object_detection(detector):
    recording_buffer_in_seconds = 5
    object_detected = False
    object_detection_timer = None
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    if(detector.isOpened()):
        frame_size = ( int(detector.get(3)), int(detector.get(4)) )
        read, frame = detector.read()
        while read:
            cv2.waitKey(20)
    else:
        log("Error initializing object detection due to unknown or missing detector.", "Critical", "Error", "logs")

    return

def load_camera(port):
    try:
        video_capture = cv2.VideoCapture(port)
    except:
        _log = log("Error loading video capture.", "Critical", "Error", "logs")
        return None
    return video_capture

def webcamera(packet):
    video_capture = load_camera(0)
    if(video_capture is not None):
        print("Loading video capture")
    else:
        print("No video capture found.")
    object_detected = False
    object_detection_stopped_time = None
    timer_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 5
    frame_size = (int(video_capture.get(3)), int(video_capture.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    if video_capture.isOpened():
        read, frame = video_capture.read()
    else:
        read = False
    while read:
        cv2.waitKey(20)
        objects = detect_bodies(frame)
        if objects > 0:
            if object_detected:
                timer_started = True
            else:
                object_detected = True
                today = dt.now().strftime('%Y-%m-%d')
                time = dt.now().strftime('%H-%M-%S')
                video_file_name = f"{len(objects)}_detected_{time}"
                if not path.isdir(f"./test_videos/{today}"):
                    mkdir(f"./test_videos/{today}")
                video_output = cv2.VideoWriter(f"./test_videos/{today}/{video_file_name}.mp4", fourcc, 20, frame_size)
        elif object_detected:
            if timer_started:
                if time.time() - object_detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    object_detected = False
                    timer_started = False
                    video_output.release()
                    print("Video recording stopped...")
            else:
                timer_started = True
                object_detection_stopped_time = time.time()
        if object_detected:
            video_output.write(frame)
        encoding_parameters = [ int(cv2.IMWRITE_JPEG_QUALITY), 65 ]
        packet[0] = cv2.imencode('.jpg', frame, encoding_parameters)[1]
