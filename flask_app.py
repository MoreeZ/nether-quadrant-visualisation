from flask import Flask, request, send_file
import subprocess
import uuid
import os
from quadrants import locate_quadrants  # Import the function from fortress.py

app = Flask(__name__)

@app.route('/quadrants', methods=['GET'])
def quadrants():
    # Get x_pos and z_pos from query parameters
    x_pos = request.args.get('x_pos')
    z_pos = request.args.get('z_pos')
    output_file = f"plot_{uuid.uuid4()}.png"
    if not x_pos or not z_pos:
        return {"error": "Please provide both x_pos and z_pos"}, 400

    try:
        # Run the locate_quadrants function with x_pos and z_pos amd output_file as arguments
        locate_quadrants(x_pos, z_pos, output_file)

        # Return the generated image
        response = send_file(output_file, mimetype='image/png')
        os.remove(output_file)
        return response;
    except subprocess.CalledProcessError as e:
        return {"error": "Failed to generate image from quadrants.py", "details": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
