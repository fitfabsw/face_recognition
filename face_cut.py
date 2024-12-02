import cv2
import face_recognition
import os

def SaveFacesFromFolder(input_dir):
    # 檢查輸入資料夾是否存在
    
    if not os.path.exists(input_dir):
        print(f"Error: Input folder '{input_dir}' does not exist.")
        return

    # 建立輸出資料夾（如果不存在）
    output_dir=input_dir+"_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍歷輸入資料夾中的所有圖片
    for dirname in os.listdir(input_dir):
        input_dir_path = os.path.join(input_dir, dirname)
        if '.DS_Store' in input_dir_path :
            continue
        for filename in os.listdir(input_dir_path):
            input_path = os.path.join(input_dir_path, filename)

            # 確保處理的是圖片文件
            if not os.path.isfile(input_path) or not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            print(f"Processing: {filename}")

            # 嘗試讀取圖片並進行人臉偵測
            try:
                # 加載圖片
                image = face_recognition.load_image_file(input_path)

                # 偵測人臉位置
                face_locations = face_recognition.face_locations(image)

                # 轉換為 OpenCV 的 BGR 格式
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # 處理每張人臉
                for i, (top, right, bottom, left) in enumerate(face_locations):
                    # 擷取人臉
                    face_image = image[top:bottom, left:right]

                    # 保存裁剪後的人臉
                    if not os.path.exists(os.path.join(output_dir,input_dir_path)):
                        os.makedirs(os.path.join(output_dir,input_dir_path))
                    face_filename = os.path.join(output_dir,input_dir_path, f"{os.path.splitext(filename)[0]}_face_{i+1}.jpg")
                    cv2.imwrite(face_filename, face_image)

                    # 在原圖上繪製框線與標籤
                    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(image, f"Face {i+1}", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

                # 保存處理後的原圖（可選）
                # processed_filename = os.path.join(output_dir,input_dir_path, f"processed_{filename}")
                # cv2.imwrite(processed_filename, image)

                print(f"Saved {len(face_locations)} face(s) from '{filename}'.")

            except Exception as e:
                print(f"Error processing '{filename}': {e}")

# 使用範例
SaveFacesFromFolder("face_image")
