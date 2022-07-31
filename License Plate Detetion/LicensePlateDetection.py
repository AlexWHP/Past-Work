""" Using image processing methods we are able to detect license plates of vehicles that are clearly displayed. Some sample 
    plates are provided which are able to be accurately detected using the methods below. Excluding the initial read of the
    image and output using Matplotlib """

import sys
from pathlib import Path

from matplotlib import pyplot
from matplotlib.patches import Rectangle

# Functions
from ImageProcessing import *

def main():

    command_line_arguments = sys.argv[1:]

    SHOW_DEBUG_FIGURES = True

    # Default input image filename
    input_filename = "numberplate1.png"

    if command_line_arguments != []:
        input_filename = command_line_arguments[0]
        SHOW_DEBUG_FIGURES = False

    output_path = Path("output_images")
    if not output_path.exists():
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)

    output_filename = output_path / Path(input_filename.replace(".png", "_output.png"))
    if len(command_line_arguments) == 2:
        output_filename = Path(command_line_arguments[1])


    # Read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(input_filename)

    # Setup the plots for intermediate results
    fig1, axs1 = pyplot.subplots(2, 2)

    # Conversion to Greyscale
    px_array = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    px_array = scaleTo0And255AndQuantize(px_array, image_width, image_height)
    original = list(px_array)
    axs1[0, 0].set_title('Contrast Stretching')
    axs1[0, 0].imshow(px_array, cmap='gray')

    # Contrast Stretching
    px_array = computeStandardDeviationImage5x5(px_array, image_width, image_height)
    px_array = scaleTo0And255AndQuantize(px_array, image_width, image_height)
    axs1[0, 1].set_title('Standard Deviation')
    axs1[0, 1].imshow(px_array, cmap='gray')

    # Threshholding
    threshold_value = 150
    px_array = computeThresholdGE(px_array, threshold_value, image_width, image_height)

    # Morphological Operations
    for i in range(4):
        px_array = computeDilation8Nbh3x3FlatSE(px_array, image_width, image_height)
    for i in range(4):
        px_array = computeErosion8Nbh3x3FlatSE(px_array, image_width, image_height)
    axs1[1, 0].set_title('Binary Close')
    axs1[1, 0].imshow(px_array, cmap='gray')

    # Connected Componenet Analysis
    # - Find the largest label
    # - Get the coordinates of the labels corners
    # - Return the label that produces a ratio of 1.5 to 5 
    px_array, labels = computeConnectedComponentLabeling(px_array, image_width, image_height)
    bbox_min_x, bbox_max_x, bbox_min_y, bbox_max_y = computeBestBoxConnectedComponent(px_array, image_width, image_height, labels)

    # Draw a bounding box as a rectangle into the input image
    axs1[1, 1].set_title('Final image of detection')
    axs1[1, 1].imshow(original, cmap='gray')
    rect = Rectangle((bbox_min_x, bbox_min_y), bbox_max_x - bbox_min_x, bbox_max_y - bbox_min_y, linewidth=1,
                     edgecolor='g', facecolor='none')
    axs1[1, 1].add_patch(rect)
    
    # Write the output image into output_filename, using the matplotlib savefig method
    extent = axs1[1, 1].get_window_extent().transformed(fig1.dpi_scale_trans.inverted())
    pyplot.savefig(output_filename, bbox_inches=extent, dpi=600)

    # Plot the current figure
    if SHOW_DEBUG_FIGURES:
        pyplot.show()

if __name__ == "__main__":
    main()
