NetComplete
-----------

    Input: 
        * network topology
        * global path requirements ( with announcements, UPDATE message )
        * configuration sketch with holes ( with route map, involve VALUE?NOTSET )

    Intermediate data: 
        * node local path requirements attribute  ( paths, block, order )
        * node local announcements attribute      ( paths_info, block_info, order_info )
        * node local announcements dependency     ( origins )
        * smt.smt2 ( z3 solver & z3 check )

    Output: 
        * synthesized configuration

    Synthesis steps:
        * synthesis directly connected interfaces
        * compute propagation paths ( local path requirements, i.e. paths, block, order )
        * compute propagation infos ( i.e. paths_info, block_info, order_info, origins )
        * generate basic SMT variables
            + generate the SMT context and some SMT enum sort, 
              PrefixSort, NextHopSort, BGPOriginSort            ---> SMT enum sort
            + all propagation infos ( paths_info + block_info ) ---> SMT variables
        * synthesis configure sketch of BGP for each router
            + export route map for each router   ---> SMT variables and SMT constraints
              ( autonomous for each router, check permit route path or block route path )
            + set announcements ( from paths_info ) to permit   ---> SMT constraints
            + set announcements ( from block_info ) to block    ---> SMT constraints
            + import route map for each router   ---> SMT variables and SMT constraints
            + path preference for each router    ---> SMT variables and SMT constraints
              ( autonomous for each router, check order route path preference )
            + evaluate all SMT variables ( VALUE?NOTSET ) sequentially
              output smt.smt2 ( before SMT solver )
              output smt_solvered.smt2 ( after SMT solver )
            + generate synthesized router configuration of BGP
        * synthesis configure sketch of OSPF      (TODO)
        * synthesis directly connected interfaces (TODO)


Basic Data Struct
-----------------

    1. path requirement

        * PathReq class
            Input params: protocol, dst_net, path, strict
              (path (route path, such as [r1, r2, r3]))
              (strict=True traffic should be dropped when path is not available)
        * ECMPPathsReq class
            Input params: protocol, dst_net, paths, strict
              (paths (pathreq list))
              (must have some dst_net and strict=False)
        * KConnectedPathsReq class
            Input params: protocol, dst_net, paths, strict
              (paths (PathReq list))
              (must have some dst_net and strict=False)
        * PreferredPathReq class
            Input params: protocol, dst_net, kconnected, strict
              (kconnected (KConnectPathReq))
              (must have some dst_net and strict=False)
        * PathOrderReq class
            Input params: protocol, dst_net, paths, strict
              (paths (involve PathReq and KConnectPathReq list))
              (must have some dst_net and strict=False)

    ------------------------------------------------------------------------------------

    2. announcement ( tekton/tekton/bgp.py class Announcement )

    Normal Parameters ( normal BGP UPDATE message attribute ): 
        * prefix: the network prefix that's being announced
        * origin: bgp attribute orgin, ibgp or ebgp or incomplete
        * as_path: the list of AS numbers
        * as_path_len: the lenghth of AS path
        * next_hop: 
             + If the BGP Peers are in different AS then the next_hop IP address
               that will be sent in the update message will be the IP address of
               the advertising router.
             + If the BGP peers are in the same AS (IBGP Peers),
               and the destination network being advertised in the update message
               is also in the same AS, then the next_hop IP address that will be sent
               in the update message will be the IP address of the advertising router
             + If the BGP peers are in the same AS (IBGP Peers),
               and the destination network being advertised in the update message
               is in an external AS, then the next_hop IP address that will be
               sent in the update message will be the IP address of the external
               peer router which sent the advertisement to this AS.
             + please refer [RFC4271] 5.1.3. NEXT_HOP and 9. UPDATE Message Handling
        * local_pref: 
             + Local_pref is only used in updates sent to the IBGP Peers.
             + It is not passed on to the BGP peers in other autonomous systems.
             + please refer [RFC4271] 5.1.5. LOCAL_PREF and 9.1. Decision Process
        * med: multi_exit_disc, med value, it is intended to be used on external links
        * communities: the dict community values: community xxx:xxx -> True or False

    NetComplete Additional Defined Parameters ( for autonomously generate configuration ):
        * peer: the peer from whom that path prefix has been received
        * permitted: the announcement ( UPDATE message ) permit or deny at router X
        * prev_announcement: keep track of the announcement that generated this one
    ------------------------------------------------------------------------------------

    3. propagation info ( synet-plus/synet/utils/bgp_utils.py class PropagatedInfo )

    Normal Parameters ( BGP information carried in propagation graph ):
        * external_peer: 
             + previous comment: the router from different AS
             + actual semantics: the destination network prefix
        * egress: 
             + previous comment: the first local router learns the prefix
             + actual semantics: the router that precedes this router in the path
        * ann_name: the name of announcement variable
        * peer: the eBGP (or first iBGP) peer propagated the route
        * as_path: the AS path learned till this router, the list of AS numbers
        * as_path_len: the length of AS path
        * path: the router path (used in IGP)
    ------------------------------------------------------------------------------------

    4. route map line

    Normal Parameters: 
        * lineno: route map line number
        * access: permit or deny ( i.e. announcement permitted attribute )
        * matches: the iterable data struct of Match
        * actions: the iterable data struct of Action

    ------------------------------------------------------------------------------------

    5. route map
        * name: route map line
        * lines: the iterable data struct of route map line

    ------------------------------------------------------------------------------------

    6. intermediate data ( paths, block, order attribute )

    ------------------------------------------------------------------------------------

    7. intermediate data ( paths_info, block_info, order_info attribute )

    ------------------------------------------------------------------------------------

    8. intermediate data ( origins attribute )

    ------------------------------------------------------------------------------------


