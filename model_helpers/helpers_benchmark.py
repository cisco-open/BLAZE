"""

This file contains several helper functions used to benchmark. 

All functions (as well as their descriptions) are listed below: 

    squad_benchmark(pQueue, name, dir, m_name) - main function called by ASKI
    was_correct(m_ans, q_ansl) - given list of answers, determines correctness


NOTE: ASKI's solo benchmarking feature may not work at the moment 
      due to ongoing changes in this file (no longer stable). Will
      be fixed shortly in a future commit! 
   
"""

from Models.ColbertSearch import *
from Models.ElasticSearch import *
#from app_constants import *
import os
import json

import numpy as np
from fuzzywuzzy import fuzz
import logging
import sys


"""

Runs the inputted model (either ColBERT or Elastic) on a SQUAD dataset

"""


def squad_benchmark(pQueue, name, dir, m_name):
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    f = open(dir, "r")
    lines = f.readlines()[1:]
    f.close()
    f_content = "".join(lines)

    q_dir = "/".join(dir.split("/")[:-1]) + "/"
    files = [files[2] for files in os.walk(q_dir)][0]
    questions = [file for file in files if file[:3] == "qas"]

    results = {
        "m_name": m_name,
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

    if m_name == "ColBERT":
        model = ColbertSearch(name, f_content)
    else:
        model = ElasticSearch(name, f_content)

    pQueue.put_nowait(results)

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

                pQueue.put_nowait(results)

            except:
                print("EXITED PREMATURELY")
                logging.debug('A debug message!')
                pass

        print("========================")

    results["times"]["avg_ts"] = np.mean(results["times"]["all_ts"])
    results["metrics"]["accuracy_num"] = results["metrics"]["correct_arr"].count(
        1)
    results["metrics"]["accuracy_prc"] = np.mean(
        results["metrics"]["correct_arr"])

    print(results)
    pQueue.put("DONE")


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
