basic network topology
----------------------

       +-------------+        +-------------+
       | Provider1   |        | Provider2   |     Provider1, Provider2
       | 10.0.0.2    |        | 10.0.0.4    |     network1: 128.0.0.0/24
       +-------------+        +-------------+
              | AS 400               | AS 500
              |                      |
    +------I1-|-E1----------------I2-|-E2------+
    |  +-------------+        +-------------+  |  Global Requirements
    |  | R1 10.0.0.3 |--------| R2 10.0.0.5 |  |  Rule 1: path1 == path2
    |  | 192.168.1.1 |        | 192.168.0.1 |  |          >> path3 == path4
    |  +-------------+        +-------------+  |
    |         |                      |         |  path1: [P1, R1, R3, C]
    |         | I3 +-------------+ I4|         |  path2: [P1, R1, R2, R3, C]
    |         +----| R3 10.0.0.1 |---+         |  path3: [P2, R2, R3, C]
    |           E3 | 192.168.2.1 | E4          |  path4: [P2, R2, R1, R3, C]
    |              +-------------+      AS 100 |
    +---------------------|--------------------+
                          |
                   +-------------+
                   | Cutomer     |                Customer
                   | 10.0.0.0    |                network2: 128.0.1.0/24
                   +-------------+ AS 600

    I1, ..., I4, E1, ..., E4: Route Map (BGP peer inbound or outbound policy)

    I1: R1_import_from_Provider1         I2: R2_import_from_Provider2
    E1: R1_export_to_Provider1           E2: R2_export_to_Provider2

    I3: R3_import_from_R1                I4: R3_import_from_R2
    E3: R3_export_to_R1                  E4: R3_export_to_R2

    other interface and related ip address

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


global requirements
-------------------

       +-------------+        +-------------+
       | Provider1   |        | Provider2   |     Provider1, Provider2
       | 10.0.0.2    |        | 10.0.0.4    |     network1: 128.0.0.0/24
       +-------------+        +-------------+
              | AS 400               | AS 500
              |                      |
    +------I1-|-E1----------------I2-|-E2------+
    |  +-------------+        +-------------+  |  Global Requirements
    |  | R1 10.0.0.3 |--------| R2 10.0.0.5 |  |  Rule 1: path1 == path2 >> 
    |  | 192.168.1.1 |        | 192.168.0.1 |  |          path3 == path4
    |  +-------------+        +-------------+  |
    |         |                      |         |  path1: [P1, R1, R3, C]
    |         | I3 +-------------+ I4|         |  path2: [P1, R1, R2, R3, C]
    |         +----| R3 10.0.0.1 |---+         |  path3: [P2, R2, R3, C]
    |           E3 | 192.168.2.1 | E4          |  path4: [P2, R2, R1, R3, C]
    |              +-------------+      AS 100 |
    +---------------------|--------------------+
                          |
                   +-------------+
                   | Cutomer     |                Customer
                   | 10.0.0.0    |                network2: 128.0.1.0/24
                   +-------------+ AS 600


    order path requirements                       block path requirements (netcomplete)

    ( path1 == path2 ) >> ( path3 == path4 )      ! [Provider2, R2, R3, R1]   ****
                                                  ! [Provider1, R1, R3, R2]   ****
    path1: [Provider1, R1, R3, Customer]          ! [Provider2, R2, R1, Provider1]
    path2: [Provider1, R1, R2, R3, Customer]      ! [Provider1, R1, R2, Provider2]
    path3: [Provider2, R2, R3, Customer]
    path4: [Provider2, R2, R1, R3, Customer]

    netcomplete intermediate calculation
    ===================================>

    Customer:
      network prefix: 128.0.0.0/24 ( Provider1 & Provider2 )
      paths attrs: [Provider1, R1, R2, R3, Customer], [Provider1, R1, R3, Customer], 
                   [Provider2, R2, R3, Customer], [Provider2, R2, R1, R3, Customer]
      order attrs: set([Provider1, R1, R2, R3, Customer], [Provider1, R1, R3, Customer])
                   >> set([Provider2, R2, R3, Customer], [Provider2, R2, R1, R3, Customer])
      block attrs: []   # NONE

    R1:
      network prefix: 128.0.0.0/24 ( Provider1 & Provider2 )
      paths attrs: [Provider2, R2, R1], [Provider1, R1]
      order attrs: set([Provider1, R1]) >> set([Provider2, R2, R1])
      block attrs: [Provider2, R2, R3, R1]

    R2: 
      network prefix: 128.0.0.0/24 ( Provider1 & Provider2 )
      paths attrs: [Provider1, R1, R2], [Provider2, R2]
      order attrs: set([Provider1, R1, R2]) >> set([Provider2, R2])
      block attrs: [Provider1, R1, R3, R2]

    R3:
      network prefix: 128.0.0.0/24 ( Provider1 & Provider2 )
      paths attrs: [Provider1, R1, R2, R3], [Provider2, R2, R1, R3], 
                   [Provider1, R1, R3], [Provider2, R2, R3]
      order attrs: set([Provider1, R1, R2, R3], [Provider1, R1, R3])
                   >> set([Provider2, R2, R1, R3], [Provider2, R2, R3])
      block attrs: []   # NONE

    Provider1:
      network prefix: 128.0.0.0/24 ( Provider1 & Provider2 )
      paths attrs: [Provider1]
      order attrs: set([Provider1])
      block attrs: [Provider2, R2, R1, Provider1]

    Provider2:
      network prefix: 128.0.0.0/24 ( Provider1 & Provider2 )
      paths attrs: [Provider2]
      order attrs: set([Provider2])
      block attrs: [Provider1, R1, R2, Provider2]


