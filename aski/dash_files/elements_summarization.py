from dash import html 

class SummarizationInterface(): 

    def __init__(self, params):
        self.params = params 

    def get_page(self): 
        return html.P("Hello.")
    
    def get_page_custom(self, params): 
        pass 

    def get_page_benchmark(self, params): 
        pass

    def get_page_comparison(self, params): 
        pass 

