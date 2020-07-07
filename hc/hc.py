import tsplib95, random, copy

n_tries = 100
n_random_swap = 50
n_child_random_swap = 1

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

def generate_random_swap_pairs(n_nodes, n_swap):
    nodes = list(range(n_nodes))
    random.shuffle(nodes)
    swap_child = []
    for i in range(n_swap):
        # first = random.randint(0, n_nodes - 1)
        # second = first
        # while second == first:
        #     second = random.randint(0, n_nodes - 1)
        swap_child.append((nodes[2 * i], nodes[(2 * i) + 1]))
    return swap_child

def swap_random_cities(nodes, points, n_nodes, n_child, n_swap):
    best_value = f_n(nodes, points, n_nodes)
    best_path = copy.deepcopy(nodes)
    best_att = False

    for i in range(n_child):
        swap_child = generate_random_swap_pairs(n_nodes, n_swap)
        for c in swap_child:
            swap_position(nodes, c[0], c[1])

        value = f_n(nodes, points, n_nodes)
        
        if value < best_value:
            best_value = value
            best_path = copy.deepcopy(nodes)
            best_att = True

        for c in swap_child:
            swap_position(nodes, c[0], c[1])

    return best_value, best_path, best_att

def find_best_solution(points, n_nodes):
    nodes = list(points.get_nodes())
    random.shuffle(nodes)

    best_path, best_value, n_iterations, best_att = nodes, f_n(nodes, points, n_nodes), -1, True

    while best_att:
        nodes = copy.deepcopy(best_path)

        # best_value, best_path, best_att = swap_close_cities(nodes, points, n_nodes)
        best_value, best_path, best_att = swap_random_cities(nodes, points, n_nodes, n_random_swap, n_child_random_swap)

        # print ("\t[", best_value, "]:", best_path)

        n_iterations += 1

    return best_path, best_value, n_iterations

def main():
    points_path = "./dj38.tsp"
    points = tsplib95.load(points_path)
    n_nodes = len(list(points.get_nodes()))
    all_value = float('inf')

    for i in range(n_tries):
        best_path, best_value, best_n = find_best_solution(points, n_nodes)
        if best_value < all_value:
            all_path, all_value, all_n, all_try = best_path, best_value, best_n, i

        # print ("[", (i+1), "]:")
        # print ("\tDistância do melhor caminho:", best_value)
        # print ("\tIterações executadas:", best_n)
        # print ("\tMelhor caminho:", best_path)
            
    print ("Overall best[", all_try , "]:")
    print ("\tDistância do melhor caminho:", best_value)
    print ("\tIterações executadas:", best_n)
    print ("\tMelhor caminho:", best_path)

if __name__ == '__main__':
    main()