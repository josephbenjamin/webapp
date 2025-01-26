from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def generate_random_walk(start, size, stepsize):
    """Generate a random walk data series."""
    np.random.seed(41)  # Set seed for reproducibility
    steps = np.random.choice([-stepsize, stepsize], size=size)
    walk = np.cumsum(steps) + start
    return walk

def prepare_data():
    # Load the bank rate data
    df = pd.read_csv('data/bankrate.csv')

    df['Date'] = pd.to_datetime(df['Date Changed'], format='%d %b %y')
    df.set_index('Date', inplace=True)

    # Create a full date range and reindex
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(full_date_range)
    df.index.name = 'Date'

    # Forward-fill missing data
    df['Rate'] = df['Rate'].ffill()

    # Generate random walk
    df['Random Walk'] = generate_random_walk(start=df['Rate'].iloc[0], stepsize=0.05, size=len(df))

    return df

def create_dash():
    df = prepare_data()
    app = Dash(__name__)

    app.layout = html.Div(
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

    # Callback to update the date range display and chart
    @app.callback(
        [Output("selected-dates", "children"), Output("time-series-chart", "figure")],
        [Input("date-range-slider", "value"), Input("series-dropdown", "value")],
    )
    def update_graph(date_range, selected_series):
        start_idx, end_idx = date_range
        start_date = df.index[start_idx]
        end_date = df.index[end_idx]
        filtered_df = df.loc[start_date:end_date]

        # Update date range label
        date_range_label = f"Selected Range: {start_date.date()} to {end_date.date()}"

        # Create the plotly figure
        fig = go.Figure()
        if selected_series in ["Rate", "Both"]:
            fig.add_trace(go.Scatter(
                x=filtered_df.index,
                y=filtered_df["Rate"],
                mode="lines",
                name="Bank Rate",
                line=dict(color="blue")
            ))
        if selected_series in ["Random Walk", "Both"]:
            fig.add_trace(go.Scatter(
                x=filtered_df.index,
                y=filtered_df["Random Walk"],
                mode="lines",
                name="Random Walk",
                line=dict(color="orange", dash="dot")
            ))

        fig.update_layout(
            title="Bank Rate and Random Walk Over Time",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_white",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            legend=dict(x=0.01, y=0.99)
        )

        return date_range_label, fig

    app.run_server(debug=True)

if __name__ == "__main__":
    create_dash()
