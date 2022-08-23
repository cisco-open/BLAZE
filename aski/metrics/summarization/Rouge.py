from aski.metrics.interfaces.hugging_face_metric import HuggingFaceMetric

class Rouge(HuggingFaceMetric):
    
    def __init__(self):
        super().__init__(
        	metric_name='rouge', 
        	lang='en', 
        	class_name='Rouge', 
        	metric_keys=['rouge1', 'rouge2', 'rougeL'])