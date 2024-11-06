# Plot the image and face locations
import os
import random
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import face_recognition


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


if __name__ == "__main__":
    home = os.path.expanduser("~")
    projdir = (
        f"{home}/.cache/kagglehub/datasets/jessicali9530/celeba-dataset/versions/2"
    )
    source_dir = f"{projdir}/img_align_celeba/img_align_celeba"
    imgpath = f"{home}/.cache/kagglehub/datasets/jessicali9530/celeba-dataset/versions/2/img_align_celeba/img_align_celeba_partial"
    #
    random_image_path = get_random_image_path_whole(source_dir)
    image = face_recognition.load_image_file(random_image_path)
    face_locations = face_recognition.face_locations(image)

    plot_faces(image, face_locations)
