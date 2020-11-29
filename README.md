# Convert a photo to a patters (i.e., Delaunay, Voronoi and halftone)
This script converts a photo to a pattern by extracting pixels of edges. Hence, edge extractors are required. I've used two edge extractors, Laplace and Canny. The final output of the Laplace edge detector was more promising despite being much simpler. The script can produce Delaunay Triangulation, Voronoi Diagram, and Halftoning pattern.

# Some samples
![Delaunay tringulation on Laplace output](data/1_delaunay_laplace.png?raw=true "Delaunay tringulation on Laplace output")
