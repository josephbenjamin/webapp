from dash import Dash

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Expose the server for deployment