""" 
====================================================
BART 
====================================================
This module loads a BART model and makes it available for the 
dashboard to use.

https://huggingface.co/docs/transformers/model_doc/bart

"""

from aski.models.model import Model_Summary
from transformers import BartTokenizer, BartForConditionalGeneration

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

class BartRXF(Model_Summary):

	def __init__(self):

		self._info      = get_bart_info()
		self._model     = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
		self._tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
		self._summary_text = "" 


	def _summarize_text(self, text_to_summarize):

		inputs = self._tokenizer([text_to_summarize], 
								  return_tensors="pt")

		summary_ids = self._model.generate(inputs["input_ids"], 
										   num_beams=4)

		self._summary_text = self._tokenizer.batch_decode(summary_ids, 
									 skip_special_tokens=True, 
									 clean_up_tokenization_spaces=False)
		print(self._summary_text)

		
	def _summarize_dataset(self, inputs):
		summary_ids = self._model.generate(inputs["input_ids"], num_beams=4)
		self._info = get_bart_info()


	def _get_summary(self): 
		return self._summary_text