import cv2
import time
import numpy as np
import face_recognition
import os
import pickle
from who_lib import save_encodings_to_file, load_encodings_from_file, get_knowns_encodings_multi

knowns_dir = "known"
knowns = os.listdir(knowns_dir)

def main():
    # known_encodings = load_encodings_from_file()
    t0 = time.time()
    if os.path.exists("encodings.pkl"):
        known_encodings, known_names = load_encodings_from_file()
    else:
        known_encodings, known_names = get_knowns_encodings_multi("known-multiple")
        save_encodings_to_file(known_encodings, known_names, filename="encodings.pkl")
    t1 = time.time()
    print(f"Time to load encodings: {t1 - t0} seconds")

    # 打開攝像頭
    video_capture = cv2.VideoCapture(0)

    while True:
        # 捕獲視頻幀
        ret, frame = video_capture.read()
        if not ret:
            break

        # 縮小視頻幀以加速人臉識別過程
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # this will crash, use below instead
        # rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
        # https://stackoverflow.com/questions/75926662/face-recognition-problem-with-face-encodings-function

        # 找到視頻幀中所有人臉的位置和編碼
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations
        )

        for (top, right, bottom, left), face_encoding in zip(
            face_locations, face_encodings
        ):
            # 與已知人臉進行比對
            # threshold = 0.4  # 使用更嚴格的閾值
            threshold = 0.5
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(distances)  # 找出距離最近的已知編碼
            name = "Unknown"
            if distances[best_match_index] < threshold:
                name = known_names[best_match_index]
            # 將標記放回原始視頻幀
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )

        # 顯示帶有標記的幀
        cv2.imshow("Video", frame)

        # 按下 'q' 鍵退出循環
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 釋放視頻流資源
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
