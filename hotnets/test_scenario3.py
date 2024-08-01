#!/usr/bin/env python

"""
An Simple example of an AS with two providers and one customer
The policy is such that the customer traffic prefer once provider over the other
And providers cannot use the network as transit.

       +-------------+        +-------------+
       | Provider1   |        | Provider2   |     Provider1, Provider2
       | 10.0.0.2 R1 |        | 10.0.0.4 R2 |     network1: 128.0.0.0/24
       +-------------+        +-------------+
              | AS 400               | AS 500
              | 100:1                | 100:2
    +--------|||---------------------|---------+
    |  +-------------+        +-------------+  |  Routing Policy
    |  | R1 10.0.0.3 |--------| R2 10.0.0.5 |  |  Rule 1: path1 == path2 >> 
    |  | 192.168.1.1 |        | 192.168.0.1 |  |          path3 == path4
    |  +-------------+        +-------------+  |  Rule 3: block [P2, R2, R1, P1]
    |         |                      |         |  Rule 4:
    |         |    +-------------+   |         |
    |         +----| R3 10.0.0.1 |=--+         |
    | 100:1 => 200 | 192.168.2.1 |=            |
    | 100:2 => 100 +-------------+      AS 100 |
    +---------------------|--------------------+
                          |
                   +-------------+
                   | Cutomer     |                Customer
                   | 10.0.0.0 R3 |                network2: 128.0.1.0/24
                   +-------------+ AS 600

    Provider1 (Fa0/0 10.0.0.2/31) <--> R1 (Fa0/0 10.0.0.3/31)
    Provider1 (lo100 128.0.0.1/32)

    Provider2 (Fa0/0 10.0.0.4/31) <--> R2 (Fa0/0 10.0.0.5/31)
    Provider2 (lo100 128.0.0.1/32)

    Customer  (Fa0/0 10.0.0.0/31) <--> R3 (Fa0/0 10.0.0.1/31)
    Customer  (lo100 128.0.1.1/32)

    R1 (Fa0/0 10.0.0.3/31)  <--> Provider1 (Fa0/0 10.0.0.2/31)
    R1 (Fa0/1 10.0.0.11/31) <--> R2 (Fa0/1 10.0.0.10/31)
    R1 (Fa1/0 10.0.0.7/31)  <--> R3 (Fa0/1 10.0.0.6/31)
    R1 (lo100 192.168.1.1/32)

    R2 (Fa0/0 10.0.0.5/31)  <--> Provider2 (Fa0/0 10.0.0.4/31)
    R2 (Fa0/1 10.0.0.10/31) <--> R1 (Fa0/1 10.0.0.11/31)
    R2 (Fa1/0 10.0.0.9/31)  <--> R3 (Fa1/0 10.0.0.8/31)
    R2 (lo100 192.168.0.1/32)Cutomer

    R3 (Fa0/0 10.0.0.1/31)  <--> Customer  (Fa0/0 10.0.0.0/31)
    R3 (Fa0/1 10.0.0.6/31)  <--> R1 (Fa1/0 10.0.0.7/31)
    R3 (Fa1/0 10.0.0.8/31)  <--> R2 (Fa1/0 10.0.0.9/31)
    R3 (lo100 192.168.2.1/32)

ERROR - netcomplete.py - raise SketchError(err)
synet.netcomplete.SketchError: The following next hop IP addresses are not announced
via IGP protocol, Hence the BGP requirements cannot be satisfied (consider announcing
them in OSPF or static routes): ['R2->Provider2:Fa0/0-10.0.0.4/31', 'R3->Provider2:
Fa0/0-10.0.0.4/31', 'R3->Provider2:Fa0/0-10.0.0.4/31']
"""

import argparse
import logging
from ipaddress import ip_interface
from ipaddress import ip_network
import json
import os

from synet.utils.common import PathReq
from synet.utils.common import PathOrderReq
from synet.utils.common import KConnectedPathsReq
from synet.utils.common import Protocols

from tekton.utils import VALUENOTSET

from tekton.bgp import BGP_ATTRS_ORIGIN
# from tekton.bgp import Access
from tekton.bgp import RouteMapLine
from tekton.bgp import RouteMap
from tekton.bgp import Announcement
from tekton.bgp import Community
from tekton.bgp import CommunityList
from tekton.bgp import IpPrefixList
from tekton.bgp import MatchCommunitiesList
from tekton.bgp import MatchIpPrefixListList
from tekton.bgp import MatchPermitted
from tekton.bgp import ActionSetCommunity
from tekton.bgp import ActionSetLocalPref
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


