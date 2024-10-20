from flask import Flask, request, send_file
import subprocess
from quadrants import locate_quadrants  # Import the function from quadrants.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes and origins

@app.route('/quadrants', methods=['GET'])
def quadrants():
    # Get x_pos and z_pos from query parameters
    x_pos = request.args.get('x_pos')
    z_pos = request.args.get('z_pos')

    # Check if x_pos and z_pos are provided
    if not x_pos or not z_pos:
        return {"error": "Please provide both x_pos and z_pos"}, 400

    try:
        # Convert x_pos and z_pos to floats
        x_pos = float(x_pos)
        z_pos = float(z_pos)
    except ValueError:
        # If conversion to float fails, return an error
        return {"error": "x_pos and z_pos must be valid numbers"}, 400

    try:
        # Run the locate_quadrants function with x_pos and z_pos
        img = locate_quadrants(x_pos, z_pos)

        # Return the generated image
        response = send_file(img, mimetype='image/png', as_attachment=False, download_name='quadrants_plot.png')
        return response
    except subprocess.CalledProcessError as e:
        return {"error": "Failed to generate image from quadrants.py", "details": str(e)}, 500
    except Exception as e:
        # General error handling
        return {"error": "An unexpected error occurred", "details": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