NetComplete Input
-----------------

    1. input network topology ( based directed graph, node, edge, attrs, ... )

    NetComplete uses a directed graph to store the network topology with some attributes 
    about BGP and OSPF, such as interface, ip address, enable BGP, enable OSPF, BGP peer 
    route map (involve export and import route map), OSPF link cost etc.

    We initially inputted node ( R1, R2, R3, Provider1, Provider2, Customer ) and edge (
    <Provider1, R1>, <Provider2, R2>,  <R1, Provider1>,  <R1, R2>,  <R1, R3>, etc. ). We 
    then added basic interface, BGP attribute, OSPF attribute and network information to 
    router node, Provider1 and Provider2 has network prefix `128.0.0.0/24`, Customer has 
    network prefix `128.0.1.0/24`.

       +-----------+        +-----------+
       | Provider1 |        | Provider2 |     Provider1, Provider2
       +-----------+        +-----------+     network1: 128.0.0.0/24
             | AS 400             | AS 500
    +--------|--------------------|--------+
    |  +-----------+        +-----------+  |  Global Path Requirements:
    |  |    R1     |--------|    R2     |  |  Rule1: ( path1 == path2 ) >> 
    |  +-----------+        +-----------+  |         ( path3 == path4 )
    |        |                    |        |
    |        |    +-----------+   |        |    path1: [Provider1, R1, R3, Customer]
    |        +----|    R3     |---+        |    path2: [Provider1, R1, R2, R3, Customer]
    |             +-----------+     AS 100 |    path3: [Provider2, R2, R3, Customer]
    +-------------------|------------------+    path4: [Provider2, R2, R1, R3, Customer]
                        |
                  +-----------+
                  | Customer  |               Customer
                  +-----------+ AS 600        network2: 128.0.1.0/24

    ------------------------------------------------------------------------------------

    2. input global path requirements ( based class PathReq, KConnectedPathsReq, ... )

    The source code that defines global path requirements as follows. In a nutshell, the
    following code mainly implements order path requirement:

        * ( path1 == path2 ) >> ( path3 == path4 )

             + path1: [Customer, R3, R1, Provider1]
             + path2: [Customer, R3, R2, R1, Provider1]
             + path3: [Customer, R3, R2, Provider2]
             + path4: [Customer, R3, R1, R2, Provider2]

    These global path requirements will be calculated local path requirements and  block 
    path requirments via netcomplete.

    ```python2``````````````````````````````````````````````````````````````````````````
    path1 = PathReq(Protocols.BGP, prefix1, [customer, r3, r1, provider1], False)
    path2 = PathReq(Protocols.BGP, prefix1, [customer, r3, r2, r1, provider1], False)
    # path3 = PathReq(Protocols.BGP, prefix1, [r2, r3, r1, provider1], False)

    path4 = PathReq(Protocols.BGP, prefix1, [customer, r3, r2, provider2], False)
    path5 = PathReq(Protocols.BGP, prefix1, [customer, r3, r1, r2, provider2], False)
    # path6 = PathReq(Protocols.BGP, prefix1, [r1, r3, r2, provider2], False)

    reqs = [
        PathOrderReq(
            Protocols.BGP,
            prefix1,
            [
                # KConnectedPathsReq(Protocols.BGP, prefix1, [path1,path2,path3], False),
                # KConnectedPathsReq(Protocols.BGP, prefix1, [path4,path5,path6], False),
                KConnectedPathsReq(Protocols.BGP, prefix1, [path1, path2], False),
                KConnectedPathsReq(Protocols.BGP, prefix1, [path4, path5], False),
            ],
            False
        ),
    ]
    ```python2``````````````````````````````````````````````````````````````````````````

    ------------------------------------------------------------------------------------

    3. input configuration sketch with holes ( with route map, involve VALUE?NOTSET )

    We can use classes RouteMap and RouteMapLine to define BGP peer route map framework. 
    We can define route map framework on both sides of all BGP peer. Such as `R1 <-> R2` 
    R1_export_to_R2, R1_import_from_R2, R2_export_to_R1 and  R2_import_from_R1 route map
    can be defined or fewer route map framework could be defined if we fell unnecessary.

    Certainly, we can decide whether the route map framework is deterministic (non-hole)
    or non-deterministic (with holes, VALUE?NOTSET).

    ------------------------------------------------------------------------------------

    4. input announcements ( UPDATE message )


    ------------------------------------------------------------------------------------


