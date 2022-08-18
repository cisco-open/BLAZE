"""This implements layouts for design pane."""

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dcc, html

from dash.dependencies import Input 
from layouts_gen import get_schema, get_title, get_cytoscape, get_warning, get_buttons, get_cyto_card
from constants import *

CREAM = "#FFE5B4"

"""
Design_layout is the element that stitches all the components together 
"""

design_layout = html.Div([
    
    dbc.Row([
        get_title(), 
        dbc.Col([
            get_cytoscape(), 
            get_warning(), 
        ], width=8), 
        dbc.Col([
            get_buttons(), 
            get_cyto_card(), 
            html.Div(id=str(DesignID.SCHEMA_PANE), children=[get_schema()]), 
        ], width=4),
        dcc.Download(id=str(DesignID.DOWNLOAD_FILE)),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0,
        )
    ])
], 
style={'background-color': '#222222', 'height': '60rem', 'width': '100%', 'padding':'1rem'})
