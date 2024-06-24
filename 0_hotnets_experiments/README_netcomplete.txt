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


NetComplete Input
-----------------

    1. input network topology ( based directed graph, node, edge, attrs, ... )

    NetComplete uses a directed graph to store the network topology with some attributes 
    about BGP and OSPF, such as interface, ip address, enable BGP, enable OSPF, BGP peer 
    route map ( involve export and import route map ), OSPF edge weight etc.

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

    2. input global path requirements ( based class PathReq, KConnectedPathsReq, ... )

    The source code that defines global path requirements as follows. In a nutshell, the
    following code mainly implements order path requirement:
        ( path1 == path2 ) >> ( path3 == path4 )
        path1: [Customer, R3, R1, Provider1]
        path2: [Customer, R3, R2, R1, Provider1]
        path3: [Customer, R3, R2, Provider2]
        path4: [Customer, R3, R1, R2, Provider2]

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

    3. input configuration sketch with holes ( with route map, involve VALUE?NOTSET )

    We can use classes RouteMap and RouteMapLine to define BGP peer route map framework.
    We can define route map framework on both sides of all BGP peer. Such as `R1 <-> R2`
    we can define R1_export_to_R2, R1_import_from_R2, R2_export_to_R1 and R2_import_from
    _R2 route map framework, or we could define fewer route map framework,  if  we  fell 
    unnecessary.

    Certainly, we can decide whether the route map framework is deterministic (non-hole)
    or non-deterministic (with holes)


NetComplete Intermediate data
-----------------------------


NetComplete Output
------------------
