# Convert a photo to a patters
## Delaunay, Voronoi and Halftone
This script converts a photo to a pattern by extracting pixels of edges. Hence, edge extractors are required. I've used two edge extractors, Laplace and Canny. The final output of the Laplace edge detector was more promising despite being much simpler. The script can produce Delaunay Triangulation, Voronoi Diagram, and Halftoning pattern.

# Some Samples
![Delaunay tringulation on Laplace output](data/1_delaunay_laplace.png?raw=true "Delaunay tringulation on Laplace output")
![Delaunay tringulation on Canny output](data/1_delaunay_canny.png?raw=true "Delaunay tringulation on Canny output")
![Voronoi diagram on Laplace output](data/1_voronoi_laplace.png?raw=true "Voronoi diagram on Laplace output")
![Voronoi diagram on Canny output](data/1_voronoi_canny.png?raw=true "Voronoi diagram on Canny output")
![Halftoning](data/1_halftone.png?raw=true "Halftoning")
![Delaunay tringulation on Laplace output](data/2_delaunay_laplace.png?raw=true "Delaunay tringulation on Laplace output")
![Delaunay tringulation on Canny output](data/2_delaunay_canny.png?raw=true "Delaunay tringulation on Canny output")
![Voronoi diagram on Laplace output](data/2_voronoi_laplace.png?raw=true "Voronoi diagram on Laplace output")
![Voronoi diagram on Canny output](data/2_voronoi_canny.png?raw=true "Voronoi diagram on Canny output")
![Halftoning](data/2_halftone.png?raw=true "Halftoning")
