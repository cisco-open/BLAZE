""" 
====================================================
BART 
====================================================
This module loads a BART model and makes it available for the 
dashboard to use.

https://huggingface.co/docs/transformers/model_doc/bart

"""


from aski.models.summarization.hugging_face_model_summary import HuggingFaceModelSummary


# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================


def get_bart_info():

    model_info = {
        'name'       : "BART",
        'class_name' : 'Bart',
        'desc'       : "BART - Denoising Sequence-to-Sequence Pre-training",
        'link'       : "https://arxiv.org/pdf/1910.13461.pdf",
        'repo'       : "https://github.com/facebookresearch/fairseq/blob/main/examples/bart"}

    return model_info


# ==============================================================================
# =============================== BART CLASS ===================================
# ==============================================================================


class Bart(HuggingFaceModelSummary):

    def __init__(self):

        super().__init__(
            model_name='facebook/bart-large',
            model_info=get_bart_info(),
            max_length=1020,
            model_max_length=1020, 
            truncation=True)
