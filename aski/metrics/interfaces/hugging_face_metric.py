
# Copyright 2022 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0



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