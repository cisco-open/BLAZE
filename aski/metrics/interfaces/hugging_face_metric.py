from aski.metrics.interfaces.metric import Metric
import evaluate

class HuggingFaceMetric(Metric):

    def __init__(self, metric_name, lang, class_name, metric_keys, verbose=True):

        if verbose == True:
            print('> Loading ' + class_name + ' metric...')

        self._metric_name = metric_name
        self._class_name  = class_name
        self._metric      = evaluate.load(metric_name)
        self._lang        = lang
        self._metric_keys = metric_keys
        
        print('\n> Finished loading ' + class_name + ' metric.\n')

    def _compute_metric(self, preds, refs):

        print('compute function')
        results = self._metric.compute(predictions=preds, references=refs)
        return results

    def _get_class_name(self):
        return self._class_name