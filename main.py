import json
import numpy as np
import random
from collections import Counter
from PIL import Image

# Prompt user for input filename
filename = input("Enter filename (without extension): ")
imname = f"images/{filename}.png"

# Load precomputed options from JSON file
precomp_data = json.load(open("precompute.json", "r"))
precomp_options = [eval(x) for x in precomp_data.keys()]

# Function to find the best color match
def find_best_color(input_rgb):
    lowest_difference = float('inf')
    best_index = 0

    for index, option in enumerate(precomp_options):
        option_rgb = list(option)
        difference = sum(abs(input_rgb[channel] - option_rgb[channel]) for channel in range(3)) / 3

        if difference < lowest_difference:
            lowest_difference = difference
            best_index = index

    return best_index

# Open input image
im = Image.open(imname)
pixels = np.asarray(im).tolist()

# Create a new RGBA image for the output
out = Image.new("RGBA", (im.width * 10, im.height * 10), (0, 0, 0, 0))

# Set the scale factor for processing
scale = 5

# Generate shuffled lists of x and y values
xvals = [x for x in range(0, len(pixels), scale)]
yvals = [x for x in range(0, len(pixels[0]), scale)]
random.shuffle(xvals)
random.shuffle(yvals)

# Initialize progress counter
progress = 0

# Iterate over pixel values
for x in xvals:
    for y in yvals:
        # Find the best color match for the current pixel
        color_index = find_best_color(pixels[x][y])

        # Retrieve the corresponding precomputed option
        option_key = list(precomp_data.keys())[color_index]
        option_path = f"files/{precomp_data[option_key]}.png"

        # Open the precomputed option image
        gim = Image.open(option_path)
        gim = gim.convert("RGBA")

        # Rotate and resize the precomputed option
        gim = gim.rotate(random.randint(0, 359), Image.NEAREST, expand=1)
        size = random.randint(100, 200)
        gim = gim.resize((size, size), Image.NEAREST)

        # Paste the precomputed option onto the output image
        out.paste(gim, (y * 10, x * 10), gim)

    # Print progress
    print(f"{progress}/{round(len(pixels) / scale)}")
    progress += 1

# Save the resulting image
out.save("result.png")
