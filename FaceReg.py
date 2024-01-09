import cv2

cap = cv2.VideoCapture(0)

#if not cap.isOpened():
  #  print("Error: Could not open camera.")
   # exit()

cap.set(3, 640)
cap.set(4, 480)
face_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_eye.xml')
side_face_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_profileface.xml')

while True:
    ret, frame = cap.read()

    #if not ret:
       # print("Error: Failed to capture frame.")
       # break

    mirrored_frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mirrored_gray = cv2.cvtColor(mirrored_frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    side_faces = side_face_cascade.detectMultiScale(gray, 1.3, 5)

    mirrored_side_faces = side_face_cascade.detectMultiScale(mirrored_gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 8)
        
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

    for (x, y, w, h) in side_faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)

    for (x, y, w, h) in mirrored_side_faces:
        x = frame.shape[1] - x - w
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
    
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
for i in range(5):
    cv2.waitKey(1)

