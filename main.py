import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

def generate_random_walk(start, size, stepsize):
    """Generate a random walk data series."""
    np.random.seed(41)  # Set seed for reproducibility
    steps = np.random.choice([-stepsize, stepsize], size=size)  # Random steps: -1 or 1
    walk = np.cumsum(steps) + start  # Cumulative sum starting from 'start'
    return walk

def load_data():
    # Load the bank rate data
    df = pd.read_csv('data/bankrate.csv')

    df['Date'] = pd.to_datetime(df['Date Changed'])

    # Set 'Date' as the index
    df.set_index('Date', inplace=True)

    # Create a full date range (including missing days)
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')

    # Reindex the DataFrame to include the full date range
    df = df.reindex(full_date_range)
    df.index.name = 'Date'  # Name the index as 'Date'

    # Forward-fill the bank rate data
    df['Rate'] = df['Rate'].ffill()

    # Generate random walk data for the full date range
    random_walk = generate_random_walk(start=df['Rate'].iloc[0], stepsize=0.05, size=len(df))
    df['Random Walk'] = random_walk  # Add random walk to DataFrame

    # Print DataFrame to verify
    print(df)
    return df

def create_mpl_chart():
    df = load_data()

    # Plot bank rate and random walk
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Rate'], linestyle = '-', label='Bank Rate')
    ax.plot(df.index, df['Random Walk'], linestyle='-', label='Random Walk')

    # Add titles, labels, and legend
    ax.set_title('Bank Rate and Random Walk Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel(None)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    # Show the plot
    plt.show()

def create_plotly_chart():
    df = load_data()
    # Create a Plotly figure
    fig = go.Figure()

    # Add the Bank Rate line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Rate'],
        mode='lines',
        name='Bank Rate',
        line=dict(color='blue')
    ))

    # Add the Random Walk line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Random Walk'],
        mode='lines',
        name='Random Walk',
        line=dict(color='orange', dash='dot')
    ))

    # Update layout for titles, labels, and grid
    fig.update_layout(
        title='Bank Rate and Random Walk Over Time',
        xaxis_title='Date',
        yaxis_title=None,
        legend=dict(x=0.01, y=0.99),
        template='plotly_white',
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    # Show the Plotly figure
    fig.show()

def main():
    create_mpl_chart()
    create_plotly_chart()

# Entry point for the script
if __name__ == '__main__':
    main()