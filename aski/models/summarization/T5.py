""" 
====================================================
T5 
====================================================
This module loads a T5 model and makes it available for the 
dashboard to use.

https://huggingface.co/docs/transformers/model_doc/t5

"""

from aski.models.interfaces.hugging_face_model_summarization import HuggingFaceModelSummarization

def get_t5_info():
    """ 
    Function to return a dictionnary containing the name, class name, 
    description, paper link and GitHub repo link of the T5 model. It is used 
    throughout the code to get various information about the model.

    Returns
    -------
    model_info : a dictionnary
        A dictionnary containing the name, class name, 
        description, paper link and GitHub repo link of the T5 model
    """
    model_info = {
        'name'       : "T5",
        'class_name' : 'T5',
        'desc'       : "T5 - Exploring the Limits of Transfer Learning",
        'link'       : "https://arxiv.org/pdf/1910.10683.pdf",
        'repo'       : "https://github.com/google-research/text-to-text-transfer-transformer"}

    return model_info

class T5(HuggingFaceModelSummarization):
    """T5 model from 'Exploring the Limits of Transfer Learning with a Unified
     Text-to-Text Transformer' paper"""

    def __init__(self):

        super().__init__(
            model_name='t5-base',
            model_info=get_t5_info(),
            max_length=2000, 
            model_max_length=2000,
            truncation=True)
