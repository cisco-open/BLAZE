""" 
====================================================
T5 
====================================================
This module loads a T5 model and makes it available for the 
dashboard to use.

https://huggingface.co/docs/transformers/model_doc/t5

"""


from aski.models.summarization.hugging_face_model_summary import HuggingFaceModelSummary


# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================


def get_t5_info():

    model_info = {
        'name'       : "T5",
        'class_name' : 'T5',
        'desc'       : "T5 - Exploring the Limits of Transfer Learning",
        'link'       : "https://arxiv.org/pdf/1910.10683.pdf",
        'repo'       : "https://github.com/google-research/text-to-text-transfer-transformer"}

    return model_info


# ==============================================================================
# =============================== BART CLASS ===================================
# ==============================================================================


class T5(HuggingFaceModelSummary):

    def __init__(self):

        super().__init__(
            model_name='t5-base',
            model_info=get_t5_info(),
            max_length=50, 
            truncation=True)