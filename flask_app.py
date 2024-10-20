from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

@app.route('/quadrants', methods=['GET'])
def quadrants():
    # Get x_pos and z_pos from query parameters
    x_pos = request.args.get('x_pos')
    z_pos = request.args.get('z_pos')

    if not x_pos or not z_pos:
        return {"error": "Please provide both x_pos and z_pos"}, 400

    try:
        # Run the fortress.py file with x_pos and z_pos as arguments
        subprocess.run(['python', 'fortress.py', x_pos, z_pos], check=True)

        # Return the generated image
        return send_file('fortress_plot.png', mimetype='image/png')
    except subprocess.CalledProcessError as e:
        return {"error": "Failed to generate image from fortress.py", "details": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
