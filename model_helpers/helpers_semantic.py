"""

This file contains several helper functions utilized by the ASKI dashboard. 

All functions (as well as their descriptions) are listed below: 

    answer_question(question, answer_text, model, tokenizer) - internal 
    dedup(hits) - returns list of potential hits in document, internal 
    summarize_answer(candidate_docs, summarized=None) - summarizer, internal 

"""

from transformers import pipeline
from transformers import BertTokenizer, BertForQuestionAnswering

import collections, torch, re


"""

Internal helper function used by BERT/ColBERT 

"""

def answer_question(question, answer_text, model, tokenizer):
    #global model, tokenizer

    input_ids = tokenizer.encode(
        question, answer_text, max_length=512, truncation=True)

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    outputs = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                    # The segment IDs to differentiate question from answer_text
                    token_type_ids=torch.tensor([segment_ids]),
                    return_dict=True)

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    answer = tokens[answer_start]
    # print(tokens)
    beg, end = tokens[0], tokens[answer_end+1]
    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start+1, answer_end+1):
       # print(f'{i},{tokens[i]}')
        # If it's a subword token, then recombine it with the previous token.
        if len(tokens[i]) > 2 and tokens[i][0:2] == '##':
            if 0 < i < answer_start:
                beg += tokens[i][2:]
            elif answer_start < i < answer_end+1:
                answer += tokens[i][2:]
            elif answer_end+1 < i:
                end += tokens[i][2:]

        # Otherwise, add a space then the token.
        else:
            if 0 < i < answer_start:
                beg += ' ' + tokens[i]
            elif answer_start < i < answer_end+1:
                if tokens[i] in [',', '.', ':']:
                    answer += tokens[i]
                else:
                    answer += ' ' + tokens[i]
            elif answer_end+1 < i:
                end += ' ' + tokens[i]

    print('Answer: "' + answer + '"')
    if answer == "[CLS]":
        answer, beg, end = '', '', ''
    else:
        m = re.search(answer, answer_text, re.IGNORECASE)
        if m:
            beg = answer_text[:m.start()]
            answer = answer_text[m.start():m.end()]
            end = answer_text[m.end()+1:]

    return answer, beg, end


"""

Returns list of potential hits in candidate document 

"""

def dedup(hits):
    candidate_docs = [h['_source']['message_body'] for h in hits]

    tmp = collections.Counter(candidate_docs)
    tmp = sorted(tmp, key=tmp.get, reverse=True)
    return list(tmp)


"""

Summarized answer found in candidate documents 

"""

def summarize_answer(candidate_docs, summarizer=None):
    if summarizer is None:
        summarizer = pipeline("summarization")
    sum_docs = []
    for doc in candidate_docs:
        if len(doc) > 300:
            doc = doc[:300]
        sum_docs.append(summarizer(
            doc, min_length=min(len(doc), 50), max_length=min(len(doc), 300)))

    return sum_docs