configuration sketch
--------------------

       +-------------+        +-------------+
       | Provider1   |        | Provider2   |     Provider1, Provider2
       | 10.0.0.2    |        | 10.0.0.4    |     network1: 128.0.0.0/24
       +-------------+        +-------------+
              | AS 400               | AS 500
    tag 100:1 |            tag 100:2 |
    +------I1-|-E1----------------I2-|-E2------+
    |  +-------------+        +-------------+  |  Global Requirements
    |  | R1 10.0.0.3 |--------| R2 10.0.0.5 |  |  Rule 1: path1 == path2 >> 
    |  | 192.168.1.1 |        | 192.168.0.1 |  |          path3 == path4
    |  +-------------+        +-------------+  |
    |         |                      |         |  path1: [P1, R1, R3, C]
    |         | I3 +-------------+ I4|         |  path2: [P1, R1, R2, R3, C]
    |         +----| R3 10.0.0.1 |---+         |  path3: [P2, R2, R3, C]
    |           E3 | 192.168.2.1 | E4          |  path4: [P2, R2, R1, R3, C]
    |              +-------------+      AS 100 |
    +---------------------|--------------------+
    100:1 => 200          |         100:1 => 200  note: local preference higher
    100:2 => 100   +-------------+  100:2 => 100        the more preferred it is
                   | Cutomer     |                Customer
                   | 10.0.0.0    |                network2: 128.0.1.0/24
                   +-------------+ AS 600

    I1: R1_import_from_Provider1         I2: R2_import_from_Provider2
        match prefix 128.0.0.0/24            match prefix 128.0.0.0/24
        set community tag 100:1              set community tag 100:2
        then drop all UPDATE message         then drop all UPDATE message

 +--E1: R1_export_to_Provider1           E2: R2_export_to_Provider2
 |      match community tag 100:2            match community tag 100:1
 |      drop this UPDATE message             drop this UPDATE message
 |      then permit all UPDATE message       then permit all UPDATE message
 |      then drop all UPDATE message         then drop all UPDATE message
 |
 |
 |  I3: R3_import_from_R1                I4: R3_import_from_R2
 |      match community tag 100:1            match community tag 100:1
 |      set local preference 200             set local preference 200
 |      match community tag 100:2            match community tag 100:2
 |      set local preference 100             set local preference 100
 |      then drop all UPDATE message         then drop all UPDATE message
 |
 |  E3: R3_export_to_R1                  E4: R3_export_to_R2
 |      match community tag 100:2            match community tag 100:1
 |      drop this UPDATE message             drop this UPDATE message
 |      then permit all UPDATE message       then permit all UPDATE message
 |      then drop all UPDATE message         then drop all UPDATE message
 |
 +---------> scenario1 full configs (non-holes)      
             E1: R1_export_to_Provider1        
                 match community tag 100:2     
                 drop this UPDATE message      
                 then permit all UPDATE message
                 then drop all UPDATE message  

             scenario2 hole configs (next-hops)    scenario3 hole configs (community)
             E1: R1_export_to_Provider1            E1: R1_export_to_Provider1
                 match ?                               match community tag ?
                 set ?                                 drop this UPDATE message
                 then drop all UPDATE message          then permit all UPDATE messag
                                                       then drop all UPDATE message

