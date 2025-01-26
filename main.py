from app import app
from layout import app_layout
import callbacks  # Registers callbacks

# Set the app layout
app.layout = app_layout

if __name__ == "__main__":
    app.run_server(debug=True)
