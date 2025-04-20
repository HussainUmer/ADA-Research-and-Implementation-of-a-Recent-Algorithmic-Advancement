import math
import random
import time
import matplotlib.pyplot as plt

def bellman_ford(graph, source):
    # Number of vertices in graph
    n = len(graph)
    
    # Initialize distances with infinity
    dist = {v: math.inf for v in range(n)}
    dist[source] = 0
    
    # Relax all edges n-1 times
    for _ in range(n - 1):
        for u in range(n):
            for v, weight in graph[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
    
    # Check for negative-weight cycles
    for u in range(n):
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                print("Graph contains negative weight cycle")
                return None
    
    return dist

# Bellman-Ford-like algorithm, but limiting the number of negative edges in the path
def hop_limited_bfd(graph, source, max_hops):
    n = len(graph)
    dist = {v: math.inf for v in range(n)}
    dist[source] = 0
    for _ in range(max_hops):
        for u in range(n):
            for v, weight in graph[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
    return dist

def price_function(graph, source):
    n = len(graph)
    dist = hop_limited_bfd(graph, source, n)
    phi = {v: dist[v] for v in range(n)}  # Assigning the shortest path from source as price function
    return phi

def apply_price_function(graph, phi):
    n = len(graph)
    new_graph = {u: [] for u in range(n)}
    for u in range(n):
        for v, weight in graph[u]:
            new_weight = weight + phi[u] - phi[v]
            if new_weight < 0:
                new_weight = 0  # Ensuring no negative edges
            new_graph[u].append((v, new_weight))
    return new_graph

def betweenness_reduction(graph, tau, beta):
    # Sample vertices and compute β-hop distances
    T = random.sample(range(len(graph)), int(tau * math.log(len(graph))))
    dist = {v: math.inf for v in range(len(graph))}
    
    for x in T:
        dist_x = hop_limited_bfd(graph, x, beta)
        for v in range(len(graph)):
            if dist_x[v] < dist[v]:
                dist[v] = dist_x[v]
    
    # Applying price function derived from betweenness reduction
    phi = {v: dist[v] for v in range(len(graph))}
    return phi

def find_negative_sandwich(graph):
    # Implementing the process to find a negative sandwich as described in the paper
    n = len(graph)
    for x in range(n):
        for y in range(n):
            reachable_from_x = set()
            reachable_to_y = set()
            for u in range(n):
                for v, weight in graph[u]:
                    if weight < 0:  # Negative weight edge
                        if u == x:
                            reachable_from_x.add(v)
                        if v == y:
                            reachable_to_y.add(u)
            if reachable_from_x and reachable_to_y:
                return (x, reachable_from_x, y)
    return None

def find_independent_set(graph, k):
    # Randomized approach to find a 1-hop independent set
    independent_set = set()
    n = len(graph)
    for u in range(n):
        is_independent = True
        for v in independent_set:
            if (u, v) in graph or (v, u) in graph:
                is_independent = False
                break
        if is_independent:
            independent_set.add(u)
        if len(independent_set) >= k:
            break
    return independent_set

def eliminate_negative_edges(graph, k):
    negative_edges = [(u, v, w) for u in range(len(graph)) for v, w in graph[u] if w < 0]
    eliminated_edges = random.sample(negative_edges, min(k, len(negative_edges)))
    for edge in eliminated_edges:
        u, v, _ = edge
        graph[u] = [(v2, w) for v2, w in graph[u] if v2 != v]
    return graph, eliminated_edges

def randomized_sssp(graph, source, max_hops, k):
    dist = hop_limited_bfd(graph, source, max_hops)
    
    # Eliminate negative edges
    graph, eliminated_edges = eliminate_negative_edges(graph, k)
    
    # Apply price function to eliminate negative edges
    phi = price_function(graph, source)
    graph = apply_price_function(graph, phi)
    
    # Betweenness reduction
    phi = betweenness_reduction(graph, 0.1, 5)
    graph = apply_price_function(graph, phi)
    
    return dist, eliminated_edges, graph


def generate_random_graph(n, m, negative_percentage=0.3):
    graph = {i: [] for i in range(n)}
    for _ in range(m):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        weight = random.randint(-10, 10) if random.random() < negative_percentage else random.randint(0, 10)
        graph[u].append((v, weight))
    return graph

# Compare Bellman-Ford with Randomized SSSP and plot the runtime
def compare_algorithms_and_plot(n_values, m_values, negative_percentage=0.3):
    bf_times = []
    randomized_times = []

    for n, m in zip(n_values, m_values):
        graph = generate_random_graph(n, m, negative_percentage)
        
        # Bellman-Ford Algorithm
        start_time = time.time()
        bellman_ford_result = bellman_ford(graph, 0)
        bf_time = time.time() - start_time
        bf_times.append(bf_time)
        
        # Randomized SSSP
        start_time = time.time()
        randomized_result, eliminated_edges, new_graph = randomized_sssp(graph, 0, 5, 10)
        randomized_time = time.time() - start_time
        randomized_times.append(randomized_time)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, bf_times, label='Bellman-Ford Time', color='blue', marker='o')
    plt.plot(n_values, randomized_times, label='Randomized SSSP Time', color='red', marker='x')
    
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Comparison of Bellman-Ford and Randomized SSSP Algorithms')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example Usage: Test with different graph sizes
n_values = [10, 20, 30, 40, 50]
m_values = [20, 40, 60, 80, 100]  # Number of edges (m) corresponding to n values

# Test for dense graphs with many negative edges
compare_algorithms_and_plot(n_values, m_values, negative_percentage=0.4)

# Test for sparse graphs with fewer negative edges
compare_algorithms_and_plot(n_values, m_values, negative_percentage=0.1)