"""
SDN Controller - CSC 4501 Assignment 4 Question 4

My watermark: e1e0c75d90c897db62e9ec7780ee9f5f9d2f42a5b0629d9d46fa40f01d7cee7c
[SHA-256 hash combining 898213621 (Student ID) with "NeoDDaBRgX5a9"]
"""

import heapq
import random
import time
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt

class SDNController:
    def __init__(self, topology):
        self.topo = topology
        self.tables = {}
        self.active_flows = []
        self.critical_flows = set([('H2', 'S4')])
        self.install_flows()

    def compute_shortest_paths(self, src):
        dist = {n: float('inf') for n in self.topo.nodes()}
        prev = {n: None for n in self.topo.nodes()}
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v, w in self.topo.neighbors(u):
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        return dist, prev

    def compute_equal_cost_next_hops(self, sw, dst, dist):
        nxt = []
        for v, w in self.topo.neighbors(sw):
            if dist.get(v, float('inf')) + w == dist.get(dst, float('inf')):
                nxt.append(v)
        return nxt

    def install_flows(self):
        self.tables = {n: [] for n in self.topo.nodes()}
        all_dist = {}
        for sw in self.topo.nodes():
            dist, _ = self.compute_shortest_paths(sw)
            all_dist[sw] = dist

        for sw in self.topo.nodes():
            dist = all_dist[sw]
            for dst in self.topo.nodes():
                if dst == sw or dist[dst] == float('inf'): continue
                primaries = self.compute_equal_cost_next_hops(sw, dst, dist)
                random.shuffle(primaries)
                entry = {
                    'match_dst': dst,
                    'action': primaries,
                    'priority': 'normal'
                }
                for src, d in self.active_flows:
                    if d == dst:
                        entry['priority'] = 'high'
                for src, d in self.active_flows:
                    if (src, d) in self.critical_flows and len(primaries) > 1:
                        entry['backup'] = primaries[1:]
                self.tables[sw].append(entry)

    def remove_link_and_reconfigure(self, u, v):
        print(f"[{time.strftime('%H:%M:%S')}] Removing link {u}<->{v} and reconfiguring...")
        self.topo.remove_link(u, v)
        self.install_flows()

    def compute_path(self, src, dst):
        dist, prev = self.compute_shortest_paths(src)
        if dist[dst] == float('inf'):
            return None
        path = []
        cur = dst
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        return list(reversed(path))

    def show_tables(self):
        for sw, flows in self.tables.items():
            print(f"Switch {sw} flow table:")
            for e in flows:
                line = f"  dst={e['match_dst']} | next_hops={e['action']} | prio={e['priority']}"
                if 'backup' in e:
                    line += f" | backup={e['backup']}"
                print(line)
            print()

    def visualize(self):
        G = nx.Graph()
        for u in self.topo.nodes():
            G.add_node(u)
        for u, nbrs in self.topo.adj.items():
            for v in nbrs:
                G.add_edge(u, v)
        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='aquamarine')

        util = defaultdict(int)
        flow_edges = []
        for src, dst in self.active_flows:
            path = self.compute_path(src, dst)
            if path:
                for i in range(len(path) - 1):
                    u, v = path[i], path[i+1]
                    flow_edges.append((u, v))
                    util[tuple(sorted((u, v)))] += 1

        nx.draw_networkx_edges(G, pos, edgelist=flow_edges,
                               edge_color='red', style='dashed', width=2)
        for (u, v), cnt in util.items():
            x_mid = (pos[u][0] + pos[v][0]) / 2
            y_mid = (pos[u][1] + pos[v][1]) / 2
            plt.text(x_mid, y_mid + 0.05, f"util={cnt}", fontsize=9, ha='center')

        plt.title('Topology with Active Flows & Link Utilization')
        plt.axis('off')
        filename = f"assignment_q4_output_{int(time.time())}.png"
        plt.savefig(filename)
        plt.close()
        print(f"Visualization saved to {filename}")