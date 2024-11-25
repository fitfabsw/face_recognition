import logging
import os
import sys
import face_recognition

logging.basicConfig(
    level=logging.INFO,
    #format='%(asctime)s - %(levelname)s - %(message)s',
    format='%(message)s',
    handlers=[
        logging.FileHandler("potential_problem.log", mode='w'),
        logging.StreamHandler(sys.stdout)  # 將日誌輸出到控制台
    ]
)

print = logging.info

accepted_people = [
    "安倍晉三",
    "岸田文雄",
    "林百里",
    "Antony_John_Blinken",
    "Barack_Obama",
    "beyonce",
    "Bill_Clinton",
    "Donald_John_Trump",
    "Elon_Musk",
    "Hillary_Clinton",
    "Jensen_Huang",
    "Joe_Biden",
    "Kamala_Harris",
    "Marco_Rubio",
    "Mark_Zuckerberg",
    "Michelle_Obama",
    "Morris_Chang",
    "Robyn_Rihanna",
    "Taylor_Swift",
    "Tim_Cook",
    "unknown"
]

dir_len = [
    40,
    10,
    10,
    10,
    10,
    10,
    40,
    10,
    10,
    10,
    10,
    10,
    10
]

# filename:abc-1.jpg
def parse_answer(filename):
    fname = filename.split('.')[0].split('-')[0].strip() # abc-1.jpg -> abc

    if not fname: # fname is null string
        return False, -1

    for name in fname.split(' '):
        is_accepted = False
        for p in accepted_people:
            if name.lower().find(p.lower()) != -1: # Found accepted people
                is_accepted = True
                break
        if not is_accepted:
            print(f"Wrong file name is {name}")
            return False, -1

    return True, len(fname.split(' '))

def image_face_num(image_path):
    unknown_image = face_recognition.load_image_file(image_path)
    return len(face_recognition.face_encodings(unknown_image))

if __name__ == "__main__":

    file_num_list = [0] * 13
    
    for d in os.listdir("./"):

        d_path = "./" + d
        if os.path.isdir(d_path) and d[:3] == "比對組":
            # dd: 01, 02, 03...
            for dd in os.listdir(d_path):
                if '.' == dd[0]:
                    continue
                elif "14" == dd[:2]: #omit 14_other
                    continue 

                dd_path = d_path + "/" + dd

                if os.path.isdir(dd_path):
                    dfile_num = 0
                    ddfile_num = 0 #for 07 dir
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
                                if not parse_answer(ff)[0]: # Parse answer fail
                                    print(f"file path : {ff_path}")
                                    print(f"File name is wrong: {ff}")
                                elif parse_answer(ff)[1] != image_face_num(ff_path):
                                    print(f"file path : {ff_path}")
                                    print(f"There are {image_face_num(ff_path)} people in image, but expect {parse_answer(ff)[1]}")
                                ddfile_num += 1
                        else:
                            if not parse_answer(f)[0]: # Parse answer fail
                                print(f"file path : {f_path}")
                                print(f"File name is wrong: {f}")
                            elif parse_answer(f)[1] != image_face_num(f_path):
                                print(f"file path : {f_path}")
                                print(f"There are {image_face_num(f_path)} people in image, but expect {parse_answer(f)[1]}")
                            dfile_num += 1
                    
                    try:
                        dir_index = int(dd) - 1
                        if 6 == dir_index: # for 07 dir
                            file_num_list[dir_index] = ddfile_num
                        elif 0 <= dir_index <= 12: # for 01 ~ 13 dir
                            file_num_list[dir_index] = dfile_num
                    except:
                        print("To handle length of directory error! for dd = %s" % dd)
                        
            # after for dd in os.listdir(d_path)
            for i, fnum in enumerate(file_num_list):
                if fnum == dir_len[i]:
                    print(f"The number of files in {i+1} are {fnum}, expect = {dir_len[i]}, matched.")
                else:
                    print(f"The number of files in {i+1} are {fnum}, expect = {dir_len[i]}, NOT matched.")
                    
