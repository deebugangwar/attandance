import cv2
import os
import numpy as np

def train_model():

    dataset_path = "data_set"
    faces = []
    labels = []
    label_dict = {}
    current_id = 0

    for folder in os.listdir(dataset_path):

        path = os.path.join(dataset_path, folder)

        if not os.path.isdir(path):
            continue

        label_dict[current_id] = folder

        for img in os.listdir(path):

            img_path = os.path.join(path, img)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if image is None:
                continue

            faces.append(image)
            labels.append(current_id)

        current_id += 1

    if len(faces) == 0:
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    recognizer.save("trainer.yml")

    with open("labels.txt", "w") as f:
        for id_, name in label_dict.items():
            f.write(f"{id_},{name}\n")