import pandas as pd
import matplotlib.pyplot as plt


def main():
    # Load the CSV file
    df = pd.read_csv('data/bankrate.csv')

    # Convert the 'Date Changed' column to datetime
    df['Date'] = pd.to_datetime(df['Date Changed'])

    # Print the DataFrame for verification
    print(df)

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Rate'], marker='o', label='Bank Rate')  # Added label for legend

    # Add titles and labels
    ax.set_title('Interest Rate Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate (%)')

    # Add grid and legend
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    # Display the plot
    plt.show()


# Entry point for the script
if __name__ == '__main__':
    main()