""" 
====================================================
MUPPET 
====================================================
This module loads a MUPPET model and makes it available for the 
dashboard to use.

"""


<<<<<<< HEAD
from aski.models.model import Model
=======
from aski.models.model import Model_Summary
>>>>>>> fb353a3ed880d07d309ad6bf9bac1f2166570658


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

class Muppet(Model_Summary):

	def __init__(self):
		self._info = get_muppet_info()

    def get_name(self): 
        return self._info['name']
