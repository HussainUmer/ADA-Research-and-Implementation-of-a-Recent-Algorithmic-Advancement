# Single-Source Shortest Paths with Negative Real Weights in Õ(mn^{8/9}) Time

The paper addresses the problem of computing single-source shortest paths (SSSP) on directed graphs with real edge weights, including both positive and negative values. The classic Bellman-Ford algorithm for this problem runs in \(O(mn)\) time, where \(m\) is the number of edges and \(n\) is the number of vertices. This paper introduces a randomized algorithm that improves upon the Bellman-Ford algorithm by leveraging Djisktra Algorithm, achieving a time complexity of \(Õ(mn^{8/9})\), marking the first asymptotic improvement in the problem.

The main contribution of the paper is the development of a randomized algorithm that solves the SSSP problem for real-weighted graphs with high probability in the improved time complexity.


## How to Run the Code

There are two Python scripts available:

Partial Implementation: This script contains the core Randomized SSSP algorithm (without the full feature set).

To run the partial implementation, use the following command:
python partial_implementation.py

Full Implementation: This version includes the complete Randomized SSSP algorithm, including all steps (like negative edge elimination, price function reweighting, etc.).

To run the full implementation, use:
python full_implementation.py

## Modifying the Graph Inputs:
In both scripts, you can adjust the number of vertices (n_values) and edges (m_values) by changing the arrays. For example:

n_values = [10, 20, 30, 40, 50]  # Number of vertices

m_values = [20, 40, 60, 80, 100]  # Number of edges corresponding to n values

This will allow you to test the algorithm on different graph configurations.

Viewing Results

The script will automatically run both Bellman-Ford and Randomized SSSP algorithms and generate a plot comparing their execution times.

X-Axis: Number of Vertices (n)

Y-Axis: Time (seconds)

The plot will help visualize the performance differences between Bellman-Ford and Randomized SSSP.


## Video Presentation and Demo:
https://youtu.be/RQmtsodyyG0
