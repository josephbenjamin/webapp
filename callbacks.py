from dash import Input, Output
from app import app
from data import prepare_data
import plotly.graph_objects as go

df = prepare_data()  # Load the data once for reuse

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