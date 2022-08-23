"""This implements logic for flame workload design."""

import json
from enum import Enum

import ast
import importlib


class Sort(Enum):
    """Sort enum class."""

    Node = 1
    Edge = 2


class Node(object):
    """This implements node class."""

    #
    def __init__(self, node_id: str, label: str, type : str) -> None:
        """Initialize node instance."""

        self.node_id = node_id # Internal node ID (Model X or Data X)
        self.label = label # Name of node (ex. ColBERT, ElasticBERT, SQUAD 2.0)
        self.type = type # Either "data" or "model"

        self.role = Role()
        self.channels = dict()


    def node_to_callback(self):
        """Return node in callback-compatible format."""

        return {
            'data': {
                'id': self.node_id,
                'label': self.label,
                'sort': Sort.Node.name, 
            }
        }

    @classmethod
    def edge_to_callback(cls, u, v):
        """Return edge between left and node in callback-compatible format."""
        return {
            'data': {
                'source': u.node_id,
                'target': v.node_id,
                'sort': Sort.Edge.name,
                'label': u.channels[v].name, 
                'flags': u.channels[v].flags,
            }
        }

    def set_label(self, text):
        print(f"Switching label from {self.label} to {text}")
        self.label = text 

    def set_description(self, text):
        """Update  description in the role object."""
        self.role.description = text

    def set_data_consumer(self, is_data_consumer):
        """Update data consumer flag in the role object."""
        self.role.is_data_consumer = is_data_consumer

    def set_files(self, file_dict):
        """Update uploaded files in the role object."""
        self.role.file_dict = file_dict

    def get_node_details(self):
        """Return details on node."""
        self.role.name = self.label
        return (self.role.name, self.role.description,
                self.type, self.role.file_dict.keys())

    def get_edge_details(self, v):
        """Return details on node."""
        channel = self.channels[v]

        nodes = [{
            'id': self.node_id,
            'label': self.label
        }, {
            'id': v.node_id,
            'label': v.label
        }]

        return channel.name, channel.description, nodes, channel.flags

    def get_func_tags(self, other):
        """Return a dictionary of function tags associated with this node."""
        channel = self.channels[other]
        return channel.get_func_tags(self.node_id, self.role.name,
                                     self.role.file_dict)

    def set_func_tags(self, other, func_tags, selected):
        """Set function tags associated with this node."""
        channel = self.channels[other]
        channel.set_func_tags(self.node_id, self.role.name, func_tags,
                              selected)


