# Import Flask modules
from flask import Flask, request, jsonify

# Create a Flask app instance
app = Flask(__name__)

# Define a route for the home ("/") URL
@app.route("/")
def index():
    return jsonify("Flask is working") # Returns a JSON response when accessed

# Define a route "/func" that accepts POST requests
@app.route("/func", methods=["POST"])
def func():
    return jsonify("Write API function here") # Placeholder response for a POST request

# Run the Flask app when the script is executed
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 
    # host="0.0.0.0" allows external access (from other devices in the network)
    # port=8000 sets the server to run on port 8000


