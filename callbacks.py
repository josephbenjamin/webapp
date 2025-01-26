from dash import Input, Output
from app import app
from data import prepare_data
import plotly.graph_objects as go

df = prepare_data()

@app.callback(
    Output("selected-dates", "children"),
    Output("time-series-chart", "figure"),
    Input("date-range-slider", "value"),
    Input("series-dropdown", "value")
)

def update_graph(date_range, selected_series):
    # Extract start and end indices from the slider
    start_idx, end_idx = date_range
    start_date = df.index[start_idx]
    end_date = df.index[end_idx]

    # Format dates
    formatted_start_date = start_date.strftime('%d %b %Y')
    formatted_end_date = end_date.strftime('%d %b %Y')

    # Update the selected date range label
    date_range_label = f"Selected Range: {formatted_start_date} to {formatted_end_date}"

    # Create the Plotly figure
    fig = go.Figure()
    if selected_series in ["Rate", "Both"]:
        fig.add_trace(go.Scatter(
            x=df.index[start_idx:end_idx + 1],
            y=df["Rate"].iloc[start_idx:end_idx + 1],
            mode="lines",
            name="Bank Rate",
            line=dict(color="blue"),
        ))
    if selected_series in ["Random Walk", "Both"]:
        fig.add_trace(go.Scatter(
            x=df.index[start_idx:end_idx + 1],
            y=df["Random Walk"].iloc[start_idx:end_idx + 1],
            mode="lines",
            name="Random Walk",
            line=dict(color="orange", dash="dot"),
        ))

    fig.update_layout(
        title="Bank Rate and Random Walk Over Time",
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_white",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        legend=dict(x=0.01, y=0.99),
    )

    return date_range_label, fig


# Code to allow the user to switch the attribute 'data-bs-theme' from 'dark' to 'light' locally
app.clientside_callback(
    """
    function(switchOn) {
        document.documentElement.setAttribute('data-bs-theme', switchOn ? 'dark' : 'light');
        return window.dash_clientside.no_update;
    }
    """,
    Output("theme-toggle", "value"),  # A dummy Output just to register the callback
    Input("theme-toggle", "value"),
)

@app.callback(
    Output("date-range-slider", "marks"),  # Dynamically update marks
    Input("date-range-slider", "value"),
)
def update_tooltip(value):
    # Extract start and end indices from the slider
    start_idx, end_idx = value

    # Format dates for the tooltips
    marks = {
        start_idx: df.index[start_idx].strftime('%d %b %Y'),
        end_idx: df.index[end_idx].strftime('%d %b %Y'),
    }

    return marks