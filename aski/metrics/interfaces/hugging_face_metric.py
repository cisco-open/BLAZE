from aski.metrics.interfaces.metric import Metric
import evaluate

class HuggingFaceMetric(Metric):

	def __init__(self, metric_name, lang):
		
		self._metric_name = metric_name
		self._metric      = evaluate.load(metric_name)
		self._lang		  = lang

	def _compute_metric(self, preds, refs):

		results = self._metric .compute(predictions=preds, references=refs)
		return results