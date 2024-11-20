import logging
import os
import sys
from who_lib import knowns_dir, knowns_multi_dir, get_knowns_encondings, get_knowns_encodings_multi, who, who2, who2_multiple, who3, who3_multiple, who3_threshold, save_encodings_to_file, load_encodings_from_file

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

def print_solution(unknown_image_file):
    print("")
    print(unknown_image_file)

    #whoami = who(unknown_image_file, print)
    whoami2 = who2(unknown_image_file, print)
    whoami2_m = who2_multiple(unknown_image_file, print)
    whoami3 = who3(unknown_image_file, print)
    whoami3_m = who3_multiple(unknown_image_file, print)
    whoami3th = who3_threshold(unknown_image_file, print)
    
    #print(f"[method1] This is {whoami}")
    print(f"[method2] This is {whoami2}")
    print(f"[method2_m] They are {whoami2_m}")
    print(f"[method3] This is {whoami3}")
    print(f"[method3_m] They are {whoami3_m}")
    print(f"[method3_th] This is {whoami3th}")

if __name__ == "__main__":
    print("knowns_dir %s"% knowns_dir)
    print("knowns_multi_dir %s"% knowns_multi_dir)

    for d in os.listdir("./"):
        d_path = "./" + d
        if os.path.isdir(d_path) and d[:3] == "比對組":
            # dd: 01, 02, 03...
            for dd in os.listdir(d_path):
                if '.' == dd[0]:
                    continue 
                dd_path = d_path + "/" + dd
                if os.path.isdir(dd_path):
                    for f in os.listdir(dd_path):
                        if '.' == f[0]:
                            continue
                        f_path = dd_path + "/" + f
                        # for 07 dir
                        if os.path.isdir(f_path):
                            for ff in os.listdir(f_path):
                                if '.' == ff[0]:
                                    continue
                                ff_path = f_path + "/" + ff
                                print_solution(ff_path) 
                        else:
                            print_solution(f_path)

