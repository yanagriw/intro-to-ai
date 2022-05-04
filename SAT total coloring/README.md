# Total coloring
[Total coloring](https://en.wikipedia.org/wiki/Total_coloring) of a graph is the coloring of vertices and edges such that:
* vertices connected by an edge have different colors,
* edges sharing a common vertex have different colors and
* edges and their end-vertices have different colors.
The total chromatic number of a graph is the minimum number of colors required for total coloring of the graph.

Program finds the total chromatic number using the <ins>Satisfiability of boolean formulas (SAT)</ins> with the library [python-sat](https://pypi.org/project/python-sat/).   
A graph is given using the library [networkx](https://pypi.org/project/networkx/). 
