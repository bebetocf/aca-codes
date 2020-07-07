import tsplib95, random, copy, tqdm

n_tries = 100
n_random_swap = 200
n_child_random_swap = 3
swap_strategy = 'random'
points_path = "dj38.tsp"

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
        swap_child.append((nodes[2 * i], nodes[(2 * i) + 1]))
    return swap_child

def swap_random_cities(nodes, points, n_nodes, n_child, n_swap):
    best_value = f_n(nodes, points, n_nodes)
    best_path = copy.deepcopy(nodes)
    best_att = False

    for i in range(n_child):
        swap_child = generate_random_swap_pairs(n_nodes, random.randint(1, n_swap))
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

        if swap_strategy == 'close': 
            best_value, best_path, best_att = swap_close_cities(nodes, points, n_nodes)
        elif swap_strategy == 'random':
            best_value, best_path, best_att = swap_random_cities(nodes, points, n_nodes, n_random_swap, n_child_random_swap if n_iterations < 15 else 1)

        # print ("\t[", best_value, "]:", best_path)

        n_iterations += 1

    return best_path, best_value, n_iterations

def write_list_file(fl, lst):
    fl.write('[')
    for j in range(len(lst)):
        fl.write(str(lst[j]) + (', ' if (j != (len(lst) - 1)) else ']\n'))


def main():
    points = tsplib95.load('data/' + points_path)
    n_nodes = len(list(points.get_nodes()))
    all_value = 1000000000

    file_name = points_path.split('.')[0] + '_' + swap_strategy + '_' + str(n_tries)
    if swap_strategy == 'random':
        file_name += '_' + str(n_random_swap) + '_' + str(n_child_random_swap)
    file_name += '_random_decay.txt'
    file_log = open('results/log_' + file_name, 'w')

    for i in tqdm.tqdm(range(n_tries)):
        best_path, best_value, best_n = find_best_solution(points, n_nodes)
        if best_value < all_value:
            all_path, all_value, all_n, all_try = best_path, best_value, best_n, (i+1)

        file_log.write("[" + str(i+1) + "]:" + "\n")
        file_log.write("\tDistância do melhor caminho: " + str(best_value) + "\n")
        file_log.write("\tIterações executadas: " + str(best_n) + "\n")
        file_log.write("\tMelhor caminho: ")
        write_list_file(file_log, best_path)

    file_log.close()

    file_best = open('results/best_' + file_name, 'w')

    file_best.write("Overall best[" + str(all_try)  + "]:" + "\n")
    file_best.write("\tDistância do melhor caminho: " + str(all_value) + "\n")
    file_best.write("\tIterações executadas: " + str(all_n) + "\n")
    file_best.write("\tMelhor caminho: ")
    write_list_file(file_best, all_path)

    file_best.close()

if __name__ == '__main__':
    main()