NetComplete Connected Synthesis
-------------------------------

    NetComplete firstly synthesize directly connected interfaces,  involve interface, ip
    address. Fastethernet interface default synthesis network is `10.0.0.0/31`, loopback 
    interface default synthesis network is `192.168.0.0/24`. 

    BGP peers are established using the interface fastethernet. 
    OSPF peers are established using the interface loopback. 

    The connected synthesized network topology is shown below. 

       +-------------+        +-------------+
       | Provider1   |        | Provider2   |     Provider1, Provider2
       | 10.0.0.2    |        | 10.0.0.4    |     network1: 128.0.0.0/24
       +-------------+        +-------------+
              | AS 400               | AS 500
    +---------|----------------------|---------+
    |  +-------------+        +-------------+  |  Global Path Requirements:
    |  | R1 10.0.0.3 |--------| R2 10.0.0.5 |  |  Rule1: ( path1 == path2 ) >> 
    |  | 192.168.1.1 |        | 192.168.0.1 |  |         ( path3 == path4 )
    |  +-------------+        +-------------+  |
    |         |                      |         |  path1: [Provider1, R1, R3, Customer]
    |         |    +-------------+   |         |  path2: [Provider1, R1, R2, R3, Customer]
    |         +----| R3 10.0.0.1 |---+         |  path3: [Provider2, R2, R3, Customer]
    |              | 192.168.2.1 |             |  path4: [Provider2, R2, R1, R3, Customer]
    |              +-------------+      AS 100 |
    +---------------------|--------------------+  FastEthernet network: 10.0.0.0/31
                          |                       Loopback network:  192.168.0.0/24
                   +-------------+
                   | Cutomer     |                Customer
                   | 10.0.0.0    |                network2: 128.0.1.0/24
                   +-------------+ AS 600

    Provider1 (Fa0/0 10.0.0.2/31) <--> R1 (Fa0/0 10.0.0.3/31)  Fa: interface fastethernet
    Provider1 (lo100 128.0.0.1/32)                             lo: interface loopback

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


NetComplete Compute Propagation Paths
-------------------------------------

    NetComplete calculates the propagation paths ( i.e. local path requirements for each
    node ) from global path requirements.  NetComplete calculates  the propagation paths
    by simulating the UPDATE message transmissions based on global path requirements and
    blocks unspecified route path.

    For the sake of later needs, the propagation paths contains three main data fields.

        * paths - the set of route path that the router may receive
        * block - the set of route path that are blocked by the router
        * order - the set of order route path that the router may receive

    The order attribute format which is based on the format of global path requirements.
    Global path requirements `( path1 == path2 ) >> ( path3 == path4 )`,  the format  of 
    corresponding order attribute should be `[[set1], [set2]]`.  The route path  in set1 
    have a higher preference then the route path in set2.

    For all destination network prefixes, the paths, block and order of each router need 
    to be calculated. The destination network prefixes for the route path in global path 
    requirements below is the same, which is network1 `128.0.0.0/24`. 

       +-----------+        +-----------+
       | Provider1 |        | Provider2 |     Provider1, Provider2
       +-----------+        +-----------+     network1: 128.0.0.0/24
             | AS 400             | AS 500
    +--------|--------------------|--------+
    |  +-----------+        +-----------+  |  Global Path Requirements:
    |  |    R1     |--------|    R2     |  |  Rule1: ( path1 == path2 ) >> 
    |  +-----------+        +-----------+  |         ( path3 == path4 )
    |        |                    |        |
    |        |    +-----------+   |        |    path1: [Provider1, R1, R3, Customer]
    |        +----|    R3     |---+        |    path2: [Provider1, R1, R2, R3, Customer]
    |             +-----------+     AS 100 |    path3: [Provider2, R2, R3, Customer]
    +-------------------|------------------+    path4: [Provider2, R2, R1, R3, Customer]
                        |
                  +-----------+
                  | Customer  |               Customer
                  +-----------+ AS 600        network2: 128.0.1.0/24

    The network topology and the global path requirements above are calculated to output
    paths, block, order attributes for each router as shown below.

    Destination Network: network1 128.0.0.0/24
        * Provider1:
             + paths: [(Provider1,)]
             + block: [(Provider2, R2, R1, Provider1)]
             + order: [[(Provider1,)],                    note: ( path1 == path2 )
                       []]                                   >> ( path3 == path4 )
        * Provider2: 
             + paths: [(Provider2,)]
             + block: [(Provider1, R1, R2, Provider2)]
             + order: [[(Provider2,)], 
                       []]
        * R1:
             + paths: [(Provider2, R2, R1), (Provider1, R1)]
             + block: [(Provider2, R2, R3, R1)]
             + order: [[(Provider1, R1)], 
                       [(Provider2, R2, R1)]]
        * R2:
             + paths: [(Provider1, R1, R2), (Provider2, R2)]
             + block: [(Provider1, R1, R3, R2)]
             + order: [[(Provider1, R1, R2)], 
                       [(Provider2, R2)]]
        * R3: 
             + paths: [(Provider1, R1, R2, R3), (Provider2, R2, R1, R3), 
                       (Provider1, R1, R3), (Provider2, R2, R3)]
             + block: []
             + order: [[(Provider1, R1, R2, R3), (Provider1, R1, R3)], 
                       [(Provider2, R2, R1, R3), (Provider2, R2, R3)]]
        * Customer:
             + paths: [(Provider1, R1, R2, R3, Customer), (Provider1, R1, R3, Customer), 
                       (Provider2, R2, R3, Cusomter), (Provider2, R2, R1, R3, Customer)]
             + block: []
             + order: [[(Provider1, R1, R2, R3, Customer), (Provider1, R1, R3, Customer)],
                       [(Provider2, R2, R3, Cusomter), (Provider2, R2, R1, R3, Customer)]]

    Other Destination Network ( if exist )
        omitting ... ...


