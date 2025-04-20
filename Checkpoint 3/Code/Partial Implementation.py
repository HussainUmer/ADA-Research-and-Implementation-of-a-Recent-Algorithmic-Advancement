import random
import time
import matplotlib.pyplot as plt
import math

# Bellman-Ford Algorithm (Classic)
def bellman_ford(graph, source):
    n = len(graph)
    dist = {v: math.inf for v in range(n)}
    dist[source] = 0
    
    for _ in range(n - 1):
        for u in range(n):
            for v, weight in graph[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
    
    for u in range(n):
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                print("Graph contains negative weight cycle")
                return None
    
    return dist


# Randomized SSSP Algorithm (Simplified)
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


def eliminate_negative_edges(graph, negative_edges, k):
    if len(negative_edges) == 0:
        print("No negative edges to eliminate.")
        return []
    
    eliminated_edges = []
    for _ in range(k):
        if not negative_edges:
            break
        edge = random.choice(negative_edges)
        eliminated_edges.append(edge)
        negative_edges.remove(edge)
    
    return eliminated_edges


def randomized_sssp(graph, source, max_hops, k):
    dist = hop_limited_bfd(graph, source, max_hops)
    
    negative_edges = [(u, v, w) for u in range(len(graph)) for v, w in graph[u] if w < 0]
    eliminated_edges = eliminate_negative_edges(graph, negative_edges, k)
    
    return dist, eliminated_edges


# Function to generate random graph
def generate_random_graph(n, m):
    graph = {i: [] for i in range(n)}
    for _ in range(m):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        weight = random.randint(-10, 10)  # Allow negative edge weights
        graph[u].append((v, weight))
    return graph


# Function to compare both algorithms and plot
def compare_algorithms_and_plot(n_values, m_values):
    bf_times = []
    randomized_times = []

    for n, m in zip(n_values, m_values):
        graph = generate_random_graph(n, m)
        
        # Bellman-Ford Algorithm
        start_time = time.time()
        bellman_ford_result = bellman_ford(graph, 0)
        bf_time = time.time() - start_time
        bf_times.append(bf_time)
        
        # Randomized SSSP
        start_time = time.time()
        randomized_result, eliminated_edges = randomized_sssp(graph, 0, 5, 10)
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

compare_algorithms_and_plot(n_values, m_values)
