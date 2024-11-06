# Plot the image and face locations
import os
import random
import numpy as np
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import face_recognition

knowns_dir = "known"
knowns = os.listdir(knowns_dir)


def get_random_image_path_whole(source_dir):
    selected_image = random.sample(os.listdir(source_dir), 1)[0]
    selected_image_path = os.path.join(source_dir, selected_image)
    return selected_image_path


def get_random_image_path(imgpath):
    person_folders = ["10", "20", "30", "40", "50", "unknown"]
    random_folder = random.choice(person_folders)
    folder_path = os.path.join(imgpath, random_folder)
    images = os.listdir(folder_path)
    random_image = random.choice(images)
    return os.path.join(folder_path, random_image)


def plot_faces(image, face_locations):
    fig, ax = plt.subplots(1)
    ax.imshow(image)
    for top, right, bottom, left in face_locations:
        rect = patches.Rectangle(
            (left, top),
            right - left,
            bottom - top,
            linewidth=2,
            edgecolor="r",
            facecolor="none",
        )
        ax.add_patch(rect)
    plt.show()


def get_knowns_encondings():
    known_images = [f"known/{i}" for i in knowns]
    known_encodings = []
    for known_image_path in known_images:
        known_image = face_recognition.load_image_file(known_image_path)
        encoding = face_recognition.face_encodings(known_image)
        if encoding:  # Check if at least one face encoding is found
            known_encodings.append(encoding[0])
    return known_encodings


def get_knowns_encodings_multi():
    known_encodings = []
    known_names = []

    # 假設每個人有一個文件夾，文件夾名稱即人名
    base_dir = "known-multiple"
    for person_name in os.listdir(base_dir):
        person_dir = os.path.join(base_dir, person_name)

        # 確保是目錄
        if os.path.isdir(person_dir):
            for filename in os.listdir(person_dir):
                image_path = os.path.join(person_dir, filename)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    known_encodings.append(encodings[0])  # 每張圖片的第一個人臉編碼
                    known_names.append(person_name)  # 使用文件夾名稱作為人名
                    print(f"Loaded encoding for {person_name} from {filename}")

    return known_encodings, known_names


def who(image_path):
    known_encodings = get_knowns_encondings()
    unknown_image = face_recognition.load_image_file(image_path)

    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if unknown_encoding:
        unknown_encoding = unknown_encoding[0]
    else:
        return "unknown"
    # unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces(known_encodings, unknown_encoding)
    print("results", results)
    who = [e for e, if_true in zip(knowns, results) if if_true]
    if who:
        who = who[0].split(".")[0]
    else:
        who = "unknown"
    return who


def who2(image_path):
    known_encodings, known_names = get_knowns_encodings_multi()
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if unknown_encoding:
        unknown_encoding = unknown_encoding[0]
    else:
        return "unknown"
    threshold = 0.4  # 使用更嚴格的閾值
    distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    best_match_index = np.argmin(distances)  # 找出距離最近的已知編碼
    name = "Unknown"
    if distances[best_match_index] < threshold:
        name = known_names[best_match_index]
    return name


if __name__ == "__main__":
    home = os.path.expanduser("~")
    projdir = (
        f"{home}/.cache/kagglehub/datasets/jessicali9530/celeba-dataset/versions/2"
    )
    source_dir = f"{projdir}/img_align_celeba/img_align_celeba"
    imgpath = f"{home}/.cache/kagglehub/datasets/jessicali9530/celeba-dataset/versions/2/img_align_celeba/img_align_celeba_partial"
    random_image_path = get_random_image_path_whole(source_dir)
    image = face_recognition.load_image_file(random_image_path)
    face_locations = face_recognition.face_locations(image)
    known_image = face_recognition.load_image_file("known/biden.png")
    known_encodings = get_knowns_encondings()
    unknown_image = face_recognition.load_image_file("unknown/biden-01.png")
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces(known_encodings, unknown_encoding)
    print("results", results)
