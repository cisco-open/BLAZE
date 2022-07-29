import dash
import dash_bootstrap_components as dbc

from aski.dash_files.app_constants import * 

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,
											   FONT_QUICKSAND])
app.css.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True