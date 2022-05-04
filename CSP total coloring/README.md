# Total coloring
[Total coloring](https://en.wikipedia.org/wiki/Total_coloring) of a graph is the coloring of vertices and edges such that:
* vertices connected by an edge have different colors,
* edges sharing a common vertex have different colors and
* edges and their end-vertices have different colors.
The total chromatic number of a graph is the minimum number of colors required for total coloring of the graph.

Program finds the total chromatic number using the <ins>constraint satisfaction programming solver</ins> with the library [python-constraint](https://pypi.org/project/python-constraint/).   
A graph is given using the library [networkx](https://pypi.org/project/networkx/). 
