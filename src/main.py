from PIL import Image, ImageDraw, ImageStat, ImageFilter
from pathlib import Path
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay
import numpy as np
import matplotlib.pyplot as plt
from canny import cannyEdgeDetector
import sys


def halftone(img, sample, width, height):
    img_grey = img.convert('L')  # Converts to 8-bit pixels (gray).
    size = width, height
    bitmap = Image.new('1', size)  # mode = '1' means 1-bit pixels
    draw = ImageDraw.Draw(bitmap)

    for x in range(0, img_grey.size[0], sample):
        for y in range(0, img_grey.size[1], sample):
            box = img_grey.crop((x, y, x+sample, y+sample))
            mean = ImageStat.Stat(box).mean[0]
            diameter = (mean/255) ** 0.5
            edge = 0.5 * (1-diameter)
            x_pos, y_pos = (x+edge), (y+edge)
            box_edge = sample * diameter
            draw.ellipse((x_pos, y_pos, x_pos+box_edge, y_pos+box_edge),
                         fill=255)

    width_half, height_half = bitmap.size
    xx = (width_half - width) / 2
    yy = (height_half - height) / 2
    bitmap = bitmap.crop((xx, yy, xx + width,
                          yy + height))
    return Image.merge('1', [bitmap])


def extract_point(points, threshold, width, height):
    '''threshold needs to be a tuple'''
    result_img = np.zeros((width, height))
    voronoi_sites = np.empty((0, 2), int)

    # I want to ignore the white box around the edge image
    ipoints = points
    for i, p in enumerate(ipoints):
        for j, t in enumerate(p):
            if t > threshold:
                # print('{} , {}'.format(i,j))
                voronoi_sites = np.append(voronoi_sites, [[j, i]], axis=0)
                result_img[j][i] = 255  # j is represeting height
    return result_img, voronoi_sites


def draw_voronoi(sites, output_name):
    vor = Voronoi(sites)
    voronoi_plot_2d(vor, show_vertices=False, show_points=False)
    plt.gca().invert_yaxis()  # to reverse y axis to show image properly
    fig = plt.gcf()
    fig.set_size_inches(8, 8)
    plt.axis('off')
    plt.show()
    fig.savefig(output_name, bbox_inches='tight',
                transparent=True, pad_inches=0)


def draw_delaunay(sites, output_name, draw_sites=False):
    tess = Delaunay(sites)
    tri = tess.vertices
    fig = plt.gcf()
    fig.set_size_inches(8, 8)
    plt.triplot(sites[:, 0], sites[:, 1], tri, linewidth=0.3, color='black')
    if draw_sites == True:
        plt.plot(sites[:, 0], sites[:, 1], 'o')
    plt.gca().invert_yaxis()  # to reverse y axis to show image properly
    plt.axis('off')
    plt.show()
    fig.savefig(output_name, bbox_inches='tight',
                transparent=True, pad_inches=0)


def canny_based_approach(img, output_type, output_name, width, height):
    gray_img = np.asarray(img.convert('L'))
    detector = cannyEdgeDetector(gray_img, sigma=6,
                                 kernel_size=5, lowthreshold=0.8,
                                 highthreshold=0.8)
    img_canny_edges = detector.detect()
    pixels, sites = extract_point(img_canny_edges, 10, width, height)
    if output_type == 'voronoi':
        draw_voronoi(sites, output_name)
    elif output_type == 'delaunay':
        draw_delaunay(sites, output_name)


def laplacian_based_approach(img, output_type, output_name, width, height):
    # Laplacian edge detector
    img_edges = img.filter(ImageFilter.FIND_EDGES)
    points = list(img_edges.getdata())
    points = [points[(i * width)+1:((i + 1) * width)-1]
              for i in range(1, height-1)]
    pixels, sites = extract_point(points, (30, 30, 30), width, height)
    img = Image.fromarray(pixels)
    if output_type == 'voronoi':
        draw_voronoi(sites, output_name)
    elif output_type == 'delaunay':
        draw_delaunay(sites, output_name)


def halftoning(img, output_name, width, height):
    img_ht = halftone(img, 8, width, height)
    img_ht.show()
    # TODO: Save file


def main():
    file_name = sys.argv[1]  # give file name as an argument
    output_name = sys.argv[2]
    edge_detection = sys.argv[3]  # canny or laplace
    output_type = sys.argv[4]
    img = Image.open(Path(file_name))  # e.g., 'data/portrait.jpg'
    width, height = img.size
    if output_type not in ['voronoi', 'delaunay', 'halftone']:
        print(
            '''Please select a valid output type: 'voronoi' or 'delaunay' or 'halftone' ''')
    elif output_type == 'halftone':
        halftoning(img, output_name, width, height)
    else:
        if edge_detection == 'canny':
            canny_based_approach(img, output_type, output_name, width, height)
        elif edge_detection == 'laplace':
            laplacian_based_approach(
                img, output_type, output_name, width, height)
        else:
            print('''Please select a valid option: 'canny' or 'laplace' ''')
    # TODO: Plot the original file and the result in a figure
    # TODO: Write a readme file


if __name__ == "__main__":
    main()
