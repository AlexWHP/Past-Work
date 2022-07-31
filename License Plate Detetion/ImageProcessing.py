""" Each of these functions deal with image processing and all, bar the first three functions, constitute my own work. """

# import our basic, light-weight png reader library
import imageIO.png

import math
from collections import deque

# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# Create a list of lists based array representation for an image, initialized with a value
def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array

def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for y in range(image_height):
        for x in range(image_width):
            greyscale_pixel_array[y][x] = int(round(0.299*pixel_array_r[y][x] + 0.587*pixel_array_g[y][x] + 0.114*pixel_array_b[y][x]))
    
    return greyscale_pixel_array

# Contrast Stretching
def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    # Getting max and min
    num_min, num_max = 255, 0
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] < num_min:
                num_min = pixel_array[y][x]
            if pixel_array[y][x] > num_max:
                num_max = pixel_array[y][x]
    # All the same - return zeros
    scaled = createInitializedGreyscalePixelArray(image_width, image_height)
    if num_min == num_max:
        return scaled
    # Scale
    diff = num_max - num_min
    for y in range(image_height):
        for x in range(image_width):
            scaled[y][x] = round(255*(pixel_array[y][x]-num_min)/diff)
    return scaled

# Filtering to detect high contrast regions
def computeStandardDeviationImage5x5(pixel_array, image_width, image_height):
    width = 5
    radius = width // 2
    arr = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(radius, image_height - radius):
        for x in range(radius, image_width- radius):
            vals = []
            total = 0
            for y2 in range(width):
                for x2 in range(width):
                    y_pos = y + y2 - radius
                    x_pos = x + x2 - radius
                    total += pixel_array[y_pos][x_pos]
                    vals.append(pixel_array[y_pos][x_pos])
            mean = total / len(vals)
            variance = 0
            variance = sum([math.pow(mean-num, 2) for num in vals])
            arr[y][x] = math.sqrt(variance/len(vals))
    return arr

# Threshholding for segmentation
def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] < threshold_value:
                pixel_array[y][x] = 0
            else:
                pixel_array[y][x] = 255
    return pixel_array

# Morphological Operations - Dilation
def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    arr = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] != 0:
                for y2 in range(3):
                    for x2 in range(3):
                        y_pos = y+y2-1
                        x_pos = x+x2-1
                        if y_pos < 0 or y_pos >= image_height or x_pos < 0 or x_pos >= image_width:
                            pass
                        else:
                            arr[y_pos][x_pos] = 1
    return arr

# Morphological Operations - Erosion
def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    arr = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] != 0:
                erode = False
                for y2 in range(3):
                    for x2 in range(3):
                        y_pos = y+y2-1
                        x_pos = x+x2-1
                        if y_pos < 0 or y_pos >= image_height or x_pos < 0 or x_pos >= image_width:
                           erode = True
                        elif pixel_array[y_pos][x_pos] == 0:
                            erode = True
                if erode == False:
                    arr[y][x] = 1
    return arr

# Connected Component Analysis - Uniquely labels connected sections
def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    labels = {}
    q = deque()
    label = 1
    not_visited = [ [True]*image_width for i in range(image_height)]
    for j in range(image_height):
        for i in range(image_width):
            if pixel_array[j][i] != 0 and not_visited[j][i]:
                labels[label] = 0
                q.clear()
                q.appendleft([j, i])
                while len(q) != 0:
                    pixel_cord = q.pop()
                    y, x = pixel_cord[0], pixel_cord[1]
                    labels[label] += 1
                    pixel_array[y][x] = label
                    not_visited[y][x] = False
                    if x-1 > 0 and pixel_array[y][x-1] != 0 and not_visited[y][x-1]:
                        not_visited[y][x-1] = False
                        q.appendleft([y, x-1])
                    if x+1 < image_width and pixel_array[y][x+1] != 0  and not_visited[y][x+1]:
                        not_visited[y][x+1] = False
                        q.appendleft([y, x+1])
                    if y-1 > 0 and pixel_array[y-1][x] != 0 and not_visited[y-1][x]:
                        not_visited[y-1][x] = False
                        q.appendleft([y-1, x])
                    if y+1 < image_height and pixel_array[y+1][x] != 0  and not_visited[y+1][x]:
                        not_visited[y+1][x] = False
                        q.appendleft([y+1, x])
                label += 1
    return pixel_array, labels

# Based on expected ratio of width to height of a license plate we can select the best connected component
def computeBestBoxConnectedComponent(pixel_array, image_width, image_height, labels):
    bbox_min_x, bbox_max_x = image_width, 0
    bbox_min_y, bbox_max_y = image_height, 0
    while len(labels.keys()) > 0:
        num_max = 0
        largest = 0
        for key, value in labels.items():
            if value > num_max:
                num_max = value
                largest = key
        # Computing the box for largest
        for y in range(image_height):
            for x in range(image_width):
                if pixel_array[y][x] == largest:
                    if x < bbox_min_x:
                        bbox_min_x = x
                    if x > bbox_max_x:
                        bbox_max_x = x
                    if y < bbox_min_y:
                        bbox_min_y = y
                    if y > bbox_max_y:
                        bbox_max_y = y
        # Calculating Ratio
        ratio = (bbox_max_x - bbox_min_x) / (bbox_max_y - bbox_min_y)
        if ratio >= 1.5 and ratio <= 5:
            break
        del labels[largest]
        bbox_min_x, bbox_max_x = image_width, 0
        bbox_min_y, bbox_max_y = image_height, 0
    return bbox_min_x, bbox_max_x, bbox_min_y, bbox_max_y

# Extension - Using Sobel to more accurately perform morphological operations to extend the 
#             original to be able to handle less clear plates
def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    arr = createInitializedGreyscalePixelArray(image_width, image_height)
    sobel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    for y in range(image_height):
        for x in range(image_width):
            total = 0.0
            if y == 0 or x == 0 or y == image_height-1 or x == image_width-1:
                arr[y][x] = total
            else:
                for y2 in range(3):
                    for x2 in range(3):
                            total += pixel_array[y+y2-1][x+x2-1]*sobel[y2][x2]
                arr[y][x] = abs((1.0/8.0)*total)
    return arr

def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    arr = createInitializedGreyscalePixelArray(image_width, image_height)
    sobel = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    for y in range(image_height):
        for x in range(image_width):
            total = 0.0
            if y == 0 or x == 0 or y == image_height-1 or x == image_width-1:
                arr[y][x] = total
            else:
                for y2 in range(3):
                    for x2 in range(3):
                            total += pixel_array[y+y2-1][x+x2-1]*sobel[y2][x2]
                arr[y][x] = abs((1.0/8.0)*total)
    return arr
