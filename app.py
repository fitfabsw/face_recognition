import pickle
import os
import numpy as np
import face_recognition

knowns_dir = "example-known"
knowns_multi_dir = "example-known-multiple"


def get_knowns_encondings(knowns_dir="known"):
    known_images = [f"known/{i}" for i in os.listdir(knowns_dir)]
    # print("known_images", known_images)
    known_encodings = []
    for known_image_path in known_images:
        known_image = face_recognition.load_image_file(known_image_path)
        encoding = face_recognition.face_encodings(known_image)
        if encoding:  # Check if at least one face encoding is found
            known_encodings.append(encoding[0])
    return known_encodings


def get_knowns_encodings_multi(knowns_multi_dir="example-known-multiple"):
    known_encodings = []
    known_names = []
    # 假設每個人有一個文件夾，文件夾名稱即人名
    for person_name in os.listdir(knowns_multi_dir):
        person_dir = os.path.join(knowns_multi_dir, person_name)
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
    knowns = os.listdir(knowns_dir)
    known_encodings = get_knowns_encondings()
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if unknown_encoding:
        unknown_encoding = unknown_encoding[0]
    else:
        return "unknown"
    results = face_recognition.compare_faces(known_encodings, unknown_encoding)
    who = [e for e, if_true in zip(knowns, results) if if_true]
    if who:
        who = who[0].split(".")[0]
    else:
        who = "unknown"
    return who


def who2(image_path):
    if os.path.exists("encodings.pkl"):
        known_encodings, known_names = load_encodings_from_file()
    else:
        known_encodings, known_names = get_knowns_encodings_multi()
        save_encodings_to_file(known_encodings, known_names, filename="encodings.pkl")
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if unknown_encoding:
        unknown_encoding = unknown_encoding[0]
    else:
        return "unknown"
    # threshold = 0.4  # 使用更嚴格的閾值
    threshold = 0.5
    distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    best_match_index = np.argmin(distances)  # 找出距離最近的已知編碼
    name = "Unknown"
    if distances[best_match_index] < threshold:
        name = known_names[best_match_index]
    return name


def save_encodings_to_file(encodings, names, filename="encodings.pkl"):
    with open(filename, "wb") as f:
        pickle.dump((encodings, names), f)


def load_encodings_from_file(filename="encodings.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return None, None


if __name__ == "__main__":
    print("knowns_dir", knowns_dir)
    print("knowns_multi_dir", knowns_multi_dir)
    while True:
        unknown_image_file = input("Please enter image path:")
        if unknown_image_file == "":
            break
        whoami = who(unknown_image_file)
        whoami2 = who2(unknown_image_file)
        print(f"[method1] This is {whoami}")
        print(f"[method2] This is {whoami2}")
