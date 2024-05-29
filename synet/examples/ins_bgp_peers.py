#!/usr/bin/env python

"""
An Simple example of an AS with two providers and one customer
The policy is such that the customer traffic prefer once provider over the other
And providers cannot use the network as transit

       +--------+        +--------+
       | AS 200 |    +---| AS 300 |    Provider
       +--------+    |   +--------+          
           |         |        |
           | +-------+        |
    +------|-|----------------|------+
    |  +--------+        +--------+  |
    |  |   R1   |--------|   R2   |  |
    |  +--------+        +--------+  |
    |      |                  |      |   Routing Policy
    |      |    +--------+    |      |   Rule 1: Traffic from the customer peer
    |      +----|   R3   |----+      |   AS100 to the external peers prefers exit
    |           +--------+    AS 400 |   routers in order: AS200, AS300 via R2, 
    +---------------|----------------+   AS300 via R1
                    |
                +--------+
                | AS 100 |             Customer
                +--------+
"""

import argparse
import logging
from ipaddress import ip_interface
from ipaddress import ip_network

from synet.utils.common import PathReq
from synet.utils.common import PathOrderReq
from synet.utils.common import KConnectedPathsReq
from synet.utils.common import Protocols

from tekton.utils import VALUENOTSET

from tekton.bgp import BGP_ATTRS_ORIGIN
from tekton.bgp import RouteMapLine
from tekton.bgp import RouteMap
from tekton.bgp import Announcement
from tekton.bgp import Community
from synet.netcomplete import NetComplete
from synet.utils.topo_gen import gen_mesh


def setup_logging():
    # create logger
    logger = logging.getLogger('synet')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


