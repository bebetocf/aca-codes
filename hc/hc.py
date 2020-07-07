import tsplib95, random, copy

# TODO: trocar duas cidades aleatorias
# Filho nao pode ficar muito diferente do pai
# No comeco pode trocar muitos filhos e depois trocar pouco

def f_n(nodes, points, n_nodes):
    dist = 0
    for i in range(n_nodes-1):
        edge = nodes[i], nodes[i+1]
        dist += points.get_weight(*edge)
    return dist

def swap_position(nodes, i, j):
    nodes[i], nodes[j] = nodes[j], nodes[i]

def swap_close_cities(nodes, points, n_nodes):
    best_value = f_n(nodes, points, n_nodes)
    best_path = copy.deepcopy(nodes)
    best_att = False

    for i in range(n_nodes-1):
        swap_position(nodes, i, i+1)
        value = f_n(nodes, points, n_nodes)
        
        if value < best_value:
            best_value = value
            best_path = copy.deepcopy(nodes)
            best_att = True

        swap_position(nodes, i, i+1)

    return best_value, best_path, best_att

def find_best_solution(points, n_nodes):
    nodes = list(points.get_nodes())
    random.shuffle(nodes)

    best_path, best_value, n_iterations, best_att = nodes, f_n(nodes, points, n_nodes), -1, True

    while best_att:
        nodes = copy.deepcopy(best_path)
        
        best_value, best_path, best_att = swap_close_cities(nodes, points, n_nodes)

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