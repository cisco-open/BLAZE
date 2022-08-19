"""This defines callbacks of design pane."""

import base64
from doctest import master

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import ALL, Input, Output, State

import drag.global_obj as g
from drag.constants import DesignID, build_yaml 

from drag.layouts import dropdown_data_inputs, dropdown_models_inputs, dropdown_models_items, dropdown_data_items
import yaml 

toast_message = ""
toast_icon = ""


def get_callbacks(app): 



    @app.callback(
        Output(str(DesignID.DESIGN_INTERFACE), 'elements'),
        Output(str(DesignID.SCHEMA_PANE), 'children'),
        Output(str(DesignID.DOWNLOAD_FILE), 'data'),
        Input(str(DesignID.INPUT_EDIT_EDGE_LABEL), 'value'),
        Input(str(DesignID.BTN_ADD_MODEL), 'n_clicks'),
        Input(str(DesignID.BTN_ADD_DATA), 'n_clicks'),
        Input(str(DesignID.BTN_REMOVE_ELMT), 'n_clicks'),
        Input(str(DesignID.BTN_CONNECT_NODES), 'n_clicks'),
        Input(str(DesignID.BTN_BUILD_SCHEMA), 'n_clicks'),
        State(str(DesignID.DESIGN_INTERFACE), 'selectedNodeData'),
        State(str(DesignID.DESIGN_INTERFACE), 'selectedEdgeData'),
        State(str(DesignID.DESIGN_INTERFACE), 'elements'),
        State(str(DesignID.INPUT_DESIGN_TITLE), 'value'),
        State(str(DesignID.INPUT_YAML_TITLE), 'value'),
    )
    def update_elements(
        input_edge_label,
        btn_add_model,
        btn_add_data,
        btn_remove,
        btn_connect,
        btn_build,
        nodes,
        edges,
        elements,
        title,
        yaml_filename,
    ):
        """Update elements based on the selected buttion actions."""
        ctx = dash.callback_context
        if not ctx.triggered: return elements
        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]


        # COMPONENT 01 - Adding new Models 

        if prop_id == str(DesignID.BTN_ADD_DATA):
            print(f"(update_elements) > Adding new data...")
            return elements + [g.design.get_new_node("data")], get_schema(), None 

        # COMPONENT 02 - Adding new Datasets 

        elif prop_id == str(DesignID.BTN_ADD_MODEL):
            print(f"(update_elements) > Adding new model...")
            return elements + [g.design.get_new_node("model")], get_schema(), None 


        # COMPONENT 03 - Deleting Nodes (either models or datasets)

        elif prop_id == str(DesignID.BTN_REMOVE_ELMT):
            print(f"(update_elements) > Removing elements...")

            combined = None

            if nodes is None and edges is None:
                return elements
            elif nodes is None:
                combined = edges
            elif edges is None:
                combined = nodes
            else:
                combined = nodes + edges

            print(f"(update_elements) > Removing {combined}")

            g.design.remove_elements(combined)

            return g.design.get_nodes_edges(), get_schema(), None 

        # COMPONENT 04 - Connecting Nodes (all nodes must be connected)

        elif prop_id == str(DesignID.BTN_CONNECT_NODES):
            print(f"(update_elements) > Connecting elements...")

            if not g.design.link(nodes):
                return elements

            return g.design.get_nodes_edges(), get_schema(), None 


        # COMPONENT 05 - Selecting "Build" button 

        elif prop_id == str(DesignID.BTN_BUILD_SCHEMA):
            print(f"(update_elements) > Building YAML...")

            print(f"      - Title: {title}")
            print(f"      - Nodes: {g.design.get_nodes_edges()}")

            yaml_raw = build_yaml(title, g.design.get_nodes_edges()) 
            print(yaml_raw) 

            if yaml_filename is None or yaml_filename == "": 
                yaml_filename = "test"

            f_n = "yaml/" + yaml_filename + ".yaml"

            with open (f_n, mode="wt", encoding="utf-8") as file:
                yaml.dump(yaml_raw, file)
 
            return elements, get_schema(f_n), dcc.send_file(f_n, filename=yaml_filename)

        # COMPONENT 06 - Editing Node Labels 

        # elif prop_id == str(DesignID.INPUT_SELECT_ELEMENT):
        #     print(f"(update_elements) > Editing node label...")

        #     if nodes is None or len(nodes) != 1 or not g.design.update_label(
        #             nodes[0], input_node_label):
        #         return elements

        #     return g.design.get_nodes_edges()


        # # COMPONENT 07 - Editing Edge Labels 

        # elif prop_id == str(DesignID.INPUT_EDIT_EDGE_LABEL):
        #     print(f"(update_elements) > Editing edge label...")

        #     if edges is None or len(edges) != 1 or not g.design.update_label(
        #             edges[0], input_edge_label):
        #         return elements

        #     return g.design.get_nodes_edges()
        


        # None has been clicked
        return elements, get_schema(), None 

    



    # ========================================================================================= #

    @app.callback(Output(str(DesignID.TABS_DESIGN), 'active_tab'),
                Output(str(DesignID.TAB_NODE_MODEL_CONTENT), 'style'),
                Output(str(DesignID.TAB_NODE_DATA_CONTENT), 'style'),
                Output(str(DesignID.TAB_EDGE_CONTENT), 'style'),
                Input(str(DesignID.DESIGN_INTERFACE), 'selectedNodeData'),
                Input(str(DesignID.DESIGN_INTERFACE), 'selectedEdgeData'))
    def switch_tab(nodes, edges):
        print(f"(switch_tab) > Entered switch tab callback")
        """Switch a tab between role and channel."""
        display_on = {'display': 'block'}
        display_off = {'display': 'none'}

        if nodes is not None and len(nodes) == 1:

            (node_label, desc, type_node,
            filenames_in_node) = g.design.get_node_details(nodes[0])

            if type_node == "model": 
                print("turning on model tab")
                return str(DesignID.TAB_NODE_PROPERTY_VALUE), display_on, display_off, display_off
            else: 
                print("turning on data tab")
                return str(DesignID.TAB_NODE_PROPERTY_VALUE), display_off, display_on, display_off


        if edges is not None and len(edges) == 1:
            return str(DesignID.TAB_EDGE_PROPERTY_VALUE), display_off, display_off, display_on

        return "", display_off, display_off, display_off


    # ========================================================================================= #

    """ Callback for data - node """




    """ Callback for model - node """



    @app.callback(Input(str(DesignID.DESIGN_INTERFACE), 'selectedNodeData'),
                  dropdown_models_inputs
    )
    def dropdown_model_callback(*args):
        print(f"(dropdown_model_callback) > Entered model tab callback")

        nodes = args[0]

        ctx = dash.callback_context
        if nodes is None or len(nodes) != 1 or not ctx.triggered:
            return 

        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if "dropdown" in prop_id: 
            print(f"(update_dropdown) > Updating label of {nodes[0]}")
            button_id = prop_id.split("dropdown_")[-1]
            print(f"         replacing with {button_id}")
            g.design.update_label(nodes[0], button_id)
    

    @app.callback(Input(str(DesignID.DESIGN_INTERFACE), 'selectedNodeData'),
                dropdown_data_inputs
    )
    def dropdown_data_callback(*args):
        print(f"(dropdown_data_callback) > Entered model tab callback")

        nodes = args[0]

        ctx = dash.callback_context
        if nodes is None or len(nodes) != 1 or not ctx.triggered:
            return 

        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if "dropdown" in prop_id: 
            print(f"(update_dropdown) > Updating label of {nodes[0]}")
            button_id = prop_id.split("dropdown_")[-1]
            print(f"         replacing with {button_id}")
            g.design.update_label(nodes[0], button_id)
    
    

    @app.callback(Output(str(DesignID.INPUT_MODEL_DISPLAY_ELEMENT), 'value'),
                  Output(str(DesignID.TEXTAREA_MODEL_NODE_DESCRIPTION), 'value'),
                  Output(str(DesignID.INPUT_DATA_DISPLAY_ELEMENT), 'value'),
                  Output(str(DesignID.TEXTAREA_DATA_NODE_DESCRIPTION), 'value'),
                  Input('interval-component', 'n_intervals'),
                  Input(str(DesignID.DESIGN_INTERFACE), 'selectedNodeData'),
    )
    def display_label(n_intervals, nodes): 
        ctx = dash.callback_context
        if g is None or nodes is None or len(nodes) != 1 or not ctx.triggered:
            return "", "", "", "" 
        
        (node_label, desc, type_node,
        filenames_in_node) = g.design.get_node_details(nodes[0])
        print(f"type: {type_node}, label: {node_label}")
        if "Model" not in node_label and "Data" not in node_label: 
            #print(f"We have already sleected: {node_label}")
            print(f"Returning {node_label}, {master_dict[node_label]}")

            if type_node == "model": 
                return node_label, master_dict[node_label], "", "" 
            else: 
                return "", "", node_label, master_dict[node_label]

        elif type_node == "model": 
            print("Please sleect model from dataset")
            return "Please select a model from the dropdown...", "", "", ""
        else: 
            print("Please select datasetse from dropdown")
            return "", "", "Please select a dataset from the dropdown...", ""




    @app.callback(
        Output(str(DesignID.INPUT_EDIT_EDGE_LABEL), 'value'),
        Output(str(DesignID.TOGGLE_CUSTOM), 'value'),
        Output(str(DesignID.TOGGLE_BENCHMARK), 'value'),
        Output(str(DesignID.TOGGLE_COMPARISON), 'value'),
        Input(str(DesignID.INPUT_EDIT_EDGE_LABEL), 'value'),
        Input(str(DesignID.TOGGLE_CUSTOM), 'value'),
        Input(str(DesignID.TOGGLE_BENCHMARK), 'value'),
        Input(str(DesignID.TOGGLE_COMPARISON), 'value'),
        Input(str(DesignID.DESIGN_INTERFACE), 'selectedEdgeData'),
    )
    def display_edge_tab_content(new_label, toggle_custom, toggle_benchmark, toggle_comparison, edges):
        print(f"(display_edge_tab_content) > Entered edge tab callback w/ {new_label}")

        """Display content of edge tab."""
        if edges is None or len(edges) != 1:
            return '', False, False, False 



        label, desc, node_labels, flags = g.design.get_edge_details(edges[0])

        print(f"Current: {flags} vs Toggles: {toggle_custom} {toggle_benchmark} {toggle_comparison}")
        if toggle_custom or toggle_benchmark or toggle_comparison: 
            g.design.update_toggle(edges[0], toggle_custom, toggle_benchmark, toggle_comparison)

        print(f"Current label is {label}")

        if new_label == '': 
            return label, flags[0], flags[1], flags[2]

        options = [{
            'label': node_labels[0]['label'],
            'value': node_labels[0]['id']
        }]
        if node_labels[0] != node_labels[1]:
            options.append({
                'label': node_labels[1]['label'],
                'value': node_labels[1]['id']
            })
        g.design.update_label(edges[0], new_label)
        print(f"UPDATED LABEL w/ {new_label}")

        label, desc, node_labels, flags = g.design.get_edge_details(edges[0])
        return new_label, flags[0], flags[1], flags[2]




    # ========================================================================================= #




    @app.callback(Input(str(DesignID.TOGGLE_DATA_CONSUMER), 'value'),
                State(str(DesignID.DESIGN_INTERFACE), 'selectedNodeData'))
    def update_data_consumer_flag(toogle_value, nodes):
        """Update data consumer flag at the backend."""
        if nodes is None or len(nodes) != 1:
            return

        g.design.set_data_consumer_flag(nodes[0], toogle_value)


    @app.callback(
        Output(str(DesignID.LISTGROUP_FUNC_TAGS), 'children'),
        Input(str(DesignID.RADIOITEMS_ROLES_FOR_FUNC_TAGS), 'value'),
        State(str(DesignID.DESIGN_INTERFACE), 'selectedEdgeData'),
    )
    def load_func_tags(node, edges):
        """Load function tags associated with a node."""
        if node == '':
            return []

        func_tags_status = g.design.get_func_tags(node, edges[0])
        children = list()
        for i, (name, checked) in enumerate(func_tags_status.items()):
            func_tag = dbc.InputGroup(children=[
                dbc.InputGroupText(
                    dbc.Checkbox(id={
                        'type': str(DesignID.INPUTGROUP_CHECKBOX_FUNC_TAG),
                        'index': i
                    },
                                value=checked)),
                dbc.Input(id={
                    'type': str(DesignID.INPUTGROUP_INPUT_FUNC_TAG),
                    'index': i
                },
                        value=name,
                        disabled=True)
            ])
            children.append(dbc.ListGroupItem(func_tag))

        return children


    @app.callback(
        Input(str(DesignID.RADIOITEMS_ROLES_FOR_FUNC_TAGS), 'value'),
        Input({
            'type': str(DesignID.INPUTGROUP_CHECKBOX_FUNC_TAG),
            'index': ALL
        }, 'value'),
        State({
            'type': str(DesignID.INPUTGROUP_INPUT_FUNC_TAG),
            'index': ALL
        }, 'value'),
        State(str(DesignID.DESIGN_INTERFACE), 'selectedEdgeData'),
    )
    def update_func_tags_selection(node, selected, func_tags, edges):
        """Update function tag status."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return

        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if prop_id == str(DesignID.RADIOITEMS_ROLES_FOR_FUNC_TAGS):
            return

        g.design.set_func_tags(node, selected, func_tags, edges[0])

