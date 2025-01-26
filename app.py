from dash import Dash, Input, Output
import dash_bootstrap_components as dbc

# Initialize the app with an initial theme
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP]
           )
server = app.server
