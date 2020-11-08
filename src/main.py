from PIL import Image, ImageDraw, ImageStat, ImageFilter
from pathlib import Path
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay
import numpy as np
import matplotlib.pyplot as plt

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

    width_half, height_half = bitmap.size
    xx = (width_half - img.size[0]*scale) / 2
    yy = (height_half - img.size[1]*scale) / 2
    bitmap = bitmap.crop((xx, yy, xx + img.size[0]*scale,
                                  yy + img.size[1]*scale))
    return Image.merge('1', [bitmap])


def extract_point(edges_img, threshold):
    '''threshold needs to be a tuple'''
    width, height = edges_img.size
    result_img = np.zeros((width-2, height-2))
    voronoi_sites = np.empty((0,2), int)
    points = list(edges_img.getdata())

    # I want to ignore the white box around the edge image
    points = [points[(i * width)+1:((i + 1) * width)-1] for i in range(1,height-1)]
    for i, p in enumerate(points):
        for j, t in enumerate(p):
            if t > threshold:
                # print('{} , {}'.format(i,j))
                voronoi_sites = np.append(voronoi_sites,[[i,j]] , axis=0)
                result_img[i][j] = 255
    return result_img, voronoi_sites


def draw_voronoi(sites):
    vor = Voronoi(sites)
    voronoi_plot_2d(vor, show_vertices = False, show_points = False)
    plt.show()


def draw_delaunay(sites):
    tess = Delaunay(sites)
    tri = tess.vertices
    plt.triplot(sites[:,0], sites[:,1], tri, linewidth=0.3, color='black')
    # plt.plot(sites[:,0], sites[:,1], 'o')
    plt.show()

def main():
    img = Image.open(Path('data/portrait.jpg'))
    # img_ht = halftone(img, 8, 1)
    # img_ht.show()
    img_edges = img.filter(ImageFilter.FIND_EDGES)
    img_edges.show()
    pixels, sites = extract_point(img_edges,(20,20,20))
    img = Image.fromarray(pixels)
    img.show()
    draw_voronoi(sites)
    draw_delaunay(sites)


if __name__ =="__main__":
    main()