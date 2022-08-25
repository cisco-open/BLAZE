""" 
====================================================
BART 
====================================================
This module loads a BART model and makes it available for the 
dashboard to use.

https://huggingface.co/docs/transformers/model_doc/bart

"""

from aski.models.interfaces.hugging_face_model_summarization import HuggingFaceModelSummarization

def get_bart_info():
    """ 
    Function to return a dictionnary containing the name, class name, 
    description, paper link and GitHub repo link of the BART model. It is used 
    throughout the code to get various information about the model.

    Returns
    -------
    model_info : a dictionnary
        A dictionnary containing the name, class name, 
        description, paper link and GitHub repo link of the T5 model
    """
    model_info = {
        'name'       : "BART",
        'class_name' : 'Bart',
        'desc'       : "BART - Denoising Sequence-to-Sequence Pre-training",
        'link'       : "https://arxiv.org/pdf/1910.13461.pdf",
        'repo'       : "https://github.com/facebookresearch/fairseq/blob/main/examples/bart"}

    return model_info

class Bart(HuggingFaceModelSummarization):
    """BART model from 'Denoising Sequence-to-Sequence Pre-training for Natural 
    Language Generation, Translation, and Comprehension' paper"""
    
    def __init__(self):

        super().__init__(
            model_name='facebook/bart-large-cnn',
            model_info=get_bart_info(),
            max_length=1024,
            model_max_length=1024, 
            truncation=True)
