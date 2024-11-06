# Plot the image and face locations
import os
import random
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

    # plot_faces(image, face_locations)

    known_image = face_recognition.load_image_file("known/biden.png")

    # biden_encoding = face_recognition.face_encodings(known_image)[0]

    # knowns = [f"known/{i}" for i in knowns]
    # known_encodings = []
    # for known_image_path in knowns:
    #     known_image = face_recognition.load_image_file(known_image_path)
    #     encoding = face_recognition.face_encodings(known_image)
    #     if encoding:  # Check if at least one face encoding is found
    #         known_encodings.append(encoding[0])

    known_encodings = get_knowns_encondings()

    unknown_image = face_recognition.load_image_file("unknown/biden-01.png")
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces(known_encodings, unknown_encoding)
    # results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    #
    print("results", results)
