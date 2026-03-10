import cv2
import os

def register_face(name, roll):

    dataset_path = "data_set"
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    folder_name = f"{name}.{roll}"
    student_folder = os.path.join(dataset_path, folder_name)

    if not os.path.exists(student_folder):
        os.makedirs(student_folder)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(f"{student_folder}/{count}.jpg", face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.imshow("Register Face", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 10:
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Registration Successful!"