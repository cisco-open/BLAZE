"""This implements schema class.

This module procudes a json-format flame job schema as shown in the following
as an example:
---
{
    "name": "A simple example schema v1.0.0",
    "description": "a sample schema to demostrate a TAG layout",
    "roles": [
        {
            "name": "trainer",
            "description": "It consumes the data and trains local model",
            "isDataConsumer": true
        },
        {
            "name": "aggregator",
            "description": "It aggregates the updates from trainers",
            "replica": 1
        }
    ],
    "channels": [
        {
            "name": "param-channel",
            "description": "Model update is sent from trainer to aggregator and vice-versa",
            "pair": [
                "trainer",
                "aggregator"
            ],
            "groupBy": {
                "type": "tag",
                "value": ["us", "uk"]
            },
            "funcTags": {
                "trainer": ["fetch", "upload"],
                "aggregator": ["distribute", "aggregate"]
            }
        }
    ]
}
"""

import ast
import importlib


class Role(object):
    """Role class."""

    #
    def __init__(self):
        """Initialize a role instance."""
        self.name = ""
        self.description = ""
        self.is_data_consumer = False
        self.file_dict = dict()

    def get_raw(self):
        """Return Role's data in a raw format."""
        raw_data = {
            'name': self.name,
            'description': self.description,
            "isDataConsumer": self.is_data_consumer
        }

        return raw_data


class FuncTags(object):
    """FuncTags class."""

    #
    def __init__(self):
        """Initialize a FuncTags instance."""
        self.tags: dict[str, dict[str, bool]] = dict()
        self.id_to_name: dict[str, str] = dict()

    def get_func_tags(self, role_id, role_name, file_dict):
        """Return function tags associated with a role."""
        all_tags = list()
        for content in file_dict.values():
            func_tags = self._extract_func_tags(content)
            all_tags += func_tags

        self.id_to_name[role_id] = role_name

        if role_id not in self.tags:
            self.tags[role_id] = dict()

        # delete stale tags from the status dict
        for tag in list(self.tags[role_id].keys()):
            if tag not in all_tags:
                del self.tags[role_id][tag]

        # add new tag to tag status dict
        for tag in all_tags:
            if tag in self.tags[role_id]:
                continue

            self.tags[role_id][tag] = False

        return self.tags[role_id]

    def _extract_func_tags(self, content):
        func_tags = list()

        sa = SourceAnalyzer()
        tree = ast.parse(content)
        sa.visit(tree)

        cls_info = sa.get_class_info()
        for class_name, path in cls_info.items():
            module = importlib.import_module(path)
            if not hasattr(module, class_name):
                continue

            cls_obj = getattr(module, class_name)
            if not hasattr(cls_obj, "get_func_tags"):
                continue

            fn = getattr(cls_obj, "get_func_tags")
            func_tags += fn()

        return func_tags

    def set_func_tags(self, role_id, role_name, func_tags, selected):
        """Set function tags (and its status) associated with a role."""
        self.id_to_name[role_id] = role_name

        if role_id not in self.tags:
            self.tags[role_id] = dict()

        for i, tag in enumerate(func_tags):
            self.tags[role_id][tag] = selected[i]

    def get_raw(self):
        """Return FuncTags' data in a raw format."""
        tags_dict = dict()

        for role_id, tags in self.tags.items():
            role_name = self.id_to_name[role_id]
            tag_list = list()

            for tag, selected in tags.items():
                if not selected:
                    continue
                tag_list.append(tag)

            tags_dict[role_name] = tag_list

        raw_data = tags_dict

        return raw_data


class GroupBy(object):
    """GroupBy class."""

    #
    def __init__(self):
        """Initialize a GroupBy instance."""
        self.gtype = "tag"
        self.value = []

    def get_raw(self):
        """Return GroupBy data in a raw format."""
        raw_data = {'type': self.gtype, 'value': self.value}
        return raw_data


class Channel(object):
    """Channel class."""

    #
    def __init__(self):
        """Initialize a Channel instance."""
        self.name = ""
        self.description = ""
        self.pair = ('', '')
        self.flags = [False, False, False] 
        self.group_by = GroupBy()
        self.func_tags = FuncTags()

    def get_func_tags(self, role_id, role_name, file_dict):
        """Return function tags associated with a role in this channel."""
        return self.func_tags.get_func_tags(role_id, role_name, file_dict)

    def set_func_tags(self, role_id, role_name, func_tags, selected):
        """Set function tags status associated with this channel."""
        self.func_tags.set_func_tags(role_id, role_name, func_tags, selected)

    def get_raw(self):
        """Return Channel data in a raw format."""
        (first, second) = self.pair
        raw_data = {
            'name': self.name,
            'description': self.description,
            'pair': [first, second],
            'groupBy': self.group_by.get_raw(),
            'funcTags': self.func_tags.get_raw(),
        }

        return raw_data
