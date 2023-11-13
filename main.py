import json
import numpy as np
import random
from collections import Counter
from PIL import Image

imname = "images/" + input("filename: ") + ".png"

precomp = json.load(open("precompute.json", "r"))
precomp_options = [eval(x) for x in precomp.keys()]

def findBestColor(input):
  highest = 1000000000000
  highest_index = 0
  for x in range(0, len(precomp_options)):
    gim = list(precomp_options[x])
    sim = sum([abs(input[y]-gim[y]) for y in range(0, 3)])/3
    if sim < highest:
      highest = sim
      highest_index = x
  return highest_index


im = Image.open(imname)
pixels = np.asarray(im).tolist()

out = Image.new("RGBA", (im.width*10, im.height*10), (0, 0, 0, 0))

scale = 5

xvals = [x for x in range(0, len(pixels), scale)]
yvals = [x for x in range(0, len(pixels[0]), scale)]
random.shuffle(xvals)
random.shuffle(yvals)

progress = 0

for x in xvals:
  for y in yvals:
    f = findBestColor(pixels[x][y])
    #print(precomp[list(precomp.keys())[f]])
    gim = Image.open("files/" + precomp[list(precomp.keys())[f]] + ".png")
    gim = gim.convert("RGBA")
    gim = gim.rotate(random.randint(0, 359), Image.NEAREST, expand=1)
    size = random.randint(100,200)
    gim = gim.resize((size, size), Image.NEAREST)
    out.paste(gim, (y*10, x*10), gim)
  print(f"{progress}/{round(len(pixels)/scale)}")
  progress += 1

out.save("result.png")
