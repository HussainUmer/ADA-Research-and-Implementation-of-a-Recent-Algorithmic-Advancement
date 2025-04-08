# Single-Source Shortest Paths with Negative Real Weights in Õ(mn^{8/9}) Time

The paper addresses the problem of computing single-source shortest paths (SSSP) on directed graphs with real edge weights, including both positive and negative values. The classic Bellman-Ford algorithm for this problem runs in \(O(mn)\) time, where \(m\) is the number of edges and \(n\) is the number of vertices. This paper introduces a randomized algorithm that improves upon the Bellman-Ford algorithm by leveraging Djisktra Algorithm, achieving a time complexity of \(Õ(mn^{8/9})\), marking the first asymptotic improvement in the problem.

The main contribution of the paper is the development of a randomized algorithm that solves the SSSP problem for real-weighted graphs with high probability in the improved time complexity.
