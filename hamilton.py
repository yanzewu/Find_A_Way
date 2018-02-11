import networkx as nx 

# OK I should have written these on C

def hamilton_path_dfs(graph:nx.Graph, root, path, done):
    """ DFS brute search.
    """
    graph.nodes[root]['marked'] = True
    path.append(root)

    for neigh in graph[root]:
        if done[0]: # fast return
            return 
        if not graph.nodes[neigh]['marked']:
            hamilton_path_dfs(graph, neigh, path, done)

    if done[0]:
        return 

    if len(path) == len(graph.nodes):
        done[0] = True 
    else:
        graph.nodes[root]['marked'] = False 
        path.pop()
    

def hamilton_path_dp(graph:nx.Graph, root, path, size):
    
    graph.nodes[root]['marked'] = True 

    if size == 1:
        path += [root]
        return True 

    for neigh in graph[root]:
        if graph.nodes[neigh]['marked']:
            continue 
        subpath = []
        if hamilton_path_dp(graph, neigh, subpath, size-1):
            path += [root] + subpath
            return True 
        
    graph.nodes[root]['marked'] = False 
    return False 

