import random
import numpy as np
import matplotlib.pyplot as plt

def generate_canopy(height, width):
    canopy = np.zeros((height, width))
    return canopy

def draw_the_map(canopy):
    #  a map with value from -40 to 40 (degree)
    plt.imshow(canopy, cmap="autumn", interpolation="none", vmin=-40, vmax=40)
    plt.title(
        "COMP1005 Assignment Canopy Simulation",
        pad=20,
        fontsize=16,
        fontweight='bold',
        fontfamily='serif',
        loc='center'
    )
    # remove axis value bc wer making a map
    plt.xticks([])  
    plt.yticks([])
    # for the side bar later etc...
    plt.colorbar(label="Heats")
    plt.show()

#  this is the func that call all other stuffs to get things done
def main():
    # define the w and h parameters
    height, width = 200, 200
    canopy = generate_canopy(height, width)
    draw_the_map(canopy)

# This runs the Python file (in case u dont know type python3 file name)
if __name__ == "__main__":
    main()