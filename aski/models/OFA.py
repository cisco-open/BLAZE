""" 
====================================================
OFA 
====================================================
This module loads an OFA-Large model and makes it available for the 
dashboard to use.

"""


from aski.models.model import Model_Summary


# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================

def get_ofa_info():

    model_info = {
        'name'       : "OFA-Large",
        'class_name' : 'OFA',
        'desc'       : "OFA - Unifying Architectures, Tasks, and Modalities",
        'link'       : "https://arxiv.org/pdf/2202.03052v2.pdf",
        'repo'       : "https://huggingface.co/OFA-Sys/OFA-large"}

    return model_info

# ==============================================================================
# =============================== BART CLASS ===================================
# ==============================================================================

class OFA(Model_Summary):

	def __init__(self):
		self._info = get_ofa_info()

    def get_name(self): 
        return self._info['name']