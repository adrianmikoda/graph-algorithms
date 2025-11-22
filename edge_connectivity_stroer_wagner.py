from queue import PriorityQueue


def E_to_adjacency_list(V, E):
    adjacency_list = [{} for _ in range(V+1)]
    for u, v, w in E:
        adjacency_list[u][v] = w

    is_vertex_active = [True for _ in range(V+1)]
    return adjacency_list, is_vertex_active


def merge_vertices(a, b, adjacency_list, is_vertex_active):
    for v in adjacency_list[b].keys():
        w = adjacency_list[b][v]
        if v != a:
            adjacency_list[a][v] = adjacency_list[a].get(v, 0) + w
            adjacency_list[v][a] = adjacency_list[v].get(a, 0) + w

            adjacency_list[v].pop(b)
    is_vertex_active[b] = False


def minimum_cut_phase(V, adjacency_list, is_vertex_active):
    starting_vertex = None

    for i in range(1, V+1):
        if is_vertex_active[i]:
            starting_vertex = i
            break

    pq = PriorityQueue()
    w_counter = [0 for _ in range(V+1)]
    is_available = [True for _ in range(V+1)]

    pq.put((0, starting_vertex))
    a, b = None, None

    while not pq.empty():
        current_vertex = pq.get()[1]

        if not is_available[current_vertex]:
            continue

        b = a
        a = current_vertex

        for v in adjacency_list[current_vertex].keys():
            w = adjacency_list[current_vertex][v]
            if is_vertex_active[v]:
                w_counter[v] -= w
                pq.put((w_counter[v], v))

        is_available[current_vertex] = False

    w = 0
    for v in adjacency_list[a].keys():
        w += adjacency_list[a][v]

    merge_vertices(a, b, adjacency_list, is_vertex_active)

    return w


def edge_connectivity_stroer_wagner(V, E):
    adjacency_list, is_vertex_active = E_to_adjacency_list(V, E)
    answer = float('inf')
    for _ in range(V-2):
        answer = min(answer, minimum_cut_phase(V, adjacency_list, is_vertex_active))

    return answer
