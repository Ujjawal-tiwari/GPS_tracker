import json
from flask import Flask, render_template
from flask import send_from_directory

app = Flask(__name__)

# Function to read location data from a JSON file
def read_location_data():
    with open("received_data.json", "r") as file:
        return json.load(file)

@app.route('/')
def index():
    # Get location data from the JSON file
    location_data = read_location_data()

    # Extract coordinates for map display
    coordinates = [(loc['lat'], loc['lon']) for loc in location_data if 'lat' in loc and 'lon' in loc]

    # Render the template and pass the coordinates
    return render_template('index.html', coordinates=coordinates)

@app.route('/leaflet.js')
def leaflet_js():
    # Serve the Leaflet.js library (usually you'd use a CDN, but to demonstrate, we're serving locally)
    return send_from_directory('static', 'leaflet.js')

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
