; benchmark generated from python API

(set-info :status unknown)

(declare-datatypes ((PrefixSort 0)) ((PrefixSort (APLPHA_128_DOT_0_DOT_1_DOT_0_SLASH_24) (APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24))))
 (declare-datatypes ((NextHopSort 0)) ((NextHopSort (R3_DASH_lo100) (R3_DASH_Fa0_DASH_0) (Provider2_DASH_Fa0_DASH_0) (R1_DASH_lo100) (APLPHA_0_DOT_0_DOT_0_DOT_0) (R2_DASH_Fa0_DASH_0) (Provider1_DASH_Fa0_DASH_0) (Customer_DASH_Fa0_DASH_0) (R1_DASH_Fa0_DASH_0) (R2_DASH_lo100) (Provider2Hop) (Provider1Hop))))
 (declare-datatypes ((BGPOriginSort 0)) ((BGPOriginSort (IGP) (EBGP) (INCOMPLETE))))

(declare-fun Var_325 () NextHopSort)
(declare-fun Var_306 () NextHopSort)
(declare-fun Var_303 () NextHopSort)
(declare-fun Var_302 () NextHopSort)
(declare-fun Var_329 () NextHopSort)
(declare-fun Var_380 () NextHopSort)
(declare-fun Var_381 () NextHopSort)
(declare-fun Var_328 () NextHopSort)
(declare-fun Constrain_161 () Bool)
(declare-fun Var_334 () Bool)
(declare-fun Constrain_180 () Bool)
(declare-fun Var_390 () Bool)
(declare-fun const_and_247 () Bool)
(declare-fun Var_357 () Bool)
(declare-fun const_and_200 () Bool)
(declare-fun Var_366 () Bool)
(declare-fun Constrain_206 () Bool)
(declare-fun Var_362 () Bool)
(declare-fun Constrain_203 () Bool)
(declare-fun Var_414 () Bool)
(declare-fun Constrain_266 () Bool)
(declare-fun const_and_181 () Bool)
(declare-fun Var_338 () Bool)
(declare-fun const_and_184 () Bool)
(declare-fun Var_87 () Bool)
(declare-fun const_and_2 () Bool)
(declare-fun Var_343 () Bool)
(declare-fun const_and_188 () Bool)
(declare-fun Var_138 () Bool)
(declare-fun const_and_14 () Bool)
(declare-fun Constrain_183 () Bool)
(declare-fun Var_386 () Bool)
(declare-fun const_and_244 () Bool)
(declare-fun Var_424 () Bool)
(declare-fun Constrain_276 () Bool)
(declare-fun Constrain_119 () Bool)
(declare-fun Constrain_199 () Bool)
(declare-fun Var_353 () Bool)
(declare-fun Constrain_196 () Bool)
(declare-fun Var_347 () Bool)
(declare-fun Constrain_190 () Bool)
(declare-fun Var_370 () Bool)
(declare-fun Constrain_210 () Bool)
(declare-fun Var_405 () Bool)
(declare-fun Constrain_259 () Bool)
(declare-fun Constrain_109 () Bool)
(declare-fun Var_372 () Bool)
(declare-fun Constrain_213 () Bool)
(declare-fun Var_201 () Bool)
(declare-fun Constrain_25 () Bool)
(declare-fun Constrain_133 () Bool)
(declare-fun Constrain_239 () Bool)
(declare-fun Var_216 () Bool)
(declare-fun Constrain_37 () Bool)
(declare-fun Var_399 () Bool)
(declare-fun const_and_254 () Bool)
(declare-fun Var_395 () Bool)
(declare-fun const_and_251 () Bool)
(declare-fun const_and_207 () Bool)
(declare-fun Var_422 () Bool)
(declare-fun Constrain_273 () Bool)
(declare-fun Constrain_240 () Bool)
(declare-fun Constrain_243 () Bool)
(declare-fun Constrain_246 () Bool)
(declare-fun const_and_267 () Bool)
(declare-fun Var_418 () Bool)
(declare-fun const_and_270 () Bool)
(declare-fun Var_409 () Bool)
(declare-fun const_and_263 () Bool)
(declare-fun Constrain_250 () Bool)
(declare-fun const_and_260 () Bool)
(declare-fun const_and_274 () Bool)
(declare-fun const_and_277 () Bool)
(declare-fun Constrain_13 () Bool)
(declare-fun Constrain_1 () Bool)
(declare-fun const_and_26 () Bool)
(declare-fun Constrain_269 () Bool)
(declare-fun Constrain_262 () Bool)
(declare-fun const_and_211 () Bool)
(declare-fun const_and_204 () Bool)
(declare-fun Constrain_253 () Bool)
(declare-fun Constrain_177 () Bool)
(declare-fun Constrain_176 () Bool)
(declare-fun const_and_38 () Bool)
(declare-fun const_and_214 () Bool)
(declare-fun const_and_191 () Bool)
(declare-fun const_and_197 () Bool)
(declare-fun Constrain_187 () Bool)
(assert
 (let (($x800 (= $x799 true)))
 (=> Constrain_161 $x800)))))