NetComplete Compute Propagation Infos
-------------------------------------

    Then extend the propagation paths ( route path in paths, block and order attribute ) 
    to the propagation infos based previous defined announcements. The propagation infos 
    data struct is shown above. 

    The extended propagation infos as shown below.

    Destination Network: network1 128.0.0.0/24
        * Provider1: 
             + paths_info: set( prop1 )
                 prop1:
                 - Prefix: 128.0.0.0/24     <- param ann_name
                 - External: None           <- param external_peer
                 - Egress: None             <- param egress
                 - Peer: None               <- param peer
                 - ASPath: (400, 5000)      <- param as_path
                 - ASPathLen: 2             <- param as_path_len
                 - Path: ('Provider1',)     <- param path
             + block_info: set( prop2 )
                 prop2:
                 - Prefix: 128.0.0.0/24
                 - External: R1
                 - Egress: Provider1
                 - Peer: R1
                 - ASPath: (400, 100, 500, 3000, 5000)
                 - ASPathLen: 5
                 - Path: ('Provider2', 'R2', 'R1', 'Provider1')
             + order_info: [set(prop1),                   note: ( path1 == path2 )
                            set()]                           >> ( path3 == path4 )
                 prop1: defined above
        * Provider2:
             omitting ... ...
        * R1: 
             omitting ... ...
        * R2: 
             omitting ... ...
        * R3: 
             omitting ... ...
        * Customer: 
             omitting ... ...

    ------------------------------------------------------------------------------------

    Then NetComplete compute origin propagation infos of each paths_info and block_infos
    , such as

        * propagation infos (Provider2, R2, R1, Provider1).propagated_info
          origin propagation infos -> (Provider2, R2, R1).propagated_info
        * propagation infos (Provider1,).propagated_info
          origin propagation infos -> None

    ------------------------------------------------------------------------------------

    In the end, the propagation infos of all routers is summarized as follows.
    ( after remove empty set and through possible other operation )

    node: Provider1
    network prefix: 128.0.0.0/24
    paths attributes: set([('Provider1',)])
    order attributes: [set([('Provider1',)])]
    block attributes: set([('Provider2', 'R2', 'R1', 'Provider1')])
    paths info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: None, Egress: None, Peer: None, 
        ASPath: (400, 5000), ASPathLen: 2, 
        Path: ('Provider1',)>])
    order info attributes: 
        [set([Prop<Prefix: 128.0.0.0/24, External: None, Egress: None, Peer: None, 
        ASPath: (400, 5000), ASPathLen: 2, 
        Path: ('Provider1',)>])]
    block info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: R1, Egress: Provider1, Peer: R1, 
        ASPath: (400, 100, 500, 3000, 5000), ASPathLen: 5, 
        Path: ('Provider2', 'R2', 'R1', 'Provider1')>])
    origins info attributes: 
        {Prop<Prefix: 128.0.0.0/24, External: R1, Egress: Provider1, Peer: R1, 
        ASPath: (400, 100, 500, 3000, 5000), ASPathLen: 5, 
        Path: ('Provider2', 'R2', 'R1', 'Provider1')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
            ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
            Path: ('Provider2', 'R2', 'R1')>}
    ------------------------------------------------------------------------------------
    node: Provider2
    network prefix: 128.0.0.0/24
    paths attributes: set([('Provider2',)])
    order attributes: [set([('Provider2',)])]
    block attributes: set([('Provider1', 'R1', 'R2', 'Provider2')])
    paths info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: None, Egress: None, Peer: None, 
        ASPath: (500, 3000, 5000), ASPathLen: 3, 
        Path: ('Provider2',)>])
    order info attributes: 
        [set([Prop<Prefix: 128.0.0.0/24, External: None, Egress: None, Peer: None, 
        ASPath: (500, 3000, 5000), ASPathLen: 3, 
        Path: ('Provider2',)>])]
    block info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: R2, Egress: Provider2, Peer: R2, 
        ASPath: (500, 100, 400, 5000), ASPathLen: 4, 
        Path: ('Provider1', 'R1', 'R2', 'Provider2')>])
    origins info attributes: 
        {Prop<Prefix: 128.0.0.0/24, External: R2, Egress: Provider2, Peer: R2, 
        ASPath: (500, 100, 400, 5000), ASPathLen: 4, 
        Path: ('Provider1', 'R1', 'R2', 'Provider2')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
            ASPath: (100, 400, 5000), ASPathLen: 3, 
            Path: ('Provider1', 'R1', 'R2')>}
    ------------------------------------------------------------------------------------
    node: R1
    network prefix: 128.0.0.0/24
    paths attributes: set([('Provider2', 'R2', 'R1'), ('Provider1', 'R1')])
    order attributes: [set([('Provider1', 'R1')]), 
                   >> set([('Provider2', 'R2', 'R1')])]
    block attributes: set([('Provider2', 'R2', 'R3', 'R1')])
    paths info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R1')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: Provider1, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1')>])
    order info attributes: 
        [set([Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: Provider1,        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1')>]), 
     >> set([Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R1')>])]
    block info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R3, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R3', 'R1')>])
    origins info attributes: 
        {Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R3, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R3', 'R1')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
            ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
            Path: ('Provider2', 'R2', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R1')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: Provider2, 
            ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
            Path: ('Provider2', 'R2')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: Provider1, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: None, Egress: None, Peer: None, 
            ASPath: (400, 5000), ASPathLen: 2, 
            Path: ('Provider1',)>}
    ------------------------------------------------------------------------------------
    node: R2
    network prefix: 128.0.0.0/24
    paths attributes: set([('Provider1', 'R1', 'R2'), ('Provider2', 'R2')])
    order attributes: [set([('Provider1', 'R1', 'R2')]), 
                   >> set([('Provider2', 'R2')])]
    block attributes: set([('Provider1', 'R1', 'R3', 'R2')])
    paths info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: Provider2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R2')>])
    order info attributes: 
        [set([Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R2')>]), 
     >> set([Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: Provider2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2')>])]
    block info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R3, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R3', 'R2')>])
    origins info attributes: 
        {Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R3, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R3', 'R2')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
            ASPath: (100, 400, 5000), ASPathLen: 3, 
            Path: ('Provider1', 'R1', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: Provider2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: None, Egress: None, Peer: None, 
            ASPath: (500, 3000, 5000), ASPathLen: 3, 
            Path: ('Provider2',)>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R2')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: Provider1, 
            ASPath: (100, 400, 5000), ASPathLen: 3, 
            Path: ('Provider1', 'R1')>}
    ------------------------------------------------------------------------------------
    node: R3
    network prefix: 128.0.0.0/24
    paths attributes: set([('Provider1', 'R1', 'R2', 'R3'), 
                      ('Provider2', 'R2', 'R1', 'R3'), ('Provider1', 'R1', 'R3'), 
                      ('Provider2', 'R2', 'R3')])
    order attributes: [set([('Provider1', 'R1', 'R2', 'R3'), ('Provider1', 'R1', 'R3')]),
                   >> set([('Provider2', 'R2', 'R1', 'R3'), ('Provider2', 'R2', 'R3')])]
    block attributes: set([])
    paths info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R2, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R2', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R1, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R1', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R3')>])
    order info attributes: 
        [set([Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R2, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R2', 'R3')>]), 
     >> set([Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R1, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R1', 'R3')>])]
    block info attributes: set([])
    origins info attributes: 
        {Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R3')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: Provider1, 
            ASPath: (100, 400, 5000), ASPathLen: 3, 
            Path: ('Provider1', 'R1')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R2, 
        ASPath: (100, 400, 5000), ASPathLen: 3, 
        Path: ('Provider1', 'R1', 'R2', 'R3')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
            ASPath: (100, 400, 5000), ASPathLen: 3, 
            Path: ('Provider1', 'R1', 'R2')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R1, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R1', 'R3')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
            ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
            Path: ('Provider2', 'R2', 'R1')>, 
        Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
        ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
        Path: ('Provider2', 'R2', 'R3')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: Provider2, 
            ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
            Path: ('Provider2', 'R2')>}
    ------------------------------------------------------------------------------------
    node: Customer
    network prefix: 128.0.0.0/24
    paths attributes: set([('Provider1', 'R1', 'R2', 'R3', 'Customer'), 
                      ('Provider1', 'R1', 'R3', 'Customer'), 
                      ('Provider2', 'R2', 'R3', 'Customer'), 
                      ('Provider2', 'R2', 'R1', 'R3', 'Customer')])
    order attributes: [set([('Provider1', 'R1', 'R2', 'R3', 'Customer'), 
                      ('Provider1', 'R1', 'R3', 'Customer')]), 
                   >> set([('Provider2', 'R2', 'R3', 'Customer'), 
                      ('Provider2', 'R2', 'R1', 'R3', 'Customer')])]
    block attributes: set([])
    paths info attributes: 
        set([Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 400, 5000), ASPathLen: 4, 
        Path: ('Provider1', 'R1', 'R3', 'Customer')>, 
        Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 500, 3000, 5000), ASPathLen: 5, 
        Path: ('Provider2', 'R2', 'R1', 'R3', 'Customer')>, 
        Prop<Prefix: 128.0.0.0/24, External: R, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 500, 3000, 5000), ASPathLen: 5, 
        Path: ('Provider2', 'R2', 'R3', 'Customer')>, 
        Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 400, 5000), ASPathLen: 4, 
        Path: ('Provider1', 'R1', 'R2', 'R3', 'Customer')>])
    order info attributes: 
        [set([Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 400, 5000), ASPathLen: 4, 
        Path: ('Provider1', 'R1', 'R3', 'Customer')>, 
        Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 400, 5000), ASPathLen: 4, 
        Path: ('Provider1', 'R1', 'R2', 'R3', 'Customer')>]), 
     >> set([Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 500, 3000, 5000), ASPathLen: 5, 
        Path: ('Provider2', 'R2', 'R1', 'R3', 'ustomer')>, 
        Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 500, 3000, 5000), ASPathLen: 5, 
        Path: ('Provider2', 'R2', 'R3', 'Customer')>])]
    block info attributes: set([])
    origins info attributes: 
        {Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 400, 5000), ASPathLen: 4, 
        Path: ('Provider1', 'R1', 'R3', 'Customer')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R1, 
            ASPath: (100, 400, 5000), ASPathLen: 3, 
            Path: ('Provider1', 'R1', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 500, 3000, 5000), ASPathLen: 5, 
        Path: ('Provider2', 'R2', 'R1', 'R3', 'Customer')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R1, 
            ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
            Path: ('Provider2', 'R2', 'R1', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: R3i, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 500, 3000, 5000), ASPathLen: 5, 
        Path: ('Provider2', 'R2', 'R3', 'Customer')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider2, Egress: R2, Peer: R2, 
            ASPath: (100, 500, 3000, 5000), ASPathLen: 4, 
            Path: ('Provider2', 'R2', 'R3')>, 
        Prop<Prefix: 128.0.0.0/24, External: R3, Egress: Customer, Peer: R3, 
        ASPath: (600, 100, 400, 5000), ASPathLen: 4, 
        Path: ('Provider1', 'R1', 'R2', 'R3', 'Customer')>: 
         -> Prop<Prefix: 128.0.0.0/24, External: Provider1, Egress: R1, Peer: R2, 
            ASPath: (100, 400, 5000), ASPathLen: 3, 
            Path: ('Provider1', 'R1', 'R2', 'R3')>}

    ------------------------------------------------------------------------------------


NetComplete Generate Basic SMT Variables
----------------------------------------

    1. create the SMT context

    SMT context contains all SMT enum sort, SMT variables and SMT constratins.

        * special symbols to SMT name map:
            + '.' : '_DOT_'
            + '/' : '_SLASH_'
            + '-' : '_DASH_'
            + ':' : '_SEMI_'
            + '(' : '_OPENP_'
            + ')' : '_CLOSEP_'

    ------------------------------------------------------------------------------------

    2. generate SMT enum sort

    Specifically, SMT enum sort include network prefix, nexthop and bgp origin attribute

        * network prefix enum sort PrefixSort:
            + APLPHA_128_DOT_0_DOT_1_DOT_0_SLASH_24  ( network2 128.0.1.0/24 )
            + APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24  ( network1 128.0.0.0/24 )
        * nexthop enum sort NextHopSort:
            + R3_DASH_lo100
            + R3_DASH_Fa0_DASH_0
            + Provider2_DASH_Fa0_DASH_0
            + omitting ...
        * bgp origin attribute enum sort BGPOriginSort:
            + IGP
            + EBGP
            + INCOMPLETE

    ------------------------------------------------------------------------------------

    3. generate SMT variables for all propagation infos ( ---> related announcement )

    Take provider1 network prefix 128.0.0.0/24 paths info prop1 as an example  to  show
    this process.

    propagation infos ( involve paths_info + block_info ) ---> related announcement
                                                          ---> related SMT variables

    propagation infos ( involve paths_info + block_info )
    node: Provider1
    network prefix: 128.0.0.0/24
    paths info attributes: 
        * Prefix: 128.0.0.0/24
        * External: None
        * Egress: None
        * Peer: None
        * ASPath: (400, 5000), ASPathLen: 2
        * Path: ('Provider1',)

    related announcement:
        * prefix:
        * peer:
        * origin:
        * as_path:
        * as_path_len:
        * next_hop:
        * local_pref:
        * med
        * communities:
            + community 100:2:
            + community 100:3:
            + community 100:1:
        * permitted: VALUE?NOTSET ( key smt variables, permit or block in this router )

    related SMT variables:
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_prefix_270
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_prefix_270, 
           EnumType(PrefixSort, 2), APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_peer_271
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_peer_271, 
           EnumType(PeerSort, 6), Provider1)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_origin_272
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_origin_272, 
           EnumType(BGPOriginSort, 3), EBGP)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_as_path_273
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_as_path_273, 
                 EnumType(ASPathSort, 8), as_path_400_5000)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_as_path_len_274
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_as_path_len_274,
                 Int, 1)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_next_hop_275
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_next_hop_275, 
                 EnumType(NextHopSort, 12), APLPHA_0_DOT_0_DOT_0_DOT_0)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_local_pref_276
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_local_pref_276, 
                 Int, 100)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_med_277
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_med_277, 
                 Int, 100)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_permitted_278
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_permitted_278, 
                 Bool, ?)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_Comm_Community_
          OPENP_100_2_CLOSEP__279
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_Comm_Community_
                 OPENP_100_2_CLOSEP__279, Bool, True)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_Comm_Community_
          OPENP_100_3_CLOSEP__280
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_Comm_Community_
                 OPENP_100_3_CLOSEP__280, Bool, True)
        * Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_Comm_Community_
          OPENP_100_1_CLOSEP__281
          SMTVar(Sham_Provider1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_Comm_Community_
                 OPENP_100_1_CLOSEP__281, Bool, True)

    ------------------------------------------------------------------------------------


