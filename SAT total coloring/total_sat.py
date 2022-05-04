from pysat.solvers import Glucose3

def total_coloring(graph):

    colors = 0
    num_of_nodes = graph.number_of_nodes()
    max_colors = graph.number_of_edges() + num_of_nodes
    num_of_obj = 0

    nodes = {}
    for u in graph.nodes():
        nodes[u] = num_of_obj
        num_of_obj += 1
        colors = max(colors, graph.degree(u))

    edges = {}
    for u, v in graph.edges():
        edges[u, v] = num_of_obj
        edges[v, u] = num_of_obj
        num_of_obj += 1

    while colors != max_colors:
        colors += 1
        g = Glucose3()
        variables = {}

        #create var for each pair (node/edge, possible color)
        var = 1
        for v in range(num_of_nodes):
            for c in range(colors):
                variables[(v, c)] = var
                var += 1
        for e in range(num_of_nodes, num_of_obj):
            for c in range(colors):
                variables[(e, c)] = var
                var += 1

        for v in graph.nodes():
            #each node will have at least 1 color
            g.add_clause([variables[nodes[v], c] for c in range(colors)])

            for color1 in range(colors - 1):
                for color2 in range(color1 + 1, colors):
                    #each node will have no more than 1 color
                    g.add_clause([-variables[nodes[v], color1], -variables[nodes[v], color2]])

            #node and its edges, must be different
            different = [edges[v, u] for v, u in graph.edges(v)] + [nodes[v]]
            for i in range(len(different) - 1):
                for j in range(i + 1, len(different)):
                    for color in range(colors):
                        #each node and its edges will have different colors
                        g.add_clause([-variables[different[i], color], -variables[different[j], color]])
        
        for u, v in graph.edges():
            #each edge will have at least 1 color
            g.add_clause([variables[edges[u, v], c] for c in range(colors)])

            for color1 in range(colors - 1):
                for color2 in range(color1 + 1, colors):
                    #each edge will have no more than 1 color
                    g.add_clause([-variables[edges[u, v], color1], -variables[edges[u, v], color2]])

            #each edge and its nodes will have different colors
            for color in range(colors):
                g.add_clause([-variables[nodes[u], color], -variables[nodes[v], color]])
                g.add_clause([-variables[edges[u, v], color], -variables[nodes[u], color]])
                g.add_clause([-variables[edges[u, v], color], -variables[nodes[v], color]])

        if g.solve():
            solution = g.get_model()
            var_keys = list(variables.keys())
            for x in solution:
                if x > 0:
                    var, color = var_keys[x - 1]
                    if var < num_of_nodes:
                        nodes_keys = list(nodes.keys())
                        graph.nodes[nodes_keys[var]]["color"] = color
                    else:
                        edges_keys = list(edges.keys())
                        index_in_dict = (var - num_of_nodes) * 2
                        graph.edges[edges_keys[index_in_dict]]["color"] = color
            return colors
