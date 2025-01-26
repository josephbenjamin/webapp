from dash import Input, Output, State, Patch
from app import app
from data import prepare_data
import plotly.graph_objects as go
import plotly.io as pio
from dash_bootstrap_templates import load_figure_template, template_from_url

df = prepare_data()

@app.callback(
    Output("selected-dates", "children"),
    Output("time-series-chart", "figure"),
    Input("date-range-slider", "value"),
    Input("series-dropdown", "value"),
    State("theme-toggle", "value")
)

def update_graph(date_range, selected_series, theme_toggle):
    #  handle dark / light templates
    template = "bootstrap_dark" if theme_toggle else "bootstrap"

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

    # load and apply the relevant figure template to align with the chosen webapp theme
    themes = [
        "bootstrap",
        "cerulean",
        "cosmo",
        "cyborg",
        "darkly",
        "flatly",
        "journal",
        "litera",
        "lumen",
        "lux",
        "materia",
        "minty",
        "morph",
        "pulse",
        "quartz",
        "sandstone",
        "simplex",
        "sketchy",
        "slate",
        "solar",
        "spacelab",
        "superhero",
        "united",
        "vapor",
        "yeti",
        "zephyr",
    ]

    dark_themes = [t + "_dark" for t in themes]
    all_templates = themes + dark_themes
    all_templates.sort()
    load_figure_template("all")

    fig.update_layout(
        title="Bank Rate and Random Walk Over Time",
        xaxis_title="Date",
        yaxis_title="Value",
        template=template,
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


# Speed up the update of figure templates by using Patch()
@app.callback(
    Output("time-series-chart", "figure", allow_duplicate=True),
    Input("theme-toggle", "value"),
    prevent_initial_call=True
)

def update_template(theme_toggle):
    print(f"update_template() triggered. theme_toggle: {theme_toggle}")
    theme_name = 'bootstrap' # manual update for now, rather than linked to global variable
    template_name = theme_name + "_dark" if theme_toggle else theme_name
    load_figure_template("all") # ensure plotly is updated with all the available names ? (tentative)
    patched_figure = Patch()
    # When using Patch() to update the figure template, you must use the figure template dict
    # from plotly.io  and not just the template name
    patched_figure["layout"]["template"] = pio.templates[template_name]
    return patched_figure
