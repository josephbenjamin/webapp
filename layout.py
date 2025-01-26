from dash import dcc, html
import dash_bootstrap_components as dbc
from data import prepare_data

# Load data once for reuse
df = prepare_data()

# Define Header
header = dbc.Row(
    [
        dbc.Col(
            html.H1(
                "Bank Rate Dashboard",
                className="text-left",
            )
        ),
    ],
    className="mb-4",
)

# Define Theme Toggle
color_mode_switch = dbc.Row(
    [
        dbc.Col(
            html.Span(
                [
                    dbc.Label(className="fa fa-sun", html_for="switch"),
                    dbc.Switch(
                        id="theme-toggle",
                        value=True,
                        className="d-inline-block ms-1",
                        persistence=True,
                    ),
                    dbc.Label(className="fa fa-moon", html_for="switch"),
                ]
            ),
        ),
    ],
    className="mb-4",
)

# Define Inputs Card
inputs_card = dbc.Card(
    [
        dbc.CardHeader("Inputs", className="bg-body-secondary"),
        dbc.CardBody(
            [
                html.Label("Select Date Range:", className="form-label"),
                dcc.RangeSlider(
                    id="date-range-slider",
                    min=0,
                    max=len(df) - 1,
                    step=1,
                    value=[0, len(df) - 1],
                    marks={
                        i: (df.index[i].strftime('%d %b %Y') if i in [0, len(df) - 1] else "")
                        for i in range(len(df))
                    },
                ),
                html.Div(id="selected-dates", className="mt-3"),
                html.Label("Select Series:", className="form-label mt-3"),
                dbc.Select(
                    id="series-dropdown",
                    options=[
                        {"label": "Bank Rate", "value": "Rate"},
                        {"label": "Random Walk", "value": "Random Walk"},
                        {"label": "Both", "value": "Both"},
                    ],
                    value="Both",
                    className="form-select",
                ),
            ]
        ),
    ],
    className="bg-body-primary shadow-sm",
)

# Define Output Card
output_card = dbc.Card(
    [
        dbc.CardHeader("Outputs", className="bg-body-secondary"),
        dbc.CardBody(dcc.Graph(id="time-series-chart")),
    ],
    className="bg-body-primary shadow-sm",
)

# Define the overall layout
app_layout = html.Div(
    id="app-container",
    children=[
        dbc.Container(
            [
                header,
                color_mode_switch,
                dbc.Row(
                    [
                        dbc.Col(inputs_card, width=4),  # Inputs on the left
                        dbc.Col(output_card, width=7),  # Outputs on the right
                    ]
                ),
            ],
            fluid=True,
        ),
    ],
)
