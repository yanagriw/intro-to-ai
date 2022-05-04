import constraint

def total_coloring(graph):

    colors = 0
    max_colors = graph.number_of_edges() + graph.number_of_nodes()
    num_of_vars = 0

    nodes = {}
    for u in graph.nodes():
        nodes[u] = num_of_vars
        num_of_vars += 1
        colors = max(colors, graph.degree(u))

    edges = {}
    for u, v in graph.edges():
        edges[u, v] = num_of_vars
        edges[v, u] = num_of_vars
        num_of_vars += 1

    while colors != max_colors:
        colors += 1
        problem = constraint.Problem()
        problem.addVariables(nodes.values(), range(0, colors))
        problem.addVariables(set(edges.values()), range(0, colors))
        for u in nodes:
            different = [edges[u, v] for u, v in graph.edges(u)] + [nodes[u]]
            problem.addConstraint(constraint.AllDifferentConstraint(), different)
            for v in graph.neighbors(u):
                different = [nodes[u], edges[u, v], nodes[v]]
                problem.addConstraint(constraint.AllDifferentConstraint(), different)
        
        solution = problem.getSolution()
        if solution != None:
            for u in nodes:
                graph.nodes[u]["color"] = solution[nodes[u]]
            for u, v in edges:
                graph.edges[u, v]["color"] = solution[edges[u, v]]
            return colors
