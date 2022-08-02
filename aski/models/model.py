""" 
====================================================
MODEL 
====================================================
This module loads a given model and makes it available for the 
dashboard to use.

"""

# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================

# ==============================================================================
# ============================== MODEL CLASS ===================================
# ==============================================================================


class Model_Summary():

    def __init__(self):
        pass

    def load_model(self, file_name, file_content):
        ''' Load a model from a directory or library'''
        self.file_name = file_name 
        self.file_content = file_content 
        pass

    def gen_summary(self):
        '''Index/fine-tune if necessary'''
        pass
        
    def _get_model_info(self):
        pass


class Model_Search():

    def __init__(self):
        pass

    def load_model(self, file_name, file_content): 
        self.file_name = file_name
        self.file_content = file_content
        pass 

    def file_search(self, search_term):
        ''' Load a model from a directory or library'''
        pass
    
    def _get_model_info(self):
        pass
