""" 
====================================================
MUPPET 
====================================================
This module loads a MUPPET model and makes it available for the 
dashboard to use.

"""


from aski_summarization.models.model import Model


# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================

def get_muppet_info():

    model_info = {
        'name'       : "MUPPET",
        'class_name' : "Muppet",
        'desc'       : "Muppet - Massive Multi-task Representations",
        'link'       : "https://arxiv.org/pdf/2101.11038.pdf",
        'repo'       : "https://huggingface.co/facebook/muppet-roberta-base"}

    return model_info

# ==============================================================================
# ============================= MUPPET CLASS ===================================
# ==============================================================================

class Muppet(Model):

	def __init__(self):
		self._info = get_muppet_info()