NetComplete Synthesis BGP
-------------------------

    1. export route map for each router ---> SMT variables and SMT constraints

    Here we take route map ( R1 export to Provider1 ) as example.

       +-----------+        +-----------+
       | Provider1 |        | Provider2 |     Provider1, Provider2
       +-----------+        +-----------+     network1: 128.0.0.0/24
             | AS 400             | AS 500
    +--------|--------------------|--------+
    |  +-----------+        +-----------+  |  Global Path Requirements:
    |  |    R1     |--------|    R2     |  |  Rule1: ( path1 == path2 ) >> 
    |  +-----------+        +-----------+  |         ( path3 == path4 )
    |        |                    |        |
    |        |    +-----------+   |        |    path1: [Provider1, R1, R3, Customer]
    |        +----|    R3     |---+        |    path2: [Provider1, R1, R2, R3, Customer]
    |             +-----------+     AS 100 |    path3: [Provider2, R2, R3, Customer]
    +-------------------|------------------+    path4: [Provider2, R2, R1, R3, Customer]
                        |
                  +-----------+
                  | Customer  |               Customer
                  +-----------+ AS 600        network2: 128.0.1.0/24

    Provider1 has only one announcement prop1 ( Provider2, R2, R1, Provoder1 )  from R1.
    So, with R1_exported_to_Provider1 route map framework defined, only one announcement 
    prop1 will match R1_exported_to_Provider1 to execute some set actions.

    prop1 ( Provider2, R2, R1, Provider1 ) ---> origin prop2 ( Provider2, R2, R1 )
                                           ---> related announcements
                                           ---> related SMT variables ( Announcement )

    Now, call function SMTMatch
        * param route_map: R1_exported_to_Provider1 route map framework
            'R1_export_to_Provider1': RouteMap R1_export_to_Provider1
            + route map line 10
	            - lineno:  10
	            - access:  EMPTY?Value, 
	            - Matches: [MatchCommunitiesList(CommunityList(id=1, 
                            access=Access.permit, 
                            communities=['EMPTY?Value']))], 
	            - Actions: []>
            + route map line 20
	            - lineno:  20
	            - access:  Access.permit, 
	            - Matches: [], 
	            - Actions: []>
            + route map line 100
                - lineno:  100
	            - access:  Access.deny, 
	            - Matches: [], 
	            - Actions: []>
        * param announcements: the set of related SMT variables ( named ann1 )

    For ann1 generate SMT variables and SMT constraints to select one route map line.
        * ann1 
            + SMT variable: SelectOneRmapLineIndex_84 ( index_var )
            + SMT constraint: RmapIndexBound_R1_exported_to_Provider1_0
                + z3.Or( index_var == 10, index_var == 20, index_var == 100, z3 context )
        * other announcement, if exist
            + SMT variable: 
            + SMT constraint: 

    For each route map line generate SMT variables and SMT constraints sequentially.
 +----- * route map line 10
 |        + route map line 10 matches ---> SMT variables and SMT constraints
 |        + is match line 10 ( announcement is match this route map line )
 |                                    ---> SMT variables and SMT constraints
 |            - ann1_is_match_line_10
 |            - other_ann_is_math_line_10, if exist
 |        + set announcement permitted attributes ( permit or block in this router )
 |                                    ---> SMT variables and SMT constraints
 |            - ann1_permitted
 |            - other_ann_permitted, if exist
 |        + route map line 10 actions ---> SMT variables and SMT constraints
 |          for announcement, is match True  -> execute some actions
 |                            is match False -> non-execute some actions
 |     * route map line 20
 |        + route map line 20 matches
 |        + is_match_line_20, is match route map line 20
 |        + set permitted attributes ( permit or block in this router )
 |        + route map line 20 actions
 |     * route map line 100
 |        + route map line 100 matches
 |        + is_match route map line 100
 |        + set permitted attributes ( permit or block in this router )
 |        + route map line 100 actions
 |
 | For each route map line generate SMT constratins to determine ann1 select one  route
 | map line at the top.
 |     * route map line 10  - ann1
 |           + SMT constraint: rmap_R1_exported_to_Provider1_order_9
 |     * route map line 10  - other announcement, if exist
 |     * route map line 20  - ann1
 |           + SMT constraint: rmap_R1_exported_to_Provider1_order_12
 |     * route map line 100 - ann1
 |           + SMT constraint: rmap_R1_exported_to_Provider1_order_15
 |
 +> Route map line 10 matches: 
	Matches: [MatchCommunitiesList(CommunityList(id=1, 
              access=Access.permit, 
              communities=['EMPTY?Value']))], 

    communities contains communitylist 100:1, 100:2, 100:3, so SMT match communities
        * communitylist 100:1  ---> SMTVar(Var_85, Bool, True)
        * communitylist 100:2  ---> SMTVar(Var_86, Bool, True)
        * communitylist 100:3  ---> SMTVar(Var_87, Bool, True)
        * selectone from above communitylist  ---> SMTVar(SelectOne_index_88, Int, ?)
        * set SMT constraint ---> SelectOne_index_range_1
                                  select Var_85 or Var_86 or Var_87 or None

    Route map line 10 is match framework: 
        * SMTSelectorMatch
            + SMTMatch
                - SMTMatchCommunityList
                    . SMTMatchAnd
                        . SMTMatchSelectorOne  ---> SMTVar(Var_90, Bool, ?)
                            . SMTMatchCommunity 100:2  ---> SMTVar(Var_91, Bool, ?) --+
                            . SMTMatchCommunity 100:3  ---> SMTVar(Var_92, Bool, ?) --+
                            . SMTMatchCommunity 100:1  ---> SMTVar(Var_93, Bool, ?) --+
                        . ---> SMT constraint SelectOne_match_5 -----------+  <-------+
                               select Var_91 or Var_92 or Var_93 or None   |
                    . ---> SMTVar(match_and_94, Bool, ?) <-----------------+
                      ---> SMT constraint const_and_6                      |
                - temp  <--------------------------------------------------+
            + temp  <------------------------------------------------------+
        * ---> SMTVar(match_sel_95, Bool, ?)  <----------------------------+
          ---> SMT constraint Selector_7

    Set announcement permitted attribute:
        ############################################################
        # is_match ( Route Map Line )                              #
        #                                                          #
        # Route Map Line True  and Announcement permit             #
        #     -> origin Announcement.permitted (permit or deny)    #
        #                                                          #
        # Route Map Line False and Announcement permit -> permit   #
        # Route Map Line False and Announcement deny   -> deny     #
        #                                                          #
        # Route Map Line True  and Announcement deny   -> deny     #
        #                                                          #
        # [Provider2, R2, R1] deny -----------------+              #
        # [Provider2, r2, r1, Provider1] deny  <----+              #
        ############################################################

    Route map actions: 
	Actions: []>
        * TODO

    ------------------------------------------------------------------------------------

    2. set announcements ( from paths_info ) to permit ---> SMT constraints
    
    Control all prop in paths_info -> set SMT constraint permit
    This SMT constraint is related to announcement permitted attribute above.

    ------------------------------------------------------------------------------------

    3. set announcements ( from block_info ) to block ---> SMT constraints

    Control all prop in block_info -> set SMT constraint permit
    This SMT constraint is related to announcement permitted attribute above.

    ------------------------------------------------------------------------------------

    4. import route map for each router ---> SMT variables and SMT constraints

    This is the same as what `export route map for each router` does.

    ------------------------------------------------------------------------------------

    5. path preference for each router ---> SMT variables and SMT constraints

    For order_info, set some SMT constraints to guarantee path preference.

    ------------------------------------------------------------------------------------

    6. evaluate all SMT variables ( VALUE?NOTSET ) sequentially

    ------------------------------------------------------------------------------------

    7. generate synthesized router configuration of BGP 

    ------------------------------------------------------------------------------------
