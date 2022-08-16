from aski.metrics.interfaces.hugging_face_metric import HuggingFaceMetric

class Bleu(HuggingFaceMetric):
    
    def __init__(self):
        super().__init__(metric_name='bleu', lang='en')
