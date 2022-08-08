""" 
====================================================
Hugging Face Model Summary 
====================================================
This module extends the ModelSummary interface to load Hugging Face models.

"""

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from transformers.pipelines.base import KeyDataset
from tqdm.auto import tqdm
import torch

from aski.models.summarization.model_summarization import ModelSummarization

class HuggingFaceModelSummary(ModelSummarization):

    def __init__(self, model_name, max_length, truncation, model_info):

        self._info = model_info
        self._model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._pipe      = pipeline(
            "summarization", 
            model=model_name, 
            max_length=max_length, 
            truncation=truncation)

    def _summarize_dataset(self, dataset, column):

        summarization_outputs = []

        for output in tqdm(self._pipe(KeyDataset(dataset, column))):

            answer = output[0]['summary_text']
            summarization_outputs.append(answer)

        dataset.add_column(
            name=('result' + self._info['class_name']), 
            column=summarization_outputs)

        return dataset

    def _summarize_text(self, text_to_summarize):

        inputs = self._tokenizer([text_to_summarize], return_tensors="pt")

        summary_ids = self._model.generate(inputs["input_ids"], num_beams=4)

        summary_text = self._tokenizer.batch_decode(summary_ids, 
                                     skip_special_tokens=True, 
                                     clean_up_tokenization_spaces=False)
        return summary_text
