from ford_fulkerson_bfs import ford_fulkerson_bfs


def edge_connectivity_ford_fulkerson(V, E):
    answer = float('inf')
    for v in range(2, V+1):
        answer = min(answer, ford_fulkerson_bfs(V, E, 1, v))
    return answer
