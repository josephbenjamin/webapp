from dash import dcc, html
import dash_bootstrap_components as dbc
from data import prepare_data

df = prepare_data()  # Load the data once for reuse

# define the colour switch
color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch( id="theme-toggle", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)

app_layout = html.Div(
    id="app-container",  # ID for setting Bootstrap's data-bs-theme attribute
    children=[
        dbc.Container(
            [
                # Header Row
                dbc.Row(
                    [
                        dbc.Col(
                            html.H1(
                                "Bank Rate Dashboard",
                                className="text-left",  # Align title to the left
                            ),
                        ),
                    ],
                    className="mb-4",  # Add spacing below the header row
                ),
                # Theme Toggle Row
                dbc.Row(
                    [
                        dbc.Col(
                            # dbc.Switch(
                            #     id="theme-toggle",
                            #     label="Dark Mode",
                            # ),
                            # width=3,
                            color_mode_switch

                        ),
                    ],
                    className="mb-4",  # Add spacing below the toggle row
                ),
                # Inputs and Output Layout
                dbc.Row(
                    [
                        # Inputs in a Card
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Inputs", className="bg-body-secondary"),  # Theme-aware header
                                    dbc.CardBody(
                                        [
                                            html.Label(
                                                "Select Date Range:",
                                                className="form-label",  # Bootstrap's form label class
                                            ),
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
                                                # tooltip={"placement": "top", "always_visible": False},
                                                # tooltip={"always_visible": False}

                                            ),
                                            html.Div(
                                                id="selected-dates",
                                                className="mt-3",  # Add margin above
                                            ),
                                            html.Label(
                                                "Select Series:",
                                                className="form-label mt-3",  # Theme-aware label
                                            ),
                                            dbc.Select(
                                                id="series-dropdown",
                                                options=[
                                                    {"label": "Bank Rate", "value": "Rate"},
                                                    {"label": "Random Walk", "value": "Random Walk"},
                                                    {"label": "Both", "value": "Both"},
                                                ],
                                                value="Both",
                                                className="form-select",  # Theme-aware dropdown
                                            ),
                                        ]
                                    ),
                                ],
                                className="bg-body-primary shadow-sm",  # Theme-aware card
                            ),
                            width=3,
                        ),
                        # Output Plot in a Card
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "Outputs",
                                        className="bg-body-secondary",  # Theme-aware header
                                    ),
                                    dbc.CardBody(dcc.Graph(id="time-series-chart")),
                                ],
                                className="bg-body-primary shadow-sm",  # Theme-aware card
                            ),
                            width=9,
                        ),
                    ]
                ),
            ],
            fluid=True,
        ),
    ],
)
