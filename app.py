import logging
import pickle
import os
import numpy as np
import sys
from sklearn.calibration import CalibratedClassifierCV
from sklearn.decomposition import PCA
from sklearn import svm #pip3 install scikit-learn
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import face_recognition

logging.basicConfig(
    level=logging.INFO,
    #format='%(asctime)s - %(levelname)s - %(message)s',
    format='%(message)s',
    handlers=[
        logging.FileHandler("app.log", mode='w'),
        logging.StreamHandler(sys.stdout)  # 將日誌輸出到控制台
    ]
)

print = logging.info

knowns_dir = "example-known"
knowns_multi_dir = "example-known-multiple"

#def get_knowns_encondings(knowns_dir="known"):
def get_knowns_encondings(knowns_dir = "example-known"):
    known_images = [f"{knowns_dir}/{i}" for i in os.listdir(knowns_dir)]
    #print("known_images", known_images)
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
                if '.DS_Store' in filename :
                    continue
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


def who2_multiple(image_path):
    if os.path.exists("encodings.pkl"):
        known_encodings, known_names = load_encodings_from_file()
    else:
        known_encodings, known_names = get_knowns_encodings_multi()
        save_encodings_to_file(known_encodings, known_names, filename="encodings.pkl")
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)

    threshold = 0.5
    name = ""
    print(f"There are {len(unknown_encoding)} people in this photo .")
    for i in range(len(unknown_encoding)):
        name += f"[{i+1}]"
        distances = face_recognition.face_distance(known_encodings, unknown_encoding[i])
        best_match_index = np.argmin(distances)

        if distances[best_match_index] < threshold:
            name += known_names[best_match_index] +" "
        else:
            name += "Unknown "
    return name




def who3(image_path):
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
    
    clf = svm.SVC(gamma='scale')
    clf.fit(known_encodings,known_names)
    name = clf.predict([unknown_encoding])

    return name[0]


def who3_multiple(image_path):
    if os.path.exists("encodings.pkl"):
        known_encodings, known_names = load_encodings_from_file()
    else:
        known_encodings, known_names = get_knowns_encodings_multi()
        save_encodings_to_file(known_encodings, known_names, filename="encodings.pkl")
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    name=""
    if unknown_encoding:
        # Create and train the SVC classifier
        clf = svm.SVC(gamma='scale')
        clf.fit(known_encodings,known_names)
        
        for i in range(len(unknown_encoding)):
            result = clf.predict([unknown_encoding[i]])
            name += f"[{i+1}]"
            name += result[0]+" "
        return name
    else:
        return "unknown"




def who3_threshold(image_path):
    if os.path.exists("encodings.pkl"):
        known_encodings, known_names = load_encodings_from_file()
    else:
        known_encodings, known_names = get_knowns_encodings_multi()
        save_encodings_to_file(known_encodings, known_names, filename="encodings.pkl")
    unknown_image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(unknown_image)
    unknown_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    if unknown_encodings:
        #unknown_encoding = unknown_encoding[0]
        pass
    else:
        return "unknown"
    
    threshold = 0.1 #
    find_face = []

    # Set up PCA for dimensionality reduction, reducing to 150 components
    #n_components = 150
    #pca = PCA(n_components=n_components, whiten=True, random_state=42)
    svc = svm.SVC(gamma='scale', class_weight='balanced', probability=True)
    #calibrated_svc = CalibratedClassifierCV(base_estimator=svc, method='sigmoid')
    #clf = svm.SVC(gamma='scale', probability=True)
    
    # Create a pipeline that first applies PCA, then SVM
    #clf = make_pipeline(StandardScaler(), pca, calibrated_svc)
    #clf = make_pipeline(StandardScaler(), calibrated_svc)
    clf = make_pipeline(StandardScaler(), svc)
    
    clf.fit(known_encodings,known_names)
    for unknown_enc in unknown_encodings:
        probas = clf.predict_proba([unknown_enc])[0]
        max_proba = np.max(probas)
        max_index = np.argmax(probas)
    
        #print(f"known_names = {known_names}")
        #print(f"clf.classes_ = {clf.classes_}")
        #print(f"max_index = {max_index}")
        #print(f"porbas = {probas}")
        #print(f"max_proba = {max_proba}")
    
        if max_proba < threshold:
            find_face.append("unknown")
        else:
            find_face.append(clf.classes_[max_index])
        
    return find_face

def save_encodings_to_file(encodings, names, filename="encodings.pkl"):
    with open(filename, "wb") as f:
        pickle.dump((encodings, names), f)


def load_encodings_from_file(filename="encodings.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return None, None


if __name__ == "__main__":
    print("knowns_dir %s"% knowns_dir)
    print("knowns_multi_dir %s"% knowns_multi_dir)
    while True:
        unknown_image_file = input("Please enter image path:")
        if unknown_image_file == "":
            break
        #whoami = who(unknown_image_file)
        whoami2 = who2(unknown_image_file)
        whoami2_m = who2_multiple(unknown_image_file)
        whoami3 = who3(unknown_image_file)
        whoami3_m = who3_multiple(unknown_image_file)
        whoami3th = who3_threshold(unknown_image_file)
        print(unknown_image_file)
        #print(f"[method1] This is {whoami}")
        print(f"[method2] This is {whoami2}")
        print(f"[method2_m] They are {whoami2_m}")
        print(f"[method3] This is {whoami3}")
        print(f"[method3_m] This is {whoami3_m}")
        print(f"[method3_th] This is {whoami3th}")
