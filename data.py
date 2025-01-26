import pandas as pd
import numpy as np

def generate_random_walk(start, size, stepsize):
    """Generate a random walk data series."""
    np.random.seed(41)  # Set seed for reproducibility
    steps = np.random.choice([-stepsize, stepsize], size=size)
    walk = np.cumsum(steps) + start
    return walk

def prepare_data():
    """Prepare the data for the application."""
    # Load the bank rate data
    df = pd.read_csv('data/bankrate.csv')

    df['Date'] = pd.to_datetime(df['Date Changed'], format='%d %b %y')
    df.set_index('Date', inplace=True)

    # Create a full date range and reindex
    full_date_range = pd.date_range(start=df.index.min(), end=pd.Timestamp.today(), freq='D')
    df = df.reindex(full_date_range)
    df.index.name = 'Date'

    # Forward-fill missing data
    df['Rate'] = df['Rate'].ffill()

    # Generate random walk
    df['Random Walk'] = generate_random_walk(start=df['Rate'].iloc[0], stepsize=0.05, size=len(df))
    return df
