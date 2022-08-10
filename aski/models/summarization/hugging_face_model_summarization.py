""" 
====================================================
Hugging Face Model Summary 
====================================================
This module extends the ModelSummary interface to load Hugging Face models.

"""

import torch
from tqdm.auto import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, SummarizationPipeline
from transformers.pipelines.base import KeyDataset

from aski.models.summarization.model_summarization import ModelSummarization

class HuggingFaceModelSummarization(ModelSummarization):
    """
    A Superclass used to build HuggingFace models for summarization


    Attributes
    ----------
    _info : dictionnary
        A dictionnary containing the name, class name, description, paper link 
        and GitHub repo link of the model
    _max_length : int
        The maximum length parameter of the model
    _truncation : boolean
        Whether or not to truncate input sequences
    _model : AutoModelForSeq2SeqLM
        A HuggingFace model for summarization
    _tokenizer : AutoTokenizer
        A HuggingFace tokenizer 
    _pipe : SummarizationPipeline
        A HuggingFace pipeline for summarization

    Methods
    -------
    _summarize_dataset(self, dataset, column):
        Summarizes a dataset and appends to it a column with the summarized text.

    _summarize_text(self, text_to_summarize):
        Summarizes a piece of text and returns it.

    """

    def __init__(self, model_name, max_length, model_max_length, truncation, model_info, verbose=True):

        self._info       = model_info
        self._max_length = max_length
        self._truncation = truncation

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' model...')

        self._model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name, 
            max_length=max_length)

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' tokenizer...')

        self._tokenizer = AutoTokenizer.from_pretrained(
            model_name, 
            max_length=max_length,
            model_max_length=model_max_length,
            truncation=truncation)

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' pipe...')

        self._pipe = SummarizationPipeline(
            model=self._model, 
            tokenizer=self._tokenizer)

        if verbose == True:

            print('\n> Finished loading ' + self._info['name'] + ' class.\n')

    def _summarize_dataset(self, dataset, column):
        """ 
        Method that takes in a HuggingFace dataset and the name of the column of
        the dataset that contains the text to summarize. It calls the 
        summarization pipeline attribute and runs it on the whole dataset. It 
        saves the results in a list and adds this list to the dataset object and
        returns it.

        Parameters
        ----------
        dataset : a HuggingFace dataset object
            The HuggingFace dataset to summarize
        column : str
            The name of the column ofthe dataset with the text to summarize

        Returns
        -------
        dataset : a HuggingFace dataset object
            The HuggingFace dataset to summarize with the summarized text column
        """

        summarization_outputs = []

        for output in tqdm(self._pipe(KeyDataset(dataset, column))):

            answer = output[0]['summary_text']
            summarization_outputs.append(answer)

        dataset.add_column(
            name=('result' + self._info['class_name']), 
            column=summarization_outputs)

        return dataset

    def _summarize_text(self, text_to_summarize):
        """ 
        Method that takes in a piece of text and summarizes it by calling the 
        tokenizer and model attributes and finally returns it.

        Parameters
        ----------
        text_to_summarize : str
            The piece of text to summarize

        Returns
        -------
        summary_text : str
            The summarized text
        """

        inputs = self._tokenizer(
            [text_to_summarize], 
            return_tensors="pt", 
            max_length=self._max_length,
            truncation=self._truncation)

        summary_ids = self._model.generate(
            inputs["input_ids"], 
            num_beams=4, 
            max_length=self._max_length)

        summary_text = self._tokenizer.batch_decode(
            summary_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False)

        return summary_text