class Design(object):
    """Design Interface class."""

    def __init__(self):
        """Initialize a design instance."""
        self.reset()

    def reset(self):
        """Reset design."""
        self.name = ""
        self.description = ""
        self.graph: dict[str, Node] = dict()
        self.counter = 0

    def get_new_node(self, type):
        """Return a new node."""
        self.counter += 1

        if type == "data": 
            prefix = "Data"
        elif type == "model": 
            prefix = "Model"
        else: 
            prefix = "Role"

        label = f"{prefix} {self.counter}"
        node = Node(label, label, type)

        self.graph[node.node_id] = node

        return node.node_to_callback()

    def link(self, elements) -> bool:
        """Link one or two nodes."""
        if elements is None or not (len(elements) == 1 or len(elements) == 2):
            return False

        if len(elements) == 1:
            # self edge
            cb_u = elements[0]
            cb_v = elements[0]
        else:
            cb_u = elements[0]
            cb_v = elements[1]

        if cb_u['sort'] != Sort.Node.name and cb_v['sort'] != Sort.Node.name:
            return False

        u = self._get_node(cb_u, 'id')
        v = self._get_node(cb_v, 'id')

        if v in u.channels:
            return False

        # link nodes
        channel = Channel()
        if v not in u.channels:
            u.channels[v] = channel
        if u not in v.channels:
            v.channels[u] = channel

        # add label
        edge_label = u.label + "-" + v.label
        u.channels[v].name = edge_label
        v.channels[u].name = edge_label

        return True

    def find_node_by_label(self, label: str):
        """Return node from node name."""
        for _, v in self.graph.items():
            if v.label == label:
                return v

        return None


    def find_node_by_id(self, id: str):
        """Return node from node name."""
        for _, v in self.graph.items():
            if v.node_id == id:
                return v

        return None

    def get_nodes_edges(self):
        """
        Return nodes and edges as a list.

        Each item in the list is callback-compatible.
        """
        nodes_edges = list()
        edge_map = dict()
        for u in self.graph.values():
            cb_node = u.node_to_callback()
            nodes_edges.append(cb_node)

            for v in u.channels.keys():
                key = u.node_id + "-" + v.node_id
                rev_key = v.node_id + "-" + u.node_id

                cb_edge = Node.edge_to_callback(u, v)
                if key in edge_map or rev_key in edge_map:
                    continue
                edge_map[key] = cb_edge

        for cb_edge in edge_map.values():
            nodes_edges.append(cb_edge)

        return nodes_edges

    def remove_elements(self, elements):
        """Remove elements from a design graph."""
        for element in elements:
            self._remove_element(element)

    def _remove_element(self, element):
        if element['sort'] == Sort.Edge.name:
            u = self._get_node(element, 'source')
            v = self._get_node(element, 'target')

            del u.channels[v]
            if u is not v:
                del v.channels[u]

        else:
            u = self._get_node(element, 'id')
            u_id = u.node_id
            for v in list(u.channels.keys()):
                # u's neighbors remove u
                del v.channels[u]

            # reset u's channels
            u.channels.clear()
            # remove u from graph
            del self.graph[u_id]

    def update_label(self, element, label) -> bool:
        """Update a label of the selected element (node or edge)."""
        if element['sort'] == Sort.Edge.name:
            u = self._get_node(element, 'source')
            v = self._get_node(element, 'target')

            if u.channels[v].name == label:
                return False

            u.channels[v].name = label
            v.channels[u].name = label

        else:
            if element['label'] == label:
                return False

            u = self._get_node(element, 'id')
            u.role.name = u.label = label

        return True

    def update_toggle(self, element, f1, f2, f3) -> bool: 
        if element['sort'] == Sort.Edge.name:
            u = self._get_node(element, 'source')
            v = self._get_node(element, 'target')

            u.channels[v].flags = [f1, f2, f3]
            v.channels[u].flags = [f1, f2, f3]

        return True

    def set_data_consumer_flag(self, element, is_data_consumer):
        """Set data consumer flag for node."""
        u = self._get_node(element, 'id')
        u.set_data_consumer(is_data_consumer)

    def set_node_label(self, element, text):
        """Set description for node."""

        print("Here we are entereing the set_node_label method")
        u = self._get_node(element, 'id')
        u.set_label(text)

        u.label = text 

    def set_node_description(self, element, text):
        """Set description for node."""
        u = self._get_node(element, 'id')
        u.set_description(text)

    def set_files(self, element, file_dict):
        """Set uploaded files in the node."""
        u = self._get_node(element, 'id')
        u.set_files(file_dict)

    def get_node_details(self, element):
        """Return details on node."""
        u = self._get_node(element, 'id')
        return u.get_node_details()

    def get_edge_details(self, element):
        """Return details on edge."""
        u = self._get_node(element, 'source')
        v = self._get_node(element, 'target')

        return u.get_edge_details(v)

    def get_func_tags(self, role, element):
        """Return function tags associated with a role."""
        u = self._get_node(element, 'source')
        v = self._get_node(element, 'target')

        if u.node_id == role:
            return u.get_func_tags(v)
        else:
            return v.get_func_tags(u)

    def set_func_tags(self, role, selected, func_tags, element):
        """Set function tags with a role."""
        u = self._get_node(element, 'source')
        v = self._get_node(element, 'target')

        if u.node_id == role:
            u.set_func_tags(v, func_tags, selected)
        else:
            v.set_func_tags(u, func_tags, selected)

    def build_schema(self, name):
        """Build schema."""
        self.name = name

        roles: set[Role] = set()
        channels: set[Channel] = set()

        for src in self.graph.values():
            roles.add(src.role)
            for dst, channel in src.channels.items():
                # update pair's label at the time of building a schema
                channel.pair = (src.label, dst.label)
                channels.add(channel)

        schema = Schema(self.name, self.description, roles, channels)
        return schema.build()

    def _get_node(self, element, key):
        node_id = element[key]
        node = self.graph[node_id]

        return node

    def build_from_template(self, template_str):
        """Build topology from template."""
        template = json.loads(template_str)

        if "roles" not in template or "channels" not in template:
            return None

        self.reset()

        for role in template["roles"]:
            cb_node = self.get_new_node()
            print(cb_node)
            element = cb_node["data"]

            if "description" in role:
                self.set_node_description(element, role["description"])

            if "isDataConsumer" in role:
                self.set_data_consumer_flag(element, role["isDataConsumer"])

            self.update_label(element, role["name"])

            u = self.graph[cb_node["data"]["id"]]
            cb_node = u.node_to_callback()

        for channel in template["channels"]:
            u_name, v_name = channel["pair"]

            u = self.find_node_by_label(u_name)
            v = self.find_node_by_label(v_name)
            cb_node_u = u.node_to_callback()
            cb_node_v = v.node_to_callback()

            element_u = cb_node_u["data"]
            element_v = cb_node_v["data"]

            if u_name == v_name:
                self.link([element_u])
            else:
                self.link([element_u, element_v])

            cb_edge = Node.edge_to_callback(u, v)

            self.update_label(cb_edge["data"], channel["name"])


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
