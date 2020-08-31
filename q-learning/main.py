import numpy as np

alpha = 0.5
gamma = 0.8
terminal_st = 5

q_value = np.zeros((6, 4))

def update_value(value, state, action):
    if state == terminal_st:
        return value, state
    
    next_s = get_next_state(state, action)
    
    rw = -1
    # bateu na parede
    if next_s == state:
        rw = -10
    # estado terminal
    elif next_s == terminal_st:
        rw = 10
   
    value[state][action] += alpha * (rw + gamma * ( np.max([value[next_s][i] for i in range(4)]) - value[state, action] ) )

    np.set_printoptions(precision=3)
    # print(print_value(value), "\n")
    return value, next_s


def get_next_state(s, a):
    next_s = s

    if a == 0:
        if s != 2 and s != 5:
            next_s = s + 1
    if a == 1:
        if s != 0 and s != 3:
            next_s = s - 1
    if a == 2:
        if s != 0 and s != 1 and s!= 2:
            next_s = s - 3
    if a == 3:
        if s != 3 and s != 4 and s!= 5:
            next_s = s + 3
    
    return next_s

def return_policy(value):   
    policy = []

    for s in range(6):
        action = np.argmax([value[s][i] for i in range(4)])
        policy.append(action)
    
    actions = ["UP","DW","LF","RG"]

    s1 = [actions[policy[2]], "+10"]
    s2 = [actions[policy[1]],actions[policy[4]]]
    s3 = [actions[policy[0]],actions[policy[3]]]

    print("\n",s1,"\n",s2,"\n",s3, "\n")

    return(policy)

def print_value(value):
    aux = np.zeros((3, 2, 4))
    aux[0,] = np.array((value[2],value[5]))
    aux[1,] = np.array((value[1],value[4]))
    aux[2,] = np.array((value[0],value[3]))
    return aux

if __name__ == "__main__":

    state = 0
    for path in [[0, 0, 0, 3], [3, 3, 2, 0]]:
        for action in path:
            q_value, state = update_value(q_value, state, action)

            if state == terminal_st:
                break
        state = 4

    print("Updated values: \n", q_value, "\n---\n")

    policy = return_policy(q_value)