full configs (non-holes)
------------------------

    full-configs-simple
    ├── configs                      # synthesized configuration
    │   ├── Customer.cfg
    │   ├── Provider1.cfg
    │   ├── Provider2.cfg
    │   ├── R1.cfg                   # R1 synthesized configuration
    │   ├── R2.cfg                   # R1 full configuration before synthesize
    │   └── R3.cfg
    ├── smt.smt2                     # SMT output (SMT solver & check)
    └── topo.ini                     # network topology


hole configs (next-hops)
------------------------

    holes-configs-simple-nexthop
    ├── configs                      # synthesized configuration
    │   ├── Customer.cfg
    │   ├── Provider1.cfg
    │   ├── Provider2.cfg
    │   ├── R1.cfg                   # R1 synthesized configuration <--+
    │   ├── R2.cfg                                                     |
    │   └── R3.cfg                                                     |
    ├── R1_configuration_sketch.cfg  # R1 configuration sketch --------+
    │                                # with VALUE?NOTSET
    │
    ├── smt.smt2                     # SMT output (SMT solver & check)
    └── topo.ini                     # network topology

    ==================== R1 route maps ===============
    {'R1_import_from_Provider1': RouteMap R1_import_from_Provider1
    	lineno: 10
    	access: Access.permit, 
    	Matches: 
    		[MatchIpPrefixListList(IpPrefixList(id=Provider1_to_Customer, access=Access.permit, networks=[IPv4Network(u'128.0.0.0/24')]))], 
    	Actions: 
    		[SetCommunity([Community(100:1)])]>
    	lineno: 100
    	access: Access.deny, 
    	Matches: 
    		[], 
    	Actions: 
    		[]>
    , 'R1_export_to_Provider1': RouteMap R1_export_to_Provider1
    	lineno: 1
    	access: EMPTY?Value, 
    	Matches: 
    		[MatchSelectOne([MatchNextHop(EMPTY?Value), MatchIpPrefixListList(IpPrefixList(id=ip_list_R1_1, access=Access.permit, networks=['EMPTY?Value'])), MatchCommunitiesList(CommunityList(id=2, access=Access.permit, communities=['EMPTY?Value'])), MatchAsPath(EMPTY?Value)])], 
    	Actions: 
    		[SetActions([SetNextHop(EMPTY?Value), SetCommunity(['EMPTY?Value']), SetCommunity(['EMPTY?Value']), SetLocalPref(EMPTY?Value)])]>
    	lineno: 100
    	access: Access.deny, 
    	Matches: 
    		[], 
    	Actions: 
    		[]>
    }

    ==================== R1 route maps call trace ====
        SMTRouteMap
          |
    +---SMTRouteMapLine
    |     |
    |   SMTMatch & SMTMatchAnd
    |
    +-> SMTSelectorMatch
    |
    +-> SMTActions

    ==================== R1 route maps smt ===========
    --------- route map & route map line smt ---------
    Route Map: R1_export_to_Provider1
        Announcement: [Provider2, R2, R1] announcement smt
                      ===> SMTVar(SelectOneRmapLineIndex_84, Int, ?) ----------+
                      ===> SMTConst RmapIndexBound_R1_export_to_Provider1_0 <--+

    Route Map Line: lineno:  1
    	            access:  EMPTY?Value, 
    	            Matches: [MatchSelectOne([
                                MatchNextHop(EMPTY?Value), 
    Route Map                   MatchIpPrefixListList(IpPrefixList(id=ip_list_R1_1, 
    R1_export_to_Provider1        access=Access.permit, networks=['EMPTY?Value'])), 
    Line 1                      MatchCommunitiesList(CommunityList(id=2, 
                                  access=Access.permit, communities=['EMPTY?Value'])), 
                                MatchAsPath(EMPTY?Value)])], 
    	            Actions: [SetActions([
                                SetNextHop(EMPTY?Value), 
                                SetCommunity(['EMPTY?Value']), 
                                SetCommunity(['EMPTY?Value']), 
                                SetLocalPref(EMPTY?Value)])]>
                    ------------------------------------------------------------------
    	            lineno:  100
    Route Map       access:  Access.deny, 
    R1_export_to_P1 Matches: [], 
    Line 1          Actions: []>

    
    for 

    --------- route map match MatchSelectOne ---------
    Route Map Line - Match: MatchSelectOne [BEGIN]

        Route Map Match:
        * MatchSelectOne - MatchNextHop(EMPTY?Value)
              ===> SMTVar(Var_85, EnumType(NextHopSort, 12), ?)
        * MatchSelectOne - MatchIpPrefixListList(IpPrefixList(id=ip_list_R1_1, access=Access.permit, networks=['EMPTY?Value']))
              ===> SMTVar(Var_86, EnumType(PrefixSort, 2), APLPHA_128_DOT_0_DOT_1_DOT_0_SLASH_24)
              ===> SMTVar(Var_87, EnumType(PrefixSort, 2), APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)
              ===>  SMTVar(SelectOne_index_88, Int, ?)
        * MatchSelectOne - MatchCommunitiesList(CommunityList(id=2, access=Access.permit, communities=['EMPTY?Value']))

              ===> SMTVar(Var_89, Bool, True)      # community 100:2 ??
              ===> SMTVar(Var_90, Bool, True)      # community 100:3 ??
              ===> SMTVar(Var_91, Bool, True)      # community 100:1 ??
              ===>  SMTVar(SelectOne_index_92, Int, ?)
        * MatchSelectOne - MatchAsPath(EMPTY?Value)
              ===> SMTVar(Var_93, EnumType(ASPathSort, 8), ?)

    Route Map Line: MatchSelectOne [END]
        ===> SMTVar(SelectOne_index_94, Int, ?)

    Route Map Selector: NONE

    --------------- route map Access -----------------
    Route Map Access: True(Permit), False(Deny) ( or True(Deny), False(Permit) )
        ===> SMT(Var_95, Bool, ?)

    --------- route map Action SetActions ------------
    Route Map Line - Action: SetActions [BEGIN]

        Route Map Action:
        * SetActions - SetActions([SetNextHop(EMPTY?Value)
              ===> SMTVar(Var_110, EnumType(NextHopSort, 12), ?)
              ===>  SMTVar(match_sel_123, Bool, ?)
        * SetActions - SetCommunity(['EMPTY?Value'])
              ===> SMTVar(Var_125, Bool, True)     # community 100:1 ??
              ===> SMTVar(Var_127, Bool, True)     # community 100:2 ??
              ===> SMTVar(Var_129, Bool, True)     # community 100:3 ??
              ===>  SMTVar(SetOneIndex_131, Int, ?)
        * SetActions - SetCommunity(['EMPTY?Value'])    # community dup ??
              ===> SMTVar(Var_135, Bool, True)
              ===> SMTVar(Var_137, Bool, True)
              ===> SMTVar(Var_139, Bool, True)
              ===>  SMTVar(SetOneIndex_141, Int, ?)
        * SetActions - SetLocalPref(EMPTY?Value)])
              ===> SMTVar(Var_145, Int, ?)

    Route Map Line - Action: SetActions [END]
        ===>  SMTVar(SetOneIndex_147, Int, ?)
    
    ==================== R1 route maps simple ========
    !
    ip prefix-list Provider1_to_Customer seq 10 permit 128.0.0.0/24
    !
    ip prefix-list ip_list_R1_1 seq 10 permit 128.0.1.0/24
    !
    !
    route-map R1_export_to_Provider1 ? 1   ===>   route-map R1_export_to_Provider1 deny 1
     match ?                               ===>    match ip address prefix-list ip_list_R1_1
     set ?                                 ===>    set next-hop 10.0.0.1
    route-map R1_export_to_Provider1 deny 100
    !
    route-map R1_import_from_Provider1 permit 10
     match ip address prefix-list Provider1_to_Customer
     set community 100:1 additive
    route-map R1_import_from_Provider1 deny 100
    !
    !
    router bgp 100
     no synchronization
     bgp log-neighbor-changes
     neighbor 10.0.0.2 remote-as 400
     neighbor 10.0.0.2 description "To Provider1"
     neighbor 10.0.0.2 advertisement-interval 0
     neighbor 10.0.0.2 soft-reconfiguration inbound
     neighbor 10.0.0.2 send-community
     neighbor 10.0.0.2 route-map R1_import_from_Provider1 in
     neighbor 10.0.0.2 route-map R1_export_to_Provider1 out


