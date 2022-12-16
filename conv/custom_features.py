
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



from mindmeld.models.helpers import register_query_feature, register_entity_feature


@register_query_feature(feature_name='average-token-length')
def extract_average_token_length(**args):
    """
    Example query feature that gets the average length of normalized tokens in the query

    Returns:
        (function) A feature extraction function that takes a query and
            returns the average normalized token length
    """
    def _extractor(query, resources):
        tokens = query.normalized_tokens
        average_token_length = sum([len(t) for t in tokens]) / len(tokens)
        return {'average_token_length': average_token_length}

    return _extractor


@register_entity_feature(feature_name='entity-span-start')
def extract_entity_span_start(**args):
    """
    Example entity feature that gets the start span for each entity

    Returns:
        (function) A feature extraction function that returns the start span of the entity
    """
    def _extractor(example, resources):
        query, entities, entity_index = example
        features = {}

        current_entity = entities[entity_index]
        current_entity_token_start = current_entity.token_span.start

        features['entity_span_start'] = current_entity_token_start
        return features

    return _extractor
