# To solve path problem appeared in 'Find A Way' Android game

import networkx as nx 
import imgread
import hamilton
import cv2 
import numpy as np 

def matrix2graph(mat):

    graph = nx.Graph()
    root = None 

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] != 1:
                graph.add_node(i * mat.shape[1] + j, coord=(i, j), marked=False)
                if i < mat.shape[0] - 1 and mat[i+1, j] != 1:
                    graph.add_edge(i * mat.shape[1] + j, (i+1) * mat.shape[1] + j)
                if j < mat.shape[1] - 1 and mat[i, j+1] != 1:
                    graph.add_edge(i * mat.shape[1] + j, i * mat.shape[1] + j + 1)

            if mat[i, j] == 2:
                root = i * mat.shape[1] + j 

    return graph, root 


def hamiltonian_path(graph, root, solver):
    
    path = []

    if solver == 'dfs':
        done = [False]
        hamilton.hamilton_path_dfs(graph, root, path, done)
    elif solver == 'dp':
        hamilton.hamilton_path_dp(graph, root, path, len(graph.nodes))
    else:
        raise NotImplemented
                
    print('-'.join(map(str, path)))

    return [graph.nodes[p] for p in path] 


def main(argv):

    assert len(argv) > 1

    img = cv2.imread(argv[1])
    img2 = img[:,:,1]
    imgmat, xcenters, ycenters = imgread.read_img(img2)

    graph, root = matrix2graph(imgmat)

    path = hamiltonian_path(graph, root, solver='dp')
    
    imgshow = np.copy(img)

    coords = []

    for p in path:
        coords.append((xcenters[p['coord'][0]], ycenters[p['coord'][1]]))
    
    for i in range(len(coords)):
        
        cv2.circle(imgshow, (coords[i][0], coords[i][1]), 10, (0, 0, 255), 5)
        if i < len(coords) - 1:
            cv2.line(imgshow, coords[i], coords[i+1], (0, 0, 255), 5)

    cv2.namedWindow('Find A Way', cv2.WINDOW_NORMAL)
    cv2.imshow('Find A Way', imgshow)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    import sys
    main(sys.argv)