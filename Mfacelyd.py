import cv2
import multiprocessing
from Mwelcome import welcome_message

# Shared variable to signal eyes detections
eyes_detected = multiprocessing.Value('b', False)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

def face_detection(eyes_detected):
    while True:
        ret, frame = cap.read()

        # ... (rest of your face detection code)

        for (ex, ey, ew, eh) in eyes:
            # ... (rest of your eye detection code)

            eyes_detected.value = True

        # ... (rest of your code)

if __name__ == "__main__":
    face_process = multiprocessing.Process(target=face_detection, args=(eyes_detected,))
    face_process.start()

    face_process.join()
