# Implementation of the ford-fulkerson algorithm using DFS
from collections import deque
import math


def get_path(vertex, parent, residual_network_capacity):
    path = []
    max_possible_flow_value = math.inf
    while parent[vertex] is not None:
        max_possible_flow_value = min(max_possible_flow_value,
                                      residual_network_capacity.get((parent[vertex], vertex), math.inf))
        path.append(vertex)
        vertex = parent[vertex]

    path.append(vertex)
    return path[::-1], max_possible_flow_value


def dfs(start, end, V, residual_network, residual_network_capacity):
    stack = deque()
    visited = [False for _ in range(V+1)]
    parent = [None for _ in range(V+1)]

    parent[start] = None
    visited[start] = True
    stack.append(start)

    while stack:
        u = stack.pop()

        if u == end:
            return get_path(u, parent, residual_network_capacity)

        for v in residual_network[u]:
            if not visited[v] and residual_network_capacity.get((u, v), 0) > 0:
                parent[v] = u
                visited[v] = True
                stack.append(v)

    return None


def E_to_residual_network(V, E):
    residual_network = [[] for _ in range(V+1)]
    residual_network_capacity = {}

    for u, v, w in E:
        residual_network[u].append(v)
        residual_network[v].append(u)
        residual_network_capacity[(u, v)] = w
        residual_network_capacity[(v, u)] = residual_network_capacity.get((v, u), 0)

    return residual_network, residual_network_capacity


def ford_fulkerson_dfs(V, E, start, end):
    residual_network, residual_network_capacity = E_to_residual_network(V, E)

    cumulative_flow = 0
    while path_and_max_possible_flow_value := dfs(start, end, V, residual_network, residual_network_capacity):

        path, max_possible_flow_value = path_and_max_possible_flow_value

        current_vertex = path[0]
        for i in range(1, len(path)):
            previous_vertex = current_vertex
            current_vertex = path[i]
            residual_network_capacity[(previous_vertex, current_vertex)] -= max_possible_flow_value
            residual_network_capacity[(current_vertex, previous_vertex)] += max_possible_flow_value

        cumulative_flow += max_possible_flow_value

    return cumulative_flow
