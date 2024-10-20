from flask import Flask, request, send_file
import subprocess
from quadrants import locate_quadrants # Import the function from quadrants.py

app = Flask(__name__)

@app.route('/quadrants', methods=['GET'])
def quadrants():
    # Get x_pos and z_pos from query parameters
    x_pos = request.args.get('x_pos')
    z_pos = request.args.get('z_pos')
    if not x_pos or not z_pos:
        return {"error": "Please provide both x_pos and z_pos"}, 400

    try:
        # Run the locate_quadrants function with x_pos and z_pos amd output_file as arguments
        img = locate_quadrants(float(x_pos), float(z_pos))

        # Return the generated image
        response = send_file(img, mimetype='image/png', as_attachment=False, download_name='quadrants_plot.png')
        return response;
    except subprocess.CalledProcessError as e:
        return {"error": "Failed to generate image from quadrants.py", "details": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
