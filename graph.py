"""
SDN Controller - CSC 4501 Assignment 4 Question 4

My watermark: e1e0c75d90c897db62e9ec7780ee9f5f9d2f42a5b0629d9d46fa40f01d7cee7c
[SHA-256 hash combining 898213621 (Student ID) with "NeoDDaBRgX5a9"]
"""

class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, node):
        self.adj.setdefault(node, {})

    def remove_node(self, node):
        if node in self.adj:
            for nbr in list(self.adj[node].keys()):
                del self.adj[nbr][node]
            del self.adj[node]

    def add_link(self, u, v, weight=1):
        self.add_node(u); self.add_node(v)
        self.adj[u][v] = weight
        self.adj[v][u] = weight

    def remove_link(self, u, v):
        self.adj.get(u, {}).pop(v, None)
        self.adj.get(v, {}).pop(u, None)

    def neighbors(self, u):
        return self.adj.get(u, {}).items()

    def nodes(self):
        return list(self.adj.keys())