""" 
====================================================
BART 
====================================================
This module loads a BART model and makes it available for the 
dashboard to use.

"""


from aski_summarization.models.model import Model


# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================

def get_bart_info():

    model_info = {
        'name'       : "BART-RXF",
        'class_name' : 'BartRXF',
        'desc'       : "BART-RXF - Reducing Representational Collapse",
        'link'       : "https://arxiv.org/pdf/2008.03156v1.pdf",
        'repo'       : "https://github.com/stanford-futuredata/ColBERT"}

    return model_info

# ==============================================================================
# =============================== BART CLASS ===================================
# ==============================================================================

class BartRXF(Model):

	def __init__(self):
		self._info = get_bart_info()
