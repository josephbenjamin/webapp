from dash import html, dcc
from data import prepare_data

df = prepare_data()  # Load the data once for reuse

app_layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
    children=[
        html.H1("Bank Rate Dashboard", style={"textAlign": "center"}),

        html.Div(
            style={"display": "flex", "flexDirection": "row"},
            children=[
                # Left-aligned div with RangeSlider
                html.Div(
                    style={"width": "20%", "padding": "10px", "borderRight": "1px solid #ddd"},
                    children=[
                        html.Label("Select Date Range:"),
                        dcc.RangeSlider(
                            id="date-range-slider",
                            min=0,
                            max=len(df) - 1,
                            step=1,
                            value=[0, len(df) - 1],
                            marks={
                                0: str(df.index[0].date()),
                                len(df) - 1: str(df.index[-1].date()),
                            },
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                        html.Div(id="selected-dates", style={"marginTop": "10px"}),
                        html.Label("Select Series:"),
                        dcc.Dropdown(
                            id="series-dropdown",
                            options=[
                                {"label": "Bank Rate", "value": "Rate"},
                                {"label": "Random Walk", "value": "Random Walk"},
                                {"label": "Both", "value": "Both"},
                            ],
                            value="Both",
                            clearable=False,
                        ),
                    ],
                ),
                # Right-aligned graph
                html.Div(
                    style={"flexGrow": "1", "padding": "10px"},
                    children=[
                        dcc.Graph(id="time-series-chart"),
                    ],
                ),
            ],
        ),
    ],
)
