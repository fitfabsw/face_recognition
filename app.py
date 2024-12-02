import logging
import os
import sys
from who_lib import knowns_dir, knowns_multi_dir, get_knowns_encondings, get_knowns_encodings_multi, who, who2, who2_multiple, who3, who3_multiple, who3_threshold, save_encodings_to_file, load_encodings_from_file ,Draw

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

if __name__ == "__main__":
    print("knowns_dir %s"% knowns_dir)
    print("knowns_multi_dir %s"% knowns_multi_dir)
    while True:
        unknown_image_file = input("Please enter image path:")
        if unknown_image_file == "":
            break
        #whoami = who(unknown_image_file)
        whoami2 = who2(unknown_image_file, print)
        whoami2_m = who2_multiple(unknown_image_file, print)
        whoami3 = who3(unknown_image_file, print)
        whoami3_m = who3_multiple(unknown_image_file, print)
        whoami3th = who3_threshold(unknown_image_file, print)
        print(unknown_image_file)
        #print(f"[method1] This is {whoami}")
        print(f"[method2] This is {whoami2}")
        print(f"[method2_m] They are {whoami2_m}")
        print(f"[method3] This is {whoami3}")
        print(f"[method3_m] This is {whoami3_m}")
        print(f"[method3_th] This is {whoami3th}")
        Draw(unknown_image_file)