hole configs (community)
------------------------

    holes-configs-simple-community
    ├── configs                      # synthesized configuration
    │   ├── Customer.cfg
    │   ├── Provider1.cfg
    │   ├── Provider2.cfg
    │   ├── R1.cfg                   # R1 synthesized configuration <--+
    │   ├── R2.cfg                                                     |
    │   └── R3.cfg                                                     |
    ├── R1_configuration_sketch.cfg  # R1 configuration sketch --------+
    │                                # with community match VALUE?NOTSET
    │
    ├── smt.smt2                     # SMT output (SMT solver & check)
    └── topo.ini                     # network topology
    
    ==================== R1 route maps ===============
    {'R1_import_from_Provider1': RouteMap R1_import_from_Provider1
    	lineno: 10
    	access: Access.permit, 
    	Matches: 
    		[MatchIpPrefixListList(IpPrefixList(id=Provider1_to_Customer, access=Access.permit, networks=[IPv4Network(u'128.0.0.0/24')]))], 
    	Actions: 
    		[SetCommunity([Community(100:1)])]>
    	lineno: 100
    	access: Access.deny, 
    	Matches: 
    		[], 
    	Actions: 
    		[]>
    , 'R1_export_to_Provider1': RouteMap R1_export_to_Provider1
    	lineno: 10
    	access: EMPTY?Value, 
    	Matches: 
    		[MatchCommunitiesList(CommunityList(id=1, access=Access.permit, communities=['EMPTY?Value']))], 
    	Actions: 
    		[]>
    	lineno: 20
    	access: Access.permit, 
    	Matches: 
    		[], 
    	Actions: 
    		[]>
    	lineno: 100
    	access: Access.deny, 
    	Matches: 
    		[], 
    	Actions: 
    		[]>
    }
    
    ==================== R1 route maps simple ========
    !                              ===>
    ip community-list 1 permit ?   ===>   ip community-list 1 permit 100:2
    !                              ===>
    ip prefix-list Provider1_to_Customer seq 10 permit 128.0.0.0/24
    !
    !
    route-map R1_export_to_Provider1 deny 10
     match community 1
    route-map R1_export_to_Provider1 permit 20
    route-map R1_export_to_Provider1 deny 100
    !
    route-map R1_import_from_Provider1 permit 10
     match ip address prefix-list Provider1_to_Customer
     set community 100:1 additive
    route-map R1_import_from_Provider1 deny 100
    !
    !
    router bgp 100
     no synchronization
     bgp log-neighbor-changes
     neighbor 10.0.0.2 remote-as 400
     neighbor 10.0.0.2 description "To Provider1"
     neighbor 10.0.0.2 advertisement-interval 0
     neighbor 10.0.0.2 soft-reconfiguration inbound
     neighbor 10.0.0.2 send-community
     neighbor 10.0.0.2 route-map R1_import_from_Provider1 in
     neighbor 10.0.0.2 route-map R1_export_to_Provider1 out
