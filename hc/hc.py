import tsplib95, random, copy

def f_n(nodes, points, n_nodes):
    dist = 0
    for i in range(n_nodes-1):
        edge = nodes[i], nodes[i+1]
        dist += points.get_weight(*edge)
    return dist

def find_best_solution(points, n_nodes):
    nodes = list(points.get_nodes())
    random.shuffle(nodes)

    best_path, best_value, n_iterations, best_att = nodes, f_n(nodes, points, n_nodes), -1, True

    while best_att:
        nodes = copy.deepcopy(best_path)
        best_att = False

        for i in range(n_nodes-1):
            nodes[i], nodes[i+1] = nodes[i+1], nodes[i]
            value = f_n(nodes, points, n_nodes)
            
            if value < best_value:
                best_value = value
                best_path = copy.deepcopy(nodes)
                best_att = True

            nodes[i], nodes[i+1] = nodes[i+1], nodes[i]

        n_iterations += 1

    return best_path, best_value, n_iterations

def main():
    points_path = "./dj38.tsp"
    points = tsplib95.load(points_path)
    n_nodes = len(list(points.get_nodes()))

    for i in range(10):
        best_path, best_value, best_n = find_best_solution(points, n_nodes)
        print ("[", (i+1), "]:")
        print ("\tDistância do melhor caminho:", best_value)
        print ("\tIterações executadas:", best_n)
        print ("\tMelhor caminho:", best_path)


if __name__ == '__main__':
    main()