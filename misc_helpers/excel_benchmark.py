"""

This is an OLD script used to create an excel spreadsheet (dump.xlsx) of 
ColBERT on all SQUAD Question/Answering datasets. Running this script 
will NOT work as of now, as it is currently still needs to be ported. 

However, feel free to take a look at dump.xlsx for some results! 

"""


from ColbertSearch import *
from dash_files.app_constants import *
import os
import json
import numpy as np

from fuzzywuzzy import fuzz
from openpyxl import Workbook

"""

Runs the ColBERT model on the given SQUAD dataset 

"""


def squad_benchmark(name, dir):

    f = open(dir, "r")
    lines = f.readlines()[1:]
    f.close()
    f_content = "".join(lines)

    q_dir = "/".join(dir.split("/")[:-1]) + "/"
    files = [files[2] for files in os.walk(q_dir)][0]
    questions = [file for file in files if file[:3] == "qas"]

    results = {
        "name": name,
        "root": q_dir,
        "questions": {
            "num_qf": len(questions),
            "num_qs": 0,
            "all_qs": questions,
            "tot_qs": 0,
        },
        "times": {
            "avg_ts": 0,
            "all_ts": [],
        },
        "metrics": {
            "correct_arr": [],
            "incorrect_d": {},
            "accuracy_num": 0,
            "accuracy_prc": 0,
        }
    }

    model = ColbertSearch(name, f_content)

    tot_q = 0
    for q_file in questions:
        q = open(q_dir + q_file, "r")
        q_data = json.load(q)
        q.close()
        for qas in q_data['qas']:
            if len(qas['answers']) == 0:
                continue
            if qas["is_impossible"]:
                continue
            tot_q = tot_q + 1

    results["questions"]["num_qs"] = tot_q

    for q_file in questions:

        q = open(q_dir + q_file, "r")
        q_data = json.load(q)
        q.close()

        for qas in q_data['qas']:
            try:
                q_text = qas['question']
                q_anss = qas['answers']
                q_ansl = []
                for ans in q_anss:
                    q_ansl.append(ans['text'])
                if len(q_ansl) == 0:
                    break

                print(f"QUESTION: {q_text}")
                print(f"POSS ANS: {q_ansl}")

                res, time = model.file_search(q_text)
                m_ans = res[0]['res']

                valid = was_correct(m_ans, q_ansl)

                print(f"TIME TAK: {time}")
                print(f"CORRECT?: {valid}")

                results["questions"]["tot_qs"] = results["questions"]["tot_qs"] + 1
                results["times"]["all_ts"].append(time)
                results["metrics"]["correct_arr"].append(valid)

                if valid == 0:
                    results["metrics"]["incorrect_d"][q_text] = [
                        m_ans, q_ansl, q_data['context']]

            except:
                print("EXITED PREMATURELY")
                pass

        print("========================")

    results["times"]["avg_ts"] = np.mean(results["times"]["all_ts"])
    results["metrics"]["accuracy_num"] = results["metrics"]["correct_arr"].count(
        1)
    results["metrics"]["accuracy_prc"] = np.mean(
        results["metrics"]["correct_arr"])

    return results


"""

Determines whether the model's answer matches the ground truth 

"""


def was_correct(m_ans, q_ansl):
    m_ans = m_ans.lower()
    m_ans = m_ans.replace(" ", "")

    for poss_ans in q_ansl:
        poss_ans = poss_ans.lower()
        poss_ans = poss_ans.replace(" ", "")

        if m_ans in poss_ans or poss_ans in m_ans or fuzz.partial_ratio(m_ans, poss_ans):
            return 1

    return 0


"""

Runs ColBERT model through ALL SQUAD datasets, dumping results in xlsx

"""


def main():
    n_squad, p_squad = [], []
    datasets = [dir[0] for dir in os.walk(data['data']['DATA_PATH'])]

    for dir in datasets[1:]:
        name = dir.split("/")[-1]
        n_squad.append(name.replace("_", " "))
        p_squad.append(dir + "/story.txt")

    workbook = Workbook()
    sheet = workbook.active
    for i in range(len(n_squad)):
        res = squad_benchmark(n_squad[i], p_squad[i])

        cols = [str(l + str(i+1)) for l in "ABCDEFG"]
        sheet[cols[0]] = res["name"]  # A
        sheet[cols[1]] = res["root"]  # B
        sheet[cols[2]] = res["metrics"]["accuracy_prc"]  # C
        sheet[cols[3]] = res["times"]["avg_ts"]  # D
        sheet[cols[4]] = res["metrics"]["accuracy_num"]  # E
        sheet[cols[5]] = res["questions"]["tot_qs"]  # F
        sheet[cols[6]] = str(res["metrics"]["incorrect_d"])  # G

        workbook.save(filename="dump.xlsx")


if __name__ == "__main__":
    main()
