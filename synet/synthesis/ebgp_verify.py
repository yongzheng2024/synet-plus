# !/usr/bin/env python

"""check an eBGP peering graph assigned with path preferences"""

import networkx as nx

from synet.settings import *
from synet.utils.common import flatten


__author__ = "Ahmed El-Hassany"     # maintainer Yongzheng Zhang
__email__ = "a.hassany@gmail.com"   # yongzheng2024@outlook.com


class EBGPVerify(object):
    """verify the stability of the eBGP requirements"""

    def __init__(self, network_graph, reqs):
        """
        :param NetworkGraph network_graph: network topology, tekton.graph.NetworkGraph
        :param list reqs: bgp path requirements, list of BGP paths preferences
        """
        self.network_graph = network_graph
        self.reqs = reqs
        self.peering_graph = self._extract_peering_graph()

    def _extract_peering_graph(self):
        """
        extract the eBGP peering graph based AS number

        each node is an AS number, if the AS has multiple routers, then
        they are grouped into only one node

        :return: the eBGP peering graph based AS number
        :rtype: networkx.Graph (undirected graph, node(x.asnum), edge(x.asnum, y.asnum))
        """
        graph = nx.Graph()
        ases = {}  # ases (map): asnum -> the set of nodes with the same asnum
        for node in self.network_graph.routers_iter():
            if self.network_graph.is_bgp_enabled(node):
                asnum = self.network_graph.get_bgp_asnum(node)
                if asnum not in ases:
                    ases[asnum] = []
                ases[asnum].append(node)
        for asnum, routers in ases.iteritems():
            graph.add_node(asnum)
            for router in routers:
                for neighbor in self.network_graph.get_bgp_neighbors(router):
                    if not self.network_graph.is_bgp_enabled(neighbor):
                        # not BGP router
                        continue
                    n_asnum = self.network_graph.get_bgp_asnum(neighbor)
                    if asnum == n_asnum:
                        # BGP router is the in the same AS
                        continue
                    graph.add_edge(asnum, n_asnum)
        return graph

    def _get_segment(self, order_paths, split, node):
        """return the ordered segment at a node"""
        segment = []
        for paths in order_paths:
            current = set()
            for path in paths:
                if split in path:
                    current.add(path[:path.index(split) + 1])
                else:  # split not in path
                    if path[-1] == node:
                        current.add(tuple(list(path) + [split]))
                    else:
                        pass
            if current:
                if not segment or (segment and current != segment[-1]):
                    segment.append(current)
        return segment

    def check_order(self, graph):
        """check that the path preferences are implementable by BGP"""
        # TODO not understand
        unmatching_orders = []
        for node in graph.nodes():
            graph.node[node][ORDER] = [x for x in graph.node[node][ORDER] if x]
        for node in graph.nodes():
            preds = set(flatten(flatten(graph.node[node][ORDER])))
            for pred in preds:
                if pred == node:
                    continue
                # print "\t\tIn pred", pred
                if node in flatten(flatten(graph.node[pred][ORDER])):
                    segment = self._get_segment(graph.node[node][ORDER], pred, node)
                else:
                    segment = self._get_segment(graph.node[node][ORDER], pred, None)
                comp = graph.node[pred][ORDER][0]
                if segment[0] in graph.node[pred][ORDER]:
                    first_match = graph.node[pred][ORDER].index(segment[0])
                    comp = graph.node[pred][ORDER][first_match:len(segment) + 1]
                err = "node %s, pred %s: expected %s but found %s" % (node, pred, segment, comp)
                if segment != comp:
                    unmatching_orders.append((segment, comp, err))
        return unmatching_orders