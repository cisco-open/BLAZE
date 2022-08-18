from aski.metrics.interfaces.hugging_face_metric import HuggingFaceMetric

class BertScore(HuggingFaceMetric):
    
    def __init__(self):
        super().__init__(metric_name='bertscore', lang='en', class_name='BertScore')