def test_bgp_example(output_dir):
    # Generate the basic network of three routers
    # generate a full mesh topology, mesh_size = 3, asnum = 100
    graph = gen_mesh(3, 100)
    # node: R1, R2, R3
    r1, r2, r3 = 'R1', 'R2', 'R3'

    # Enable OSPF in the sketch
    for node in graph.local_routers_iter():
        graph.enable_ospf(node, 100)
    # Edge weights are symbolic
    for src, dst in graph.edges():
        graph.set_edge_ospf_cost(src, dst, VALUENOTSET)
    graph.set_loopback_addr(r1, 'lo100', VALUENOTSET)
    graph.set_loopback_addr(r2, 'lo100', VALUENOTSET)
    graph.add_ospf_network(r1, 'lo100', '0.0.0.0')
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
    graph.set_bgp_asnum(provider1, 400)
    graph.set_bgp_asnum(provider2, 500)
    graph.set_bgp_asnum(customer, 600)
    graph.add_peer_edge(r1, provider1)
    graph.add_peer_edge(provider1, r1)
    graph.add_peer_edge(r2, provider2)
    graph.add_peer_edge(provider2, r2)
    graph.add_peer_edge(r3, customer)
    graph.add_peer_edge(customer, r3)

    # Establish BGP peering
    graph.add_bgp_neighbor(provider1, r1)
    graph.add_bgp_neighbor(provider2, r2)
    graph.add_bgp_neighbor(customer, r3)

    # The traffic class announced by the two providers
    net1 = ip_network(u'128.0.0.0/24')
    # The traffic class announced by the customer
    net2 = ip_network(u'128.0.1.0/24')

    prefix1 = str(net1)
    prefix2 = str(net2)
    # Known communities 100:1, 100:2, 100:3
    comms = [Community("100:{}".format(c)) for c in range(1, 4)]
    # The symbolic announcement injected by provider1
    ann1 = Announcement(prefix=prefix1,
                        peer=provider1,
                        origin=BGP_ATTRS_ORIGIN.INCOMPLETE,
                        as_path=[5000],  # We assume it learned from other upstream ASes
                        as_path_len=1,
                        # next_hop='0.0.0.0',
                        next_hop='{}Hop'.format(provider1),
                        local_pref=100,
                        med=100,
                        # communities=dict([(c, False) for c in comms]),
                        communities=dict([(c, True) for c in comms]),
                        permitted=True)
    # The symbolic announcement injected by provider1
    # Note it has a shorter AS Path
    ann2 = Announcement(prefix=prefix1,
                        peer=provider2,
                        origin=BGP_ATTRS_ORIGIN.INCOMPLETE,
                        as_path=[3000, 5000],  # We assume it learned from other upstream ASes
                        as_path_len=2,
                        # next_hop='0.0.0.0',
                        next_hop='{}Hop'.format(provider2),
                        local_pref=100,
                        med=100,
                        # communities=dict([(c, False) for c in comms]),
                        communities=dict([(c, True) for c in comms]),
                        permitted=True)
    # The symbolic announcement injected by customer
    ann3 = Announcement(prefix=prefix2,
                        peer=customer,
                        origin=BGP_ATTRS_ORIGIN.INCOMPLETE,
                        as_path=[],
                        as_path_len=0,
                        next_hop='0.0.0.0',
                        # next_hop='{}Hop'.format(customer),
                        local_pref=100,
                        med=100,
                        # communities=dict([(c, False) for c in comms]),
                        communities=dict([(c, True) for c in comms]),
                        permitted=True)

    graph.add_bgp_advertise(provider1, ann1, loopback='lo100')
    graph.set_loopback_addr(provider1, 'lo100', ip_interface(net1.hosts().next()))

    graph.add_bgp_advertise(provider2, ann2, loopback='lo100')
    graph.set_loopback_addr(provider2, 'lo100', ip_interface(net1.hosts().next()))

    graph.add_bgp_advertise(customer, ann3, loopback='lo100')
    graph.set_loopback_addr(customer, 'lo100', ip_interface(net2.hosts().next()))

    ########################## Configuration sketch ###############################

    for local, peer in [(r1, provider1)]:
        from tekton.bgp import Access
        imp_name = "{}_import_from_{}".format(local, peer)
        exp_name = "{}_export_to_{}".format(local, peer)
        comm1 = Community(value="100:1")
        comm2 = Community(value="100:2")
        # TODO ip prefix-list network/len {permit|deny}
        # network: destination network or source network
        # prefix_list = IpPrefixList(name="Provider1_to_Customer", access=Access.permit, networks=[net2])
        prefix_list = IpPrefixList(name="Provider1_to_Customer", access=Access.permit, networks=[net1])
        match_prefix_list = MatchIpPrefixListList(prefix_list=prefix_list)
        # match_permitted = MatchPermitted(access=Access.permit)
        action_set_community = ActionSetCommunity(communities=[comm1])
        rline1 = RouteMapLine(matches=[match_prefix_list], actions=[action_set_community], access=Access.permit, lineno=10)
        # rline1 = RouteMapLine(matches=[match_permitted], actions=[action_set_community], access=Access.permit, lineno=10)
        rline2 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        rmap_import = RouteMap(name=imp_name, lines=[rline1, rline2])
        comm1_list = CommunityList(list_id=1, access=Access.permit, communities=[comm1])
        comm2_list = CommunityList(list_id=2, access=Access.permit, communities=[comm2])
        match_comm1_list = MatchCommunitiesList(communities_list=comm1_list)
        match_comm2_list = MatchCommunitiesList(communities_list=comm2_list)
        # rline3 = RouteMapLine(matches=[match_comm2_list], actions=[], access=Access.deny, lineno=10)
        # rline4 = RouteMapLine(matches=[match_comm1_list], actions=[], access=Access.deny, lineno=20)
        # rline5 = RouteMapLine(matches=[], actions=[], access=Access.permit, lineno=30)
        # rline6 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        # rmap_export = RouteMap(name=exp_name, lines=[rline3, rline4, rline5, rline6])
        # TODO full-configs-simple
        # rline3 = RouteMapLine(matches=[match_comm2_list], actions=[], access=Access.deny, lineno=10)
        # rline4 = RouteMapLine(matches=[], actions=[], access=Access.permit, lineno=20)
        # rline5 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        # rmap_export = RouteMap(name=exp_name, lines=[rline3, rline4, rline5])
        # TODO holes-configs-simple-nexthop (select one)
        rmap_export = RouteMap.generate_symbolic(name=exp_name, graph=graph, router=local)
        # TODO holes-configs-simple-community
        # comm_list = CommunityList(list_id=1, access=Access.permit, communities=[VALUENOTSET])
        # match_comm_list = MatchCommunitiesList(communities_list=comm_list)
        # rline3 = RouteMapLine(matches=[match_comm_list], actions=[], access=VALUENOTSET, lineno=10)
        # rline4 = RouteMapLine(matches=[], actions=[], access=Access.permit, lineno=20)
        # rline5 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        # rmap_export = RouteMap(name=exp_name, lines=[rline3, rline4, rline5])
        # TODO deny all traffic
        # rline1 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=10)
        # rmap_export = RouteMap(name=exp_name, lines=[rline1])
        graph.add_route_map(local, rmap_import)
        graph.add_route_map(local, rmap_export)
        graph.add_bgp_import_route_map(local, peer, rmap_import.name)
        graph.add_bgp_export_route_map(local, peer, rmap_export.name)

    for local, peer in [(r2, provider2)]:
        from tekton.bgp import Access
        imp_name = "{}_import_from_{}".format(local, peer)
        exp_name = "{}_export_to_{}".format(local, peer)
        comm1 = Community(value="100:1")
        comm2 = Community(value="100:2")
        # TODO ip prefix-list network/len {permit|deny}
        # network: destination network or source network
        # prefix_list = IpPrefixList(name="Provider2_to_Customer", access=Access.permit, networks=[net2])
        prefix_list = IpPrefixList(name="Provider2_to_Customer", access=Access.permit, networks=[net1])
        match_prefix_list = MatchIpPrefixListList(prefix_list=prefix_list)
        # match_permitted = MatchPermitted(access=Access.permit)
        action_set_community = ActionSetCommunity(communities=[comm2])
        rline1 = RouteMapLine(matches=[match_prefix_list], actions=[action_set_community], access=Access.permit, lineno=10)
        # rline1 = RouteMapLine(matches=[match_permitted], actions=[action_set_community], access=Access.permit, lineno=10)
        rline2 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        rmap_import = RouteMap(name=imp_name, lines=[rline1, rline2])
        comm1_list = CommunityList(list_id=1, access=Access.permit, communities=[comm1])
        comm2_list = CommunityList(list_id=2, access=Access.permit, communities=[comm2])
        match_comm1_list = MatchCommunitiesList(communities_list=comm1_list)
        match_comm2_list = MatchCommunitiesList(communities_list=comm2_list)
        # rline3 = RouteMapLine(matches=[match_comm1_list], actions=[], access=Access.deny, lineno=10)
        # rline4 = RouteMapLine(matches=[match_comm2_list], actions=[], access=Access.deny, lineno=20)
        # rline5 = RouteMapLine(matches=[], actions=[], access=Access.permit, lineno=30)
        # rline6 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        # rmap_export = RouteMap(name=exp_name, lines=[rline3, rline4, rline5, rline6])
        rline3 = RouteMapLine(matches=[match_comm1_list], actions=[], access=Access.deny, lineno=10)
        rline4 = RouteMapLine(matches=[], actions=[], access=Access.permit, lineno=20)
        rline5 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        rmap_export = RouteMap(name=exp_name, lines=[rline3, rline4, rline5])
        graph.add_route_map(local, rmap_import)
        graph.add_route_map(local, rmap_export)
        graph.add_bgp_import_route_map(local, peer, rmap_import.name)
        graph.add_bgp_export_route_map(local, peer, rmap_export.name)

    """
    for local, peer in [(r3, r1), (r3, r2)]:
        from tekton.bgp import Access
        imp_name = "{}_import_from_{}".format(local, peer)
        # exp_name = "{}_export_to_{}".format(local, peer)
        comm1 = Community(value="100:1")
        comm2 = Community(value="100:2")
        comm1_list = CommunityList(list_id=1, access=Access.permit, communities=[comm1])
        comm2_list = CommunityList(list_id=2, access=Access.permit, communities=[comm2])
        match_comm1_list = MatchCommunitiesList(communities_list=comm1_list)
        match_comm2_list = MatchCommunitiesList(communities_list=comm2_list)
        action_set_localpref100 = ActionSetLocalPref(local_pref=100)
        action_set_localpref200 = ActionSetLocalPref(local_pref=200)
        rline1 = RouteMapLine(matches=[match_comm1_list], actions=[action_set_localpref200], access=Access.permit, lineno=10)
        rline2 = RouteMapLine(matches=[match_comm2_list], actions=[action_set_localpref100], access=Access.permit, lineno=20)
        rline3 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        rmap_import = RouteMap(name=imp_name, lines=[rline1, rline2, rline3])
        graph.add_route_map(local, rmap_import)
        # graph.add_route_map(local, rmap_export)
        graph.add_bgp_import_route_map(local, peer, rmap_import.name)
        # graph.add_bgp_export_route_map(local, peer, rmap_export.name)
    """

    """
    for local, peer in [(r3, r1)]:
        from tekton.bgp import Access
        exp_name = "{}_export_to_{}".format(local, peer)
        comm2 = Community(value="100:2")
        comm2_list = CommunityList(list_id=2, access=Access.permit, communities=[comm2])
        match_comm2_list = MatchCommunitiesList(communities_list=comm2_list)
        rline1 = RouteMapLine(matches=[match_comm2_list], actions=[], access=Access.deny, lineno=10)
        rline2 = RouteMapLine(matches=[], actions=[], access=Access.permit, lineno=20)
        rline3 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        rmap_export = RouteMap(name=exp_name, lines=[rline1, rline2, rline3])
        # graph.add_route_map(local, rmap_import)
        graph.add_route_map(local, rmap_export)
        # graph.add_bgp_import_route_map(local, peer, rmap_import.name)
        graph.add_bgp_export_route_map(local, peer, rmap_export.name)

    for local, peer in [(r3, r2)]:
        from tekton.bgp import Access
        exp_name = "{}_export_to_{}".format(local, peer)
        comm1 = Community(value="100:1")
        comm1_list = CommunityList(list_id=1, access=Access.permit, communities=[comm1])
        match_comm1_list = MatchCommunitiesList(communities_list=comm1_list)
        rline1 = RouteMapLine(matches=[match_comm1_list], actions=[], access=Access.deny, lineno=10)
        rline2 = RouteMapLine(matches=[], actions=[], access=Access.permit, lineno=20)
        rline3 = RouteMapLine(matches=[], actions=[], access=Access.deny, lineno=100)
        rmap_export = RouteMap(name=exp_name, lines=[rline1, rline2, rline3])
        # graph.add_route_map(local, rmap_import)
        graph.add_route_map(local, rmap_export)
        # graph.add_bgp_import_route_map(local, peer, rmap_import.name)
        graph.add_bgp_export_route_map(local, peer, rmap_export.name)
    """

    """
    for local, peer in [(r3, r1), (r3, r2)]:
        imp_name = "{}_import_from_{}".format(local, peer)
        exp_name = "{}_export_to_{}".format(local, peer)
        # generate route map
        imp = RouteMap.generate_symbolic(name=imp_name, graph=graph, router=local)
        exp = RouteMap.generate_symbolic(name=exp_name, graph=graph, router=local)
        graph.add_bgp_import_route_map(local, peer, imp.name)
        graph.add_bgp_export_route_map(local, peer, exp.name)
    """

    ############################### Requirements ##################################

    # PathReq class
    #   Input params: protocol, dst_net, path, strict
    #     (path (route path, such as [r1, r2, r3]))
    #     (strict=True traffic should be dropped when path is not available)
    # ECMPPathsReq class
    #   Input params: protocol, dst_net, paths, strict
    #     (paths (pathreq list))
    #     (must have some dst_net and strict=False)
    # KConnectedPathsReq class
    #   Input params: protocol, dst_net, paths, strict
    #     (paths (PathReq list))
    #     (must have some dst_net and strict=False)
    # PreferredPathReq class
    #   Input params: protocol, dst_net, kconnected, strict
    #     (kconnected (KConnectPathReq))
    #     (must have some dst_net and strict=False)
    # PathOrderReq class
    #   Input params: protocol, dst_net, paths, strict
    #     (paths (involve PathReq and KConnectPathReq list))
    #     (must have some dst_net and strict=False)

    # Block

    # DstNet (map key) -> Lists of Reqs (map value)
    # only one DstNet is prefix1
    # prefix1 -> PathOrderReq(Protocols.BGP, prefix1, [KConnectedPathsReq, ...], ...)

    # extract_reqs: reqs => as_paths and router_paths (reversed & deduplicate)
    # + as_paths
    #   [set([(p1, (AS400, AS100, AS600)), (p1, (AS400, AS100))]),
    #    set([(p2, (AS500, AS100, AS600)), (p2, (AS500, AS100))])]
    # + router_paths, {p1: provider1, p2: provider2, c: customer}
    #   [set([(p1, (p1, r2, r1, c)), (p1, (p1, r2, r3, r1, c)), (p1, (p1, r2, r1, r3))]),
    #    set([(p2, (p2, r3, r1, c)), (p2, (p2, r3, r2, r1, c)), (p2, (p2, r3, r1, r2))])]

    # _extract_peering_graph: network_graph => undirected graph (asnum)
    # + undirected graph (asnum)                            400--100--500
    #   node: as400, as500, as100, as600                          |
    #   edge: (as400, as100), (as500, as100), (as100, as600)     600 (asnum)

    # compute_propagation: graph, ordered_paths => propagation graph (asnum or router)
    # * graph: undirected graph (asnum) via _extract_peering_graph
    # * ordered_paths: as_paths via extract_reqs
    # + directed graph, propagation graph (asnum)
    #   node: as400, as500, as100, as600
    #   edge: <as400, as100>, <as500, as100>, <as100, as600>
    #   as400.paths: set([(as400,)])
    #   as400.order: [set([(as400,)]), set([])]
    #   as400.block: set([(as400, as100, as500)])
    #   as500.paths: set([(as500,)])
    #   as500.order: [set([]), set([(as500,)])]
    #   as500.block: set([(as500, as100, as400)])
    #   as100.paths: set([(as400, as100), (as500, as100)])
    #   as100.order: [set([(as400, as100)]), set([(as500, as100)])]
    #   as100.block: set([])
    #   as600.paths: set([(as400, as100, as600), (as500, as100, as600)])
    #   as600.order: [set([(as400, as100, as600)]), set([]), 
    #                 set([(as500, as100, as600)]), set([])]
    #   as600.block: set([])
    #   set(flatten(flatten(as400.order))) => set([as400])
    #   set(flatten(flatten(as500.order))) => set([as500])
    #   set(flatten(flatten(as100.order))) => set([as400, as100, as500])
    #   set(flatten(flatten(as600.order))) => set([as400, as100, as600, as500])
    # + directed graph, propagation graph (router)
    #   omitting ...

    # node: r1, r2, r3, p1, p2, c

    # (path1 = path2 = path3) >> (path4 = path5 = path6)

    # path = p1, r2, r1, c => (p1, r2), (r2, r1), (r1, c)
    # r3, p2

    # r1[prefix1]['paths']  reversed set(path1, ... path6)
    # r1[prefix1]['order']           set(path1, ... path3), set(path4, ..., path6)
    # r1[prefix1]['block']           set(other path1, other path2)

    # assert announcements
    # r1[prefix1]['paths_info']      set(path1+, ..., path6+) 
    # r1[prefix1]['order_info']      set(path1+, ..., path3+), set(path4+, ..., path6+)
    # r1[prefix1]['block_info']      set(other path1+, other path2+)


    path1 = PathReq(Protocols.BGP, prefix1, [customer, r3, r1, provider1], False)
    path2 = PathReq(Protocols.BGP, prefix1, [customer, r3, r2, r1, provider1], False)
    path3 = PathReq(Protocols.BGP, prefix1, [r2, r3, r1, provider1], False)

    path4 = PathReq(Protocols.BGP, prefix1, [customer, r3, r2, provider2], False)
    path5 = PathReq(Protocols.BGP, prefix1, [customer, r3, r1, r2, provider2], False)
    path6 = PathReq(Protocols.BGP, prefix1, [r1, r3, r2, provider2], False)
    # path6 = PathReq(Protocols.BGP, prefix1, [provider1, r1, r2, provider2], False)

    reqs = [
        PathOrderReq(
            Protocols.BGP,
            prefix1,
            [
                KConnectedPathsReq(Protocols.BGP, prefix1, [path1, path2, path3], False),
                KConnectedPathsReq(Protocols.BGP, prefix1, [path4, path5, path6], False),
                # KConnectedPathsReq(Protocols.BGP, prefix1, [path1, path2], False),
                # KConnectedPathsReq(Protocols.BGP, prefix1, [path4, path5], False),
            ],
            False
        ),
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

    ############################### Print Graph ###################################

    r1_route_maps_dict = graph.get_route_maps(r1)
    print "=" * 20 + " R1 route maps " + "=" * 15
    print r1_route_maps_dict

    r2_route_maps_dict = graph.get_route_maps(r2)
    print "=" * 20 + " R2 route maps " + "=" * 15
    print r2_route_maps_dict

    r3_route_maps_dict = graph.get_route_maps(r3)
    print "=" * 20 + " R3 route maps " + "=" * 15
    print r3_route_maps_dict

    provider1_route_maps_dict = graph.get_route_maps(provider1)
    print "=" * 20 + " Provider1 route maps " + "=" * 8
    print provider1_route_maps_dict

    provider2_route_maps_dict = graph.get_route_maps(provider2)
    print "=" * 20 + " Provider2 route maps " + "=" * 8
    print provider2_route_maps_dict

    customer_route_maps_dict = graph.get_route_maps(customer)
    print "=" * 20 + " Customer route maps " + "=" * 9
    print customer_route_maps_dict

    ############################### NetComplete ###################################

    external_anns = [ann1, ann2, ann3]
    netcomplete = NetComplete(reqs=reqs, topo=graph, external_announcements=external_anns)
    netcomplete.synthesize()
    netcomplete.write_configs(output_dir=output_dir)

    # added by yongzheng for remind the example finish
    print "========the example test_simple.py finish========="


if __name__ == '__main__':
    setup_logging()
    parser = argparse.ArgumentParser(description='BGP customer peer example.')
    parser.add_argument('outdir', type=str, help='output directory for the configuration')
    args = parser.parse_args()
    test_bgp_example(args.outdir)