(assert
(assert
(assert
(assert
(assert
(assert
(assert
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x782 (and $x781)))
(assert
(assert
 (let (($x730 (and $x729)))
(assert
(assert
 (let (($x736 (and $x735)))
(assert
 (let (($x806 (and $x805)))
(assert
 (let (($x870 (= Var_334 $x868)))
 (=> Constrain_180 $x870))))
(assert
 (=> const_and_247 $x1120)))
(assert
(assert
(assert
 (let (($x549 (and $x548)))
(assert
 (let (($x650 (and $x649)))
(assert
 (let (($x527 (and $x526)))
(assert
 (=> const_and_200 $x955)))
(assert
 (let (($x1055 (and $x1054)))
(assert
 (let (($x788 (and $x787)))
(assert
 (let (($x980 (= Var_366 $x134)))
 (=> Constrain_206 $x980))))
(assert
 (let (($x786 (and $x785)))
(assert
 (let (($x967 (= Var_362 $x633)))
 (=> Constrain_203 $x967))))
(assert
 (let (($x535 (and $x534)))
(assert
 (let (($x1199 (= Var_414 $x1166)))
 (=> Constrain_266 $x1199))))
(assert
 (let (($x565 (and $x564)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
 (=> const_and_181 $x874)))
(assert
 (let (($x1369 (and $x1368)))
(assert
 (=> const_and_184 $x889)))
(assert
 (=> const_and_2 $x140)))
(assert
 (let (($x1295 (and $x1294)))
(assert
 (let (($x1093 (or $x1090 $x1091 $x1092)))
(assert
 (=> const_and_188 $x905)))
(assert
 (let (($x810 (and $x809)))
(assert
 (let (($x1285 (and $x1284)))
(assert
 (let (($x1371 (and $x1370)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
(assert
(assert
 (let (($x724 (and $x723)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (=> const_and_14 $x238)))
(assert
(assert
 (let (($x165 (and $x164)))
(assert
 (let (($x802 (and $x801)))
(assert
 (let (($x634 (and $x633)))
(assert
(assert
 (let (($x927 (and $x913 $x926)))
(assert
 (let (($x885 (= Var_338 $x883)))
 (=> Constrain_183 $x885))))
(assert
(assert
(assert
(assert
 (=> const_and_244 $x1106)))
(assert
 (let (($x1239 (= Var_424 $x1181)))
 (=> Constrain_276 $x1239))))
(assert
 (let (($x399 (or $x396 $x397 $x398)))
(assert
 (let (($x1310 (and false true)))
 (let (($x1330 (= $x1310 false)))
 (let (($x1327 (= (or false (and true $x1313)) true)))
 (let (($x1312 (and true $x1311)))
 (let (($x1326 (= $x1312 false)))
 (let (($x684 (or (and (= EBGP IGP) (and (distinct EBGP IGP) true)) (and (= EBGP EBGP) (= EBGP INCOMPLETE)))))
 (let (($x700 (= $x684 false)))
 (let (($x1328 (= $x1310 true)))
 (let (($x698 (= $x684 true)))
 (let (($x1337 (= (and $x1335) true)))
(assert
 (let (($x664 (= $x663 true)))
 (=> Constrain_119 $x664)))))
(assert
 (let (($x551 (and $x550)))
(assert
 (let (($x630 (and $x629)))
(assert
(assert
 (let (($x1069 (and $x1068)))
(assert
 (let (($x1157 (and $x1143 $x1156)))
(assert
 (let (($x555 (and $x554)))
(assert
 (let (($x951 (= Var_357 $x134)))
 (=> Constrain_199 $x951))))
(assert
 (let (($x674 (and $x673)))
(assert
(assert
(assert
 (let (($x1384 (and $x1383)))
(assert
 (let (($x1061 (and $x1060)))
(assert
 (let (($x937 (= Var_353 $x633)))
 (=> Constrain_196 $x937))))
(assert
 (let (($x915 (= Var_347 $x883)))
 (=> Constrain_190 $x915))))
(assert
 (let (($x994 (= Var_370 $x633)))
 (=> Constrain_210 $x994))))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
(assert
(assert
 (let (($x1375 (and $x1374)))
(assert
(assert
 (let (($x808 (and $x807)))
(assert
(assert
(assert
(assert
 (let (($x519 (and $x518)))
(assert
 (let (($x1168 (= Var_405 $x1166)))
 (=> Constrain_259 $x1168))))
(assert
 (let (($x804 (and $x803)))
(assert
(assert
 (let (($x964 (and $x949 $x963)))
(assert
(assert
(assert
 (let (($x1373 (and $x1372)))
(assert
 (let (($x561 (and $x560)))
(assert
(assert
 (let (($x734 (and $x733)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
(assert
 (let (($x1057 (and $x1056)))
(assert
 (let (($x229 (or $x226 $x227 $x228)))
(assert
(assert
 (let (($x571 (and $x570)))
(assert
 (let (($x537 (and $x536)))
(assert
 (let (($x643 (ite $x640 (= Var_302 R2_DASH_lo100) $x642)))
 (let (($x644 (= $x643 true)))
 (=> Constrain_109 $x644))))))
(assert
(assert
(assert
 (let (($x638 (and $x637)))
(assert
 (let (($x1075 (and $x1074)))
(assert
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
 (let (($x589 (and true $x581)))
(assert
 (let (($x654 (and $x653)))
(assert
 (let (($x1007 (= Var_372 $x134)))
 (=> Constrain_213 $x1007))))
(assert
 (let (($x1224 (and $x1210 $x1223)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
(assert
(assert
 (let (($x1392 (and $x1391)))
(assert
 (let (($x343 (= Var_201 $x341)))
 (=> Constrain_25 $x343))))
(assert
 (let (($x622 (and (= (and (not true)) true) true)))
(assert
 (let (($x860 (or $x857 $x858 $x859)))
(assert
 (let (($x865 (or $x862 $x863 $x864)))
(assert
(assert
(assert
 (let (($x533 (and $x532)))
(assert
 (let (($x814 (and $x813)))
(assert
 (let (($x523 (and $x522)))
(assert
(assert
(assert
 (let (($x636 (and $x635)))
(assert
 (let (($x547 (and $x546)))
(assert
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x1037 (and $x1028 $x1036)))
(assert
 (let (($x721 (ite $x718 (= Var_306 R1_DASH_lo100) $x720)))
 (let (($x722 (= $x721 true)))
 (=> Constrain_133 $x722))))))
(assert
 (let (($x1059 (and $x1058)))
(assert
 (let (($x678 (and $x677)))
(assert
 (let (($x652 (and $x651)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
 (let (($x670 (and $x669)))
(assert
 (let (($x1377 (and $x1376)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
(assert
 (let (($x1065 (and $x1064)))
(assert
 (let (($x628 (and $x627)))
(assert
 (let (($x1293 (and $x1292)))
(assert
 (let (($x812 (and $x811)))
(assert
 (let (($x794 (and $x793)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
 (let (($x569 (and $x568)))
(assert
 (let (($x1081 (ite $x640 (= Var_380 R2_DASH_lo100) $x1080)))
 (let (($x1082 (= $x1081 true)))
 (=> Constrain_239 $x1082))))))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
 (let (($x543 (and $x542)))
(assert
 (let (($x1309 (and $x1308)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
 (let (($x404 (= Var_216 $x402)))
 (=> Constrain_37 $x404))))
(assert
 (let (($x784 (and $x783)))
(assert
 (=> const_and_254 $x1149)))
(assert
 (let (($x626 (and $x625)))
(assert
 (let (($x648 (and $x647)))
(assert
(assert
 (=> const_and_251 $x1136)))
(assert
 (let (($x1379 (and $x1378)))
(assert
 (let (($x1396 (and $x1395)))
(assert
(assert
 (let (($x778 (and $x777)))
(assert
 (let (($x131 (or $x126 $x128 $x130)))
(assert
 (let (($x1390 (and $x1389)))
(assert
(assert
 (=> const_and_207 $x984)))
(assert
(assert
 (let (($x742 (or $x740 $x741)))
(assert
 (let (($x1063 (and $x1062)))
(assert
 (let (($x815 (and false false)))
 (let (($x835 (= $x815 false)))
 (let (($x832 (= (or true (and false $x818)) true)))
 (let (($x817 (and false $x816)))
 (let (($x831 (= $x817 false)))
 (let (($x684 (or (and (= EBGP IGP) (and (distinct EBGP IGP) true)) (and (= EBGP EBGP) (= EBGP INCOMPLETE)))))
 (let (($x700 (= $x684 false)))
 (let (($x698 (= $x684 true)))
 (let (($x840 (or $x823 $x825 $x827 $x828 $x830 $x834 $x837 $x839)))
 (let (($x842 (= (and $x840) true)))
(assert
 (let (($x632 (and $x631)))
(assert
 (let (($x1299 (and $x1298)))
(assert
 (let (($x1067 (and $x1066)))
(assert
(assert
 (let (($x1226 (= Var_422 $x1166)))
 (=> Constrain_273 $x1226))))
(assert
(assert
 (let (($x728 (and $x727)))
(assert
 (let (($x1088 (= $x1087 true)))
 (=> Constrain_240 $x1088)))))
(assert
 (let (($x1102 (= Var_386 $x793)))
 (=> Constrain_243 $x1102))))
(assert
 (let (($x182 (and $x181)))
(assert
 (let (($x573 (and $x572)))
(assert
(assert
 (let (($x1386 (and $x1385)))
(assert
 (let (($x1116 (= Var_390 $x232)))
 (=> Constrain_246 $x1116))))
(assert
 (let (($x263 (and $x262)))
(assert
 (let (($x1051 (and $x1050)))
(assert
 (let (($x1388 (and $x1387)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x1310 (and false true)))
 (let (($x1330 (= $x1310 false)))
 (let (($x1354 (= (or false (and true $x1340)) true)))
 (let (($x1339 (and true $x1338)))
 (let (($x1353 (= $x1339 false)))
 (let (($x684 (or (and (= EBGP IGP) (and (distinct EBGP IGP) true)) (and (= EBGP EBGP) (= EBGP INCOMPLETE)))))
 (let (($x700 (= $x684 false)))
 (let (($x1328 (= $x1310 true)))
 (let (($x698 (= $x684 true)))
 (let (($x1362 (= (and $x1360) true)))
(assert
 (let (($x557 (and $x556)))
(assert
 (let (($x619 (and $x618)))
(assert
(assert
 (let (($x666 (and $x665)))
(assert
(assert
(assert
(assert
 (let (($x525 (and $x524)))
(assert
 (let (($x1053 (and $x1052)))
(assert
 (=> const_and_267 $x1203)))
(assert
(assert
(assert
 (let (($x1077 (and $x1076)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
 (=> const_and_270 $x1216)))
(assert
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
(assert
 (let (($x726 (and $x725)))
(assert
 (=> const_and_263 $x1187)))
(assert
(assert
 (let (($x732 (and $x731)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
(assert
 (let (($x1283 (and $x1282)))
(assert
(assert
 (let (($x338 (or $x335 $x336 $x337)))
(assert
 (let (($x1132 (= Var_395 $x793)))
 (=> Constrain_250 $x1132))))
(assert
 (=> const_and_260 $x1172)))
(assert
 (let (($x280 (and $x279)))
(assert
 (let (($x1394 (and $x1393)))
(assert
 (let (($x559 (and $x558)))
(assert
 (let (($x1301 (and $x1300)))
(assert
 (let (($x658 (and $x657)))
(assert
(assert
 (let (($x1367 (and $x1366)))
(assert
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (=> const_and_274 $x1230)))
(assert
 (let (($x676 (and $x675)))
(assert
 (=> const_and_277 $x1243)))
(assert
 (let (($x539 (and $x538)))
(assert
 (let (($x1073 (and $x1072)))
(assert
 (let (($x234 (= Var_138 $x232)))
 (=> Constrain_13 $x234))))
(assert
 (let (($x646 (and $x645)))
(assert
 (let (($x685 (and true true)))
 (let (($x707 (= $x685 false)))
 (let (($x704 (= (or true (and false $x688)) true)))
 (let (($x687 (and false $x686)))
 (let (($x703 (= $x687 false)))
 (let (($x684 (or (and (= EBGP IGP) (and (distinct EBGP IGP) true)) (and (= EBGP EBGP) (= EBGP INCOMPLETE)))))
 (let (($x700 (= $x684 false)))
 (let (($x698 (= $x684 true)))
 (let (($x714 (= (and $x712) true)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x541 (and $x540)))
(assert
 (let (($x589 (and true $x581)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
(assert
(assert
 (let (($x1291 (and $x1290)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x136 (= Var_87 $x134)))
 (=> Constrain_1 $x136))))
(assert
(assert
(assert
 (let (($x1305 (and $x1304)))
(assert
 (=> const_and_26 $x347)))
(assert
 (let (($x1071 (and $x1070)))
(assert
(assert
 (let (($x1289 (and $x1288)))
(assert
 (let (($x1212 (= Var_418 $x1181)))
 (=> Constrain_269 $x1212))))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x567 (and $x566)))
(assert
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
(assert
 (let (($x622 (and (= (and (not true)) true) true)))
(assert
 (let (($x668 (and $x667)))
(assert
 (let (($x583 (or $x581 $x582)))
(assert
 (let (($x1196 (and $x1180 $x1195)))
(assert
 (let (($x545 (and $x544)))
(assert
 (let (($x748 (and true $x740)))
(assert
 (let (($x372 (and $x371)))
(assert
 (let (($x656 (and $x655)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x389 (and $x388)))
(assert
 (let (($x1183 (= Var_409 $x1181)))
 (=> Constrain_262 $x1183))))
(assert
(assert
 (let (($x553 (and $x552)))
(assert
 (=> const_and_211 $x998)))
(assert
 (=> const_and_204 $x971)))
(assert
 (let (($x529 (and $x528)))
(assert
 (let (($x1287 (and $x1286)))
(assert
 (let (($x520 (= EBGP EBGP)))
 (let (($x521 (and $x520)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
 (let (($x1145 (= Var_399 $x232)))
 (=> Constrain_253 $x1145))))
(assert
 (let (($x855 (= $x854 true)))
 (=> Constrain_177 $x855)))))
(assert
 (let (($x848 (ite $x718 (= Var_328 R1_DASH_lo100) $x847)))
 (let (($x849 (= $x848 true)))
 (=> Constrain_176 $x849))))))
(assert
 (=> const_and_38 $x408)))
(assert
(assert
 (=> const_and_214 $x1011)))
(assert
 (let (($x792 (and $x791)))
(assert
 (let (($x992 (and $x978 $x991)))
(assert
(assert
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
(assert
(assert
(assert
 (let (($x1307 (and $x1306)))
(assert
 (let (($x1303 (and $x1302)))
(assert
 (let (($x1297 (and $x1296)))
(assert
 (let (($x1269 (and $x1260 $x1268)))
(assert
 (let (($x516 (= APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24 APLPHA_128_DOT_0_DOT_0_DOT_0_SLASH_24)))
 (let (($x517 (and $x516)))
(assert
(assert
 (let (($x531 (and $x530)))
(assert
(assert
(assert
(assert
 (let (($x450 (and $x449)))
(assert
 (let (($x672 (and $x671)))
(assert
(assert
 (let (($x433 (and $x432)))
(assert
 (=> const_and_191 $x919)))
(assert
 (let (($x563 (and $x562)))
(assert
 (let (($x748 (and true $x740)))
(assert
(assert
 (let (($x1098 (or $x1095 $x1096 $x1097)))
(assert
 (=> const_and_197 $x941)))
(assert
 (let (($x901 (= Var_343 $x868)))
 (=> Constrain_187 $x901))))
(assert
 (let (($x575 (and $x574)))
(assert
(assert
 (let (($x790 (and $x789)))
(assert
(assert
(check-sat)