def bgp_example(output_dir):
    # Generate the basic network of three routers
    # generate a full mesh topology, mesh_size = 3, asnum = 400
    graph = gen_mesh(3, 400)
    # node: R1, R2, R3
    r1, r2, r3 = 'R1', 'R2', 'R3'

    # Enable OSPF in the sketch
    for node in graph.local_routers_iter():
        graph.enable_ospf(node, 400)
    # Edge weights are symbolic
    for src, dst in graph.edges():
        graph.set_edge_ospf_cost(src, dst, VALUENOTSET)
    graph.set_loopback_addr(r1, 'lo100', VALUENOTSET)
    graph.set_loopback_addr(r1, 'lo200', VALUENOTSET)
    graph.set_loopback_addr(r2, 'lo100', VALUENOTSET)
    graph.set_loopback_addr(r3, 'lo100', VALUENOTSET)
    graph.add_ospf_network(r1, 'lo100', '0.0.0.0')
    graph.add_ospf_network(r1, 'lo200', '0.0.0.0')
    graph.add_ospf_network(r2, 'lo100', '0.0.0.0')
    graph.add_ospf_network(r3, 'lo100', '0.0.0.0')
    graph.add_ospf_network(r1, 'Fa0/0', '0.0.0.0')
    graph.add_ospf_network(r2, 'Fa0/0', '0.0.0.0')
    graph.add_ospf_network(r3, 'Fa0/0', '0.0.0.0')

    # Add two providers and one customer
    provider1 = 'Provider1'
    provider2 = 'Provider2'
    customer = 'Customer'
    graph.add_peer(provider1)
    graph.add_peer(provider2)
    graph.add_peer(customer)
    graph.set_bgp_asnum(provider1, 200)
    graph.set_bgp_asnum(provider2, 300)
    graph.set_bgp_asnum(customer, 100)
    graph.add_peer_edge(r1, provider1)
    graph.add_peer_edge(provider1, r1)
    graph.add_peer_edge(r1, provider2)
    graph.add_peer_edge(provider2, r1)
    graph.add_peer_edge(r2, provider2)
    graph.add_peer_edge(provider2, r2)
    graph.add_peer_edge(r3, customer)
    graph.add_peer_edge(customer, r3)

    # Establish BGP peering
    graph.add_bgp_neighbor(provider1, r1)
    graph.add_bgp_neighbor(provider2, r1)
    graph.add_bgp_neighbor(provider2, r2)
    graph.add_bgp_neighbor(customer, r3)

    # The traffic class announced by the two providers
    net1 = ip_network(u'128.0.0.0/24')
    # The traffic class announced by the customer
    net2 = ip_network(u'128.0.1.0/24')

    prefix1 = str(net1)
    prefix2 = str(net2)
    # Known communities
    comms = [Community("100:{}".format(c)) for c in range(1, 4)]
    # The symbolic announcement injected by provider1
    ann1 = Announcement(prefix1,
                        peer=provider1,
                        origin=BGP_ATTRS_ORIGIN.INCOMPLETE,
                        as_path=[5000],  # We assume it learned from other upstream ASes
                        as_path_len=1,
                        #next_hop='0.0.0.0',
                        next_hop='{}Hop'.format(provider1),
                        local_pref=100,
                        med=100,
                        communities=dict([(c, False) for c in comms]),
                        permitted=True)
    # The symbolic announcement injected by provider1
    # Note it has a shorter AS Path
    ann2 = Announcement(prefix1,
                        peer=provider2,
                        origin=BGP_ATTRS_ORIGIN.INCOMPLETE,
                        as_path=[3000, 5000],  # We assume it learned from other upstream ASes
                        as_path_len=2,
                        next_hop='0.0.0.0',
                        local_pref=100,
                        med=100,
                        communities=dict([(c, False) for c in comms]),
                        permitted=True)
    # The symbolic announcement injected by customer
    ann3 = Announcement(prefix2,
                        peer=customer,
                        origin=BGP_ATTRS_ORIGIN.INCOMPLETE,
                        as_path=[],
                        as_path_len=0,
                        next_hop='0.0.0.0',
                        local_pref=100,
                        med=100,
                        communities=dict([(c, False) for c in comms]),
                        permitted=True)

    graph.add_bgp_advertise(provider1, ann1, loopback='lo100')
    graph.set_loopback_addr(provider1, 'lo100', ip_interface(net1.hosts().next()))

    graph.add_bgp_advertise(provider2, ann2, loopback='lo200')
    graph.set_loopback_addr(provider2, 'lo200', ip_interface(net1.hosts().next()))

    graph.add_bgp_advertise(provider2, ann2, loopback='lo100')
    graph.set_loopback_addr(provider2, 'lo100', ip_interface(net1.hosts().next()))

    graph.add_bgp_advertise(customer, ann3, loopback='lo100')
    graph.set_loopback_addr(customer, 'lo100', ip_interface(net2.hosts().next()))

    ########################## Configuration sketch ###############################

    for local, peer in [(r1, provider1), (r1, provider2), (r2, provider2)]:
        imp_name = "{}_import_from_{}".format(local, peer)
        exp_name = "{}_export_to_{}".format(local, peer)
        imp = RouteMap.generate_symbolic(name=imp_name, graph=graph, router=local)
        exp = RouteMap.generate_symbolic(name=exp_name, graph=graph, router=local)
        graph.add_bgp_import_route_map(local, peer, imp.name)
        graph.add_bgp_export_route_map(local, peer, exp.name)

    for local, peer in [(r1, r2), (r2, r1)]:
        # In Cisco the last line is a drop by default
        rline1 = RouteMapLine(matches=[], actions=[], access=VALUENOTSET, lineno=10)
        from tekton.bgp import Access
        rline2 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        rmap_export = RouteMap(name='{}_export_{}'.format(local, peer), lines=[rline1, rline2])
        graph.add_route_map(local, rmap_export)
        graph.add_bgp_export_route_map(local, peer, rmap_export.name)

    # Requirements
    path1 = PathReq(Protocols.BGP, prefix1, [customer, r3, r1, provider1], False)
    path2 = PathReq(Protocols.BGP, prefix1, [customer, r3, r2, r1, provider1], False)

    path3 = PathReq(Protocols.BGP, prefix1, [customer, r3, r2, provider2], False)
    path4 = PathReq(Protocols.BGP, prefix1, [customer, r3, r1, r2, provider2], False)

    path5 = PathReq(Protocols.BGP, prefix1, [customer, r3, r1, provider2], False)
    path6 = PathReq(Protocols.BGP, prefix1, [customer, r3, r2, r1, provider2], False)

    reqs = [
        PathOrderReq(
            Protocols.BGP,
            prefix1,
            [
                KConnectedPathsReq(Protocols.BGP, prefix1, [path1, path2], False),
                KConnectedPathsReq(Protocols.BGP, prefix1, [path3, path4], False),
                KConnectedPathsReq(Protocols.BGP, prefix1, [path5, path6], False),
            ],
            False),
        PathOrderReq(
            Protocols.OSPF,
            "dummy",
            [
                PathReq(Protocols.OSPF, "dummy", [r3, r1], False),
                PathReq(Protocols.OSPF, "dummy", [r3, r2, r1], False),
            ],
            False
        ),
        PathOrderReq(
            Protocols.OSPF,
            "dummy",
            [
                PathReq(Protocols.OSPF, "dummy", [r3, r2], False),
                PathReq(Protocols.OSPF, "dummy", [r3, r1, r2], False),
            ],
            False
        ),
    ]
    external_anns = [ann1, ann2, ann3]
    netcomplete = NetComplete(reqs=reqs, topo=graph, external_announcements=external_anns)
    netcomplete.synthesize()
    netcomplete.write_configs(output_dir=output_dir)

    # added by yongzheng for remind the example finish
    print "========the example ins_bgp_peers.py finish========"


if __name__ == '__main__':
    setup_logging()
    parser = argparse.ArgumentParser(description='BGP customer peer example.')
    parser.add_argument('outdir', type=str, help='output directory for the configuration')
    args = parser.parse_args()
    bgp_example(args.outdir)
