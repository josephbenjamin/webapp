import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba

def is_light_color(color):
    """
    Determine if a given color is light based on its luminance.
    Luminance is calculated using the relative luminance formula:
    L = 0.2126*R + 0.7152*G + 0.0722*B

    Parameters:
    color : str or tuple
        Color in any Matplotlib-compatible format (e.g., named color, hex, RGBA).

    Returns:
    bool
        True if the color is light, False otherwise.
    """
    rgba = to_rgba(color)  # Convert to RGBA
    r, g, b = rgba[:3]     # Extract RGB
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance > 0.5

def annotate_line_end(ax, line, offset=0.02):
    """
    Annotates the end of a line on a plot with the latest value.

    Parameters:
    ax : matplotlib Axes object
        The axes on which the annotation will be drawn.
    line : matplotlib Line2D object
        The line to annotate.
    offset : float
        Horizontal offset for the annotation, in axis fraction.
    """
    x_data, y_data = line.get_xdata(), line.get_ydata()
    if len(x_data) == 0 or len(y_data) == 0:
        return  # Skip if there's no data

    latest_x = x_data[-1]
    latest_y = y_data[-1]
    line_color = line.get_color()

    # Determine text color based on background brightness
    text_color = 'black' if is_light_color(line_color) else 'white'

    # Annotate the last value
    bbox_props = {
        "boxstyle": "round,pad=0.3",
        "edgecolor": 'black',
        "facecolor": line_color,
        "alpha": 1
    }
    ax.text(
        latest_x + offset * (ax.get_xlim()[1] - ax.get_xlim()[0]),
        latest_y,
        f"{latest_y:.2f}",
        fontsize=10,
        color=text_color,
        bbox=bbox_props,
        verticalalignment='center',
    )

    # Adjust the plot limits to fit the annotation
    # ax.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1] + offset * (ax.get_xlim()[1] - ax.get_xlim()[0]))


if __name__ == '__main__':
    # Example usage
    np.random.seed(42)  # For reproducibility
    plt.style.use('classic')
    fig, ax = plt.subplots(figsize=(12, 8), layout='constrained')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Generate random time-series data
    num_series = 25
    num_points = 300
    x = np.linspace(0, 10, num_points)

    for i in range(num_series):
        # Create a random walk for each series
        y = np.cumsum(np.random.normal(0, 0.5, num_points))
        line, = ax.plot(x, y, label=f"Series {i + 1}")
        annotate_line_end(ax, line)

    # ax.legend()
    ax.set_title('A Random Plot')
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.yaxis.grid(True, linestyle='-', color='gray', alpha=0.5)
    ax.xaxis.grid(False)  # Disable vertical gridlines
    # plt.tight_layout()
    plt.show()
