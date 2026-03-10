import cv2
import os
import csv
import time
from datetime import datetime

def start_recognition():

    if not os.path.exists("trainer.yml"):
        return "Model not trained!"

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    labels = {}
    with open("labels.txt", "r") as f:
        for line in f:
            id_, name = line.strip().split(",")
            labels[int(id_)] = name

    cap = cv2.VideoCapture(0)

    start_time = None
    current_name = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            face_roi = gray[y:y+h, x:x+w]
            id_, confidence = recognizer.predict(face_roi)

            if confidence < 70:

                name = labels[id_]

                if current_name != name:
                    current_name = name
                    start_time = time.time()

                elif time.time() - start_time >= 3:

                    student_name, roll = name.split(".")
                    file_exists = os.path.isfile("attendance.csv")

                    today = datetime.now().strftime("%Y-%m-%d")
                    current_time = datetime.now().strftime("%H:%M:%S")

                    if file_exists:
                        with open("attendance.csv", "r") as f:
                            reader = csv.reader(f)
                            for row in reader:
                                if len(row) > 2 and row[0] == student_name and row[2] == today:
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return "Attendance Already Marked"

                    with open("attendance.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        if not file_exists:
                            writer.writerow(["Name", "Roll", "Date", "Time"])

                        writer.writerow([student_name, roll, today, current_time])

                    cap.release()
                    cv2.destroyAllWindows()
                    return "Attendance Successfully Marked"

            else:
                current_name = None
                start_time = None

        cv2.imshow("Attendance Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "No Face Detected"