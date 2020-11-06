from  PIL import Image, ImageDraw, ImageStat, ImageFilter
from pathlib import Path

def halftone(img, sample, scale=1):
    img_grey = img.convert('L')  # Converts to 8-bit pixels (gray).
    size = img_grey.size[0]*scale, img_grey.size[1]*scale
    bitmap = Image.new('1', size) # mode = '1' means 1-bit pixels
    draw = ImageDraw.Draw(bitmap)

    for x in range(0, img_grey.size[0], sample):
        for y in range(0, img_grey.size[1], sample):
            box = img_grey.crop((x, y, x+sample, y+sample))
            mean = ImageStat.Stat(box).mean[0]
            diameter = (mean/255) ** 0.5
            edge = 0.5 * (1-diameter)
            x_pos, y_pos = (x+edge) * scale, (y+edge) * scale
            box_edge = sample * diameter * scale
            draw.ellipse((x_pos, y_pos, x_pos+box_edge, y_pos+box_edge),
                         fill=255)

    # bitmap = bitmap.rotate(-angle, expand=1)
    width_half, height_half = bitmap.size
    xx = (width_half - img.size[0]*scale) / 2
    yy = (height_half - img.size[1]*scale) / 2
    bitmap = bitmap.crop((xx, yy, xx + img.size[0]*scale,
                                  yy + img.size[1]*scale))
    return Image.merge('1', [bitmap])

# Sample usage

img = Image.open(Path('data/portrait.jpg'))
img_ht = halftone(img, 8, 1)
img_ht.show()
img_edges = img.filter(ImageFilter.FIND_EDGES)
img_edges.show()
img_ht = halftone(img_edges, 6, 1)
img_ht.show()