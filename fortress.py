import sys
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

QUADRANT_SIZE = 432
QUADRANT_GAP = 64

# Hardcoded output file
OUTPUT_FILE = "fortress_plot.png"

def locate_fortress(x, z):
    # Calculate the quadrant of the input position
    x_quadrant = math.floor(x / QUADRANT_SIZE)
    z_quadrant = math.floor(z / QUADRANT_SIZE)

    # Calculate the starting points of the quadrant
    x_quad_start = QUADRANT_SIZE * x_quadrant
    z_quad_start = QUADRANT_SIZE * z_quadrant

    # Calculate the ending points of the quadrant (considering the gap)
    x_quad_end = x_quad_start + QUADRANT_SIZE - QUADRANT_GAP
    z_quad_end = z_quad_start + QUADRANT_SIZE - QUADRANT_GAP

    print(f"FROM X: {x_quad_start}, Z: {z_quad_start}")
    print(f"TO X: {x_quad_end}, Z: {z_quad_end}")

    # Plot the Cartesian plane with the quadrants and the input point
    plot_quadrant_and_position(x, z, x_quad_start, z_quad_start, x_quad_end, z_quad_end)

def plot_quadrant_and_position(x, z, x_quad_start, z_quad_start, x_quad_end, z_quad_end):
    # Increase the figure size (width=10 inches, height=10 inches)
    fig, ax = plt.subplots(figsize=(10, 10))

    # Define the 9 quadrants (3x3 grid) centered on the input quadrant
    for i in range(-1, 2):  # Three rows: above, centered, below
        for j in range(-1, 2):  # Three columns: left, centered, right
            x_offset = x_quad_start + i * QUADRANT_SIZE
            z_offset = z_quad_start + j * QUADRANT_SIZE
            # Plot the surrounding quadrants as rectangles
            rect = plt.Rectangle((x_offset, z_offset), QUADRANT_SIZE, QUADRANT_SIZE,
                                 linewidth=1, edgecolor='blue', facecolor='none')
            ax.add_patch(rect)

            # Add quadrant edge labels (at the corners of each quadrant)
            ax.text(x_offset, z_offset, f'({x_offset}, {z_offset})', fontsize=8, verticalalignment='top')
            ax.text(x_offset + QUADRANT_SIZE, z_offset, f'({x_offset + QUADRANT_SIZE}, {z_offset})', fontsize=8, verticalalignment='top', horizontalalignment='right')
            ax.text(x_offset, z_offset + QUADRANT_SIZE, f'({x_offset}, {z_offset + QUADRANT_SIZE})', fontsize=8, verticalalignment='bottom')
            ax.text(x_offset + QUADRANT_SIZE, z_offset + QUADRANT_SIZE, f'({x_offset + QUADRANT_SIZE}, {z_offset + QUADRANT_SIZE})', fontsize=8, verticalalignment='bottom', horizontalalignment='right')

            # Calculate the inner "green" region for each quadrant
            inner_x_start = x_offset
            inner_z_start = z_offset
            inner_x_end = x_offset + QUADRANT_SIZE - QUADRANT_GAP
            inner_z_end = z_offset + QUADRANT_SIZE - QUADRANT_GAP

            # Highlight the "from" and "to" region inside each quadrant and fill it with light green
            rect_inner = plt.Rectangle((inner_x_start, inner_z_start), 
                                       inner_x_end - inner_x_start, inner_z_end - inner_z_start,
                                       linewidth=1, edgecolor='green', facecolor='lightgreen', linestyle='--')
            ax.add_patch(rect_inner)

    # Plot the input point as a red dot and annotate it
    ax.plot(x, z, 'ro', label=f"Input Position ({x}, {z})")
    ax.text(x, z, f'({x}, {z})', fontsize=10, verticalalignment='bottom', horizontalalignment='center', color='red')

    # Set limits for the plot based on the surrounding quadrants, ensuring the red dot is centered
    x_margin = QUADRANT_SIZE * 1.5
    z_margin = QUADRANT_SIZE * 1.5
    ax.set_xlim(x - x_margin, x + x_margin)
    ax.set_ylim(z - z_margin, z + z_margin)

    # Flip the Z-axis (so that negative is on top and positive is at the bottom)
    ax.invert_yaxis()

    # Set equal aspect ratio to make the chart square
    ax.set_aspect('equal')

    # Hide default ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Add grid lines and labels
    ax.grid(True)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Z Coordinate')  # Rename Y to Z
    ax.set_title('Nether Fortress Spawning Quadrants')

    # Create a legend
    fortress_patch = mpatches.Patch(color='lightgreen', label='Possible Fortress Spawning Points')
    player_dot = Line2D([0], [0], marker='o', color='w', label='Player Position', markerfacecolor='red', markersize=8)
    ax.legend(handles=[fortress_patch, player_dot], loc='upper left')

    # Save the plot as an image file
    plt.savefig(OUTPUT_FILE, bbox_inches='tight')
    print(f"Plot saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fortress.py <x_position> <z_position>")
    else:
        try:
            x = float(sys.argv[1])
            z = float(sys.argv[2])
            locate_fortress(x, z)
        except ValueError:
            print("Please provide valid numerical inputs for x and z.")
