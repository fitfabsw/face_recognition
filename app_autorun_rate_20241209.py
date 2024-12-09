import logging
import os
import sys
from who_lib import knowns_dir, knowns_multi_dir, get_knowns_encondings, get_knowns_encodings_multi, who, who2, who2_multiple, who3, who3_multiple, who3_threshold, save_encodings_to_file, load_encodings_from_file

logging.basicConfig(
    level=logging.INFO,
    #format='%(asctime)s - %(levelname)s - %(message)s',
    format='%(message)s',
    handlers=[
        logging.FileHandler("app_rate.log", mode='w'),
        logging.StreamHandler(sys.stdout)  # 將日誌輸出到控制台
    ]
)

print = logging.info

# filename:abc-1.jpg
def ret_answer(filename):
    unknown_num = 0
    fname = filename.split('.')[0].split('-')[0].strip() # abc-1.jpg -> abc
    people = []
    for name in fname.split(' '):
        if name.lower().find("unknown") != -1: #find unknown
            unknown_num += 1
        else: people.append(name)

    return people, unknown_num, len(fname.split(' '))

#who_pic is list
def check_who_image(who_pic, correct_people, correct_unknown_num):
    unknown_num = 0
    people = list(correct_people)
    remove_pic = ""
    people_score_num = 0
    for w in who_pic:
        if w.lower().find("unknown") != -1: #find unknown
            unknown_num += 1
            if unknown_num <= correct_unknown_num:
                people_score_num += 1
        else:
            correct = False
            for p in people:
                if w.lower().find(p.lower()) != -1: #find people
                    correct = True
                    remove_pic = p
                    people_score_num += 1
                    break
            if correct:
                people.remove(remove_pic) #check only once
    
    return people_score_num
    
# dir_score, total_score are both list 
def handle_solution(unknown_image_file, people, unknown_num, weight, dir_score, total_score, face_num):
    people_score_num = [0] * 10
    score = [0] * 10
    print("")
    print(unknown_image_file)
    print(f"weight = {weight}")
    print(f"Expect the number of people = {face_num}")

    #whoami = who(unknown_image_file, print)
    #whoami2 = who2(unknown_image_file, print)
    whoami2_m = who2_multiple(unknown_image_file, print)
    #whoami3 = who3(unknown_image_file, print)
    whoami3_m = who3_multiple(unknown_image_file, print)
    whoami3th = who3_threshold(unknown_image_file, print)
    
    people_score_num[2] = check_who_image(whoami2_m.strip().split(' '), people, unknown_num)
    people_score_num[4] = check_who_image(whoami3_m.strip().split(' '), people, unknown_num)
    people_score_num[5] = check_who_image(whoami3th.strip().split(' '), people, unknown_num)

    score[2] = 0 if 0 == people_score_num[2] else weight / face_num * people_score_num[2]
    score[4] = 0 if 0 == people_score_num[4] else weight / face_num * people_score_num[4]
    score[5] = 0 if 0 == people_score_num[5] else weight / face_num * people_score_num[5]

    #print(f"[method1] This is {whoami}")
    #print(f"[method2] response: {whoami2}. score = {score[1]}")
    print(f"[method2_m] response: {whoami2_m}. {people_score_num[2]} people name is right, score = {score[2]}")
    #print(f"[method3] response: {whoami3}. score = {score[3]}")
    print(f"[method3_m] response: {whoami3_m}. {people_score_num[4]} people name is right, score = {score[4]}")
    print(f"[method3_th] response: {whoami3th}. {people_score_num[5]} people name is right, score = {score[5]}")

    if score[1] > 0:
        dir_score[1] += score[1]
        total_score[1] += score[1]
    if score[2] > 0:
        dir_score[2] += score[2]
        total_score[2] += score[2]
    if score[3] > 0:
        dir_score[3] += score[3]
        total_score[3] += score[3]
    if score[4] > 0:
        dir_score[4] += score[4]
        total_score[4] += score[4]
    if score[5] > 0:
        dir_score[5] += score[5]
        total_score[5] += score[5]

    #print(f"[method2] Directory score: {dir_score[1]}. Total score = {total_score[1]}")
    print(f"[method2_m] Directory score: {dir_score[2]}. Total score = {total_score[2]}")
    #print(f"[method3] Directory score: {dir_score[3]}. Total score = {total_score[3]}")
    print(f"[method3_m] Directory score: {dir_score[4]}. Total score = {total_score[4]}")
    print(f"[method3_th] Directory score: {dir_score[5]}. Total score = {total_score[5]}")

    return dir_score, total_score

def final_solution(score_1_2_4, total_score):
    print("\n================================================================")
    #print(f"[method2] Directory 1, 2, 4 score: {score_1_2_4[1]}. Final total score = {total_score[1]}")
    print(f"[method2_m] Directory 1, 2, 4 score: {score_1_2_4[2]}. Final total score = {total_score[2]}")
    #print(f"[method3] Directory 1, 2, 4 score: {score_1_2_4[3]}. Final total score = {total_score[3]}")
    print(f"[method3_m] Directory 1, 2, 4 score: {score_1_2_4[4]}. Final total score = {total_score[4]}")
    print(f"[method3_th] Directory 1, 2, 4 score: {score_1_2_4[5]}. Final total score = {total_score[5]}")

    print("\n")
    print(f"[method2_m] Final correction rate = {(total_score[2]/12) * 10} %")
    print(f"[method3_m] Final correction rate = {(total_score[4]/12) * 10} %")
    print(f"[method3_th] Final correction rate = {(total_score[5]/12) * 10} %")

if __name__ == "__main__":
    print("knowns_dir %s"% knowns_dir)
    print("knowns_multi_dir %s"% knowns_multi_dir)

    for d in os.listdir("./"):
        score_1_2_4 = [0] * 10
        total_score = [0] * 10

        d_path = "./" + d
        if os.path.isdir(d_path) and d[:3] == "比對組":
            # dd: 01, 02, 03...
            for dd in os.listdir(d_path):
                if '.' == dd[0]:
                    continue
                elif "14" == dd[:2]: #omit 14_other
                    continue 
                else:
                    if "02" == dd or "03" == dd or "04" == dd or "05" == dd or "06" == dd:
                        weight = 1
                    else:
                        weight = 0.5

                dd_path = d_path + "/" + dd
                dir_score = [0] * 10

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
                                people, unknown_num, face_num = ret_answer(ff)
                                dir_score, total_score = handle_solution(ff_path, people, unknown_num, weight, dir_score, total_score, face_num) 
                        else:
                            people, unknown_num, face_num = ret_answer(f)
                            dir_score, total_score = handle_solution(f_path, people, unknown_num, weight, dir_score, total_score, face_num)

                if "01" == dd or "02" == dd or "04" == dd:
                    score_1_2_4[1] += dir_score[1]
                    score_1_2_4[2] += dir_score[2]
                    score_1_2_4[3] += dir_score[3]
                    score_1_2_4[4] += dir_score[4]
                    score_1_2_4[5] += dir_score[5]

            final_solution(score_1_2_4, total_score)

