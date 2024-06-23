Z3 EnumSort
-----------

The Z3 EnumSort SMT formula as follows

  + (declare-datatypes ((PrefixSort 0)) ((PrefixSort (APLPHA_128_DOT_0_DOT_1_DOT_0_SLASH_24) (APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24))))

  + (declare-datatypes ((NextHopSort 0)) ((NextHopSort (R3_DASH_lo100) (R3_DASH_Fa0_DASH_0) (Provider2_DASH_Fa0_DASH_0) (R1_DASH_lo100) (APLPHA_0_DOT_0_DOT_0_DOT_0) (R2_DASH_Fa0_DASH_0) (Provider1_DASH_Fa0_DASH_0) (Customer_DASH_Fa0_DASH_0) (R1_DASH_Fa0_DASH_0) (R2_DASH_lo100) (Provider2Hop) (Provider1Hop))))

  + (declare-datatypes ((BGPOriginSort 0)) ((BGPOriginSort (IGP) (EBGP) (INCOMPLETE))))


UPDATE message (announcements)
------------------------------

The BGP UPDATE messages may carry one or more Path Attributes, NetComplete use the following Path Attributes

  * prefix: the network prefix that's being announced
  * peer: the peer from whom what prefix has been received
  * origin: bgp attrs origin, ibgp, ebgp or incomplete
  * as_path: as path, list of as numbers
  * as_path_len: as path length
  * next_hop: 
        1. If the BGP Peers are in different AS then the next_hop IP address
           that will be sent in the update message will be the IP address of
           the advertising router.
        2. If the BGP peers are in the same AS (IBGP Peers),
            and the destination network being advertised in the update message
            is also in the same AS, then the next_hop IP address that will be sent
            in the update message will be the IP address of the advertising router.
        3. If the BGP peers are in the same AS (IBGP Peers),
            and the destination network being advertised in the update message
            is in an external AS, then the next_hop IP address that will be
            sent in the update message will be the IP address of the external
            peer router which sent the advertisement to this AS.
  * local_pref: is only used in updates sent to the IBGP Peers,
                It is not passed on to the BGP peers in other autonomous systems.
  * med: MED value, int
  * communities: dict Community values, Community->True/False
  * permitted: permit or deny, Access.permit or Access.deny
  * prev_announcement: keep track of the announcement that generated this one

The BGP UPDATE message SMT formula as follows

  * Sham_{}_{}_from_{}_{}_{}.format(node, network_prefix, peer, path_attr, unique_value)

  + Sham_R3_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_R1_next_hop_155
  + Sham_R3_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_R1_med_157
  + Sham_R1_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_R2_local_pref_66
  + Sham_R2_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_R1_permitted_131
  + Sham_Provider2_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_None_permitted_248
  + Sham_R2_128_DOT_0_DOT_0_DOT_0_SLASH_24_from_Provider2_Comm_Community_OPENP_100_3_CLOSEP__121


Path Requirements
-----------------

The Path Requirement ( allow, block, best path over other path ) SMT formula as follows

    # Path Requirement - Allow
  * Req_Allow_{}_from_{}_path_{}_{}.format(node, peer, path, unique_value)

    # Path Requirement - Block
  * Req_Block_{}_from_{}_path_{}_{}.format(node, peer, path, unique_value)

    # TODO best path over other path ??
  * igp_{}_is_equal_{}{}.format(best_path, other_path, unique_value)

  + Req_Allow_Customer_from_R3_path_Provider2_R2_R1_R3_Customer_49
  + Req_Block_Provider1_from_R1_path_Provider2_R2_R1_Provider1_315

  + igp_Provider1_R1_R2_is_equal_Provider2_R2326
  + igp_Provider1_R1_R2_R3_is_equal_Provider2_R2_R1_R3434


Select Best Route
-----------------

The Select Best Route SMT formula as follows

  * SELECT_at_{}_prefix_{}_path_{}_{}.format(node, network_prefix, best_path, unique_value)

  + SELECT_at_R2_prefix_128_DOT_0_DOT_0_DOT_0_SLASH_24_path_Provider1_R1_R2_171
  + SELECT_at_R3_prefix_128_DOT_0_DOT_0_DOT_0_SLASH_24_path_Provider1_R1_R2_R3_303


Route Map
---------

The Route Map SMT formula as follows

    # logic to ensure that the announcement is matched against only one line
  * SelectOneRmapLineIndex_{}.format(unique_value)

    # bound the selector variable only to the available route map line numbers
  * RmapIndexBound_{}_{}.format(route_map_name, unique_value)

    # TODO not understand
  * rmap_{}_order_{}.format(route_map_name, unique_value)

  + SelectOneRmapLineIndex_84
  + RmapIndexBound_R3_import_from_R2_241
  + RmapIndexBound_R1_export_to_Provider1_0

  + rmap_R3_export_to_R1_order_29
  + rmap_R3_import_from_R2_order_275
  + rmap_R3_import_from_R2_order_278
  + rmap_R3_import_from_R2_order_283


Route Map Import
----------------

The Import Route Map SMT formula as follows

  * Imp_{}_from_{}_{}_{}.format(node, neighbor, attr, unique_value)
  * Imp_{}_from_{}_Comm_{}_{}.format(node, neighbor, community_name, unique_value)

  + Imp_R1_from_R2_origin_112
  + Imp_R2_from_Provider2_next_hop_153
  + Imp_R2_from_R1_Comm_Comm_100_1_142


Route Map Match
---------------

The Route Map Match function SMT formula as follows

    # matches all announcements regardless of its contents
  * match_all_{}.format(unique_value)

    # does NOT match any announcement regardless of its contents
  * match_none_{}.format(unique_value)

    # combine matches in `And` expression
  * match_and_{}.format(unique_value)

    # combine matches in `Or` expression
  * match_or_{}.format(unique_value)

    # TODO not understand
  * match_sel_{}.format(unique_value)
  * Selector_{}.format(unique_value)

  ...... ......


Route Map Set Action
--------------------

The Route Map Set Action function SMT formula as follows

    # action to change one attribute in the announcement
  * Set_{}_val_{}.format(attr, unique_value)
  * Action_set_{}_val_{}_{}.format(attr, value_name, unique_value)

    # action to change community attribute in the announcement
  * Set_community_val_{}.format(unique_value)
  * set_community_{}_val{}.format(community_name, uniqu_value)
  * Set_comm_{}.format(unique_value)

  + Set_comm_95

    # short cut to set the value of announcement.permitted
  * Set_permitted_val_{}.format(unique_value)
  * Set_{}_{}.format(attr, unique_value)
  * ActionPermittedVal{}.format(unique_value)

  + Set_permitted_4
  + Set_permitted_281
  + ActionPermittedVal90
  + ActionPermittedVal94

  ...... ......










                                            paths attrs +
      Provider1          R1 -> Provider1    block attrs [Provider2, R2, R1, Provider1]
         |                                  ---> UPDATE message
         R1              configuration sketch R1_export_to_Provider1


         paths_attrs_1 or block_attrs_1  ->  export or import
                                         ->  other export or import route map




