"""

This file contains several helper functions used to benchmark. 

All functions (as well as their descriptions) are listed below: 

    squad_benchmark(pQueue, name, dir, m_name) - main function called by ASKI
    was_correct(m_ans, q_ansl) - given list of answers, determines correctness


NOTE: ASKI's solo benchmarking feature may not work at the moment 
      due to ongoing changes in this file (no longer stable). Will
      be fixed shortly in a future commit! 
   
"""

from aski.dash_files.app_constants import * 
import os
import json

import numpy as np
from fuzzywuzzy import fuzz


"""

Runs the inputted model (either ColBERT or Elastic) on a SQUAD dataset

"""


def squad_benchmark(queue, file_name, file_path, model_obj):


    # Load all questions/files for associated dataset (SQUAD)

    f = open(file_path, "r")
    lines = f.readlines()[1:]
    f.close()
    file_content = "".join(lines)

    q_dir = "/".join(file_path.split("/")[:-1]) + "/"
    files = [files[2] for files in os.walk(q_dir)][0]
    questions = [file for file in files if file[:3] == "qas"]


    # Creating results dictionary (use to store/dump in queue)

    results = CONST_RESULTS

    results['m_name'] = model_obj._info['class_name']
    results['f_name'] = file_name 
    results['root'] = q_dir 

    results['questions']['num_qf'] = len(questions) 
    results['questions']['all_qs'] = questions 



    model_obj.load_model(file_name, file_content)
    queue.put_nowait(results)


    # Find number of answerable questions (some are impossible)

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


    # Start iterating through all answerable questions

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

                print(f"(squad_benchmark) > Question: {q_text}")
                print(f"(squad_benchmark) > Valid ans: {q_ansl}")

                res, time = model_obj.file_search(q_text)
                m_ans = res[0]['res']

                valid = was_correct(m_ans, q_ansl)

                print(f"(squad_benchmark) > Time Taken: {time}")
                print(f"(squad_benchmark) > Corect?: {valid}")

                results["questions"]["tot_qs"] = results["questions"]["tot_qs"] + 1
                results["times"]["all_ts"].append(time)
                results["metrics"]["correct_arr"].append(valid)

                if valid == 0:
                    results["metrics"]["incorrect_d"][q_text] = [
                        m_ans, q_ansl, q_data['context']]

                queue.put_nowait(results)

            except:
                print(f"(squad_benchmark) > Exited prematurely, skipping question.")
                pass



    results["times"]["avg_ts"] = np.mean(results["times"]["all_ts"])
    results["metrics"]["accuracy_num"] = results["metrics"]["correct_arr"].count(1)
    results["metrics"]["accuracy_prc"] = np.mean(results["metrics"]["correct_arr"])

    queue.put("DONE")


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
