from http.server import BaseHTTPRequestHandler, HTTPServer
import secp256k1 as ice
from bit import Key
import hashlib, base58, binascii, random, time

hostName = "localhost"
serverPort = 3333
    
class WebServer(BaseHTTPRequestHandler):
    ##########_class_attributes_###########################################################
    num,startPrivKey,random,random5H,random5J,random5K = (0,0,0,0,0,0)
    randomKw=randomKx=randomKy=randomKz=0
    randomL1=randomL2=randomL3=randomL4=randomL5=0
    previous = 0
    next = 0
    max = 904625697166532776746648320380374280100293470930272690489102837043110636675
    middle = 452312848583266388373324160190187140050146735465136345244551418521555318338
    hj = 85966769946697919304477156997851416897897452779964215616135418886216209408
    jk = 551340488851368173693535237984541213163631919119002481700768830238824024064
    L1 = 398639737335773246472125555160783623763937797351505550641748492138749584881
    L2 = 504075970525112600982146526634330530730393262381443907801548249398324792889
    L3 = 609512203714451955492167498107877437696848727411382264961348006657900000897
    L4 = 714948436903791310002188469581424344663304192441320622121147763917475208905
    L5 = 820384670093130664512209441054971251629759657471258979280947521177050416913
    Kx = 82331037767755182942062640740142902864571402261690479162349220360023960857
    Ky = 187767270957094537452083612213689809831026867291628836322148977619599168865
    Kz = 293203504146433891962104583687236716797482332321567193481948734879174376873
    randomMin = 1;
    randomMax = max;
    rndMin = 1
    rndMax = max
    first = 1;
    stride = 1;
    #-------------------------------------------------------------------------------------
    p1 = 1
    p2 = 1
    p3 = 1
    p4 = 1
    p5 = 1
    p6 = 1
    p7 = 2
    p8 = 3
    p9 = 5
    p10 = 9
    p11 = 17
    p12 = 33
    p13 = 65
    p14 = 129
    p15 = 257
    p16 = 513
    p17 = 1025
    p18 = 2049
    p19 = 4097
    p20 = 8193
    p21 = 16385
    p22 = 32769
    p23 = 65537
    p24 = 131073
    p25 = 262145
    p26 = 524289
    p27 = 1048577
    p28 = 2097153
    p29 = 4194305
    p30 = 8388609
    p31 = 16777217
    p32 = 33554433
    p33 = 67108865
    p34 = 134217729
    p35 = 268435457
    p36 = 536870913
    p37 = 1073741825
    p38 = 2147483649
    p39 = 4294967297
    p40 = 8589934593
    p41 = 17179869185
    p42 = 34359738369
    p43 = 68719476737
    p44 = 137438953473
    p45 = 274877906945
    p46 = 549755813889
    p47 = 1099511627777
    p48 = 2199023255553
    p49 = 4398046511105
    p50 = 8796093022209
    p51 = 17592186044417
    p52 = 35184372088833
    p53 = 70368744177665
    p54 = 140737488355329
    p55 = 281474976710657
    p56 = 562949953421313
    p57 = 1125899906842625
    p58 = 2251799813685249
    p59 = 4503599627370497
    p60 = 9007199254740993
    p61 = 18014398509481985
    p62 = 36028797018963969
    p63 = 72057594037927937
    p64 = 144115188075855873
    p65 = 288230376151711745
    p66 = 576460752303423489
    p67 = 1152921504606846977
    p68 = 2305843009213693953
    p69 = 4611686018427387905
    p70 = 9223372036854775809
    p71 = 18446744073709551617
    p72 = 36893488147419103233
    p73 = 73786976294838206465
    p74 = 147573952589676412929
    p75 = 295147905179352825857
    p76 = 590295810358705651713
    p77 = 1180591620717411303425
    p78 = 2361183241434822606849
    p79 = 4722366482869645213697
    p80 = 9444732965739290427393
    p81 = 18889465931478580854785
    p82 = 37778931862957161709569
    p83 = 75557863725914323419137
    p84 = 151115727451828646838273
    p85 = 302231454903657293676545
    p86 = 604462909807314587353089
    p87 = 1208925819614629174706177
    p88 = 2417851639229258349412353
    p89 = 4835703278458516698824705
    p90 = 9671406556917033397649409
    p91 = 19342813113834066795298817
    p92 = 38685626227668133590597633
    p93 = 77371252455336267181195265
    p94 = 154742504910672534362390529
    p95 = 309485009821345068724781057
    p96 = 618970019642690137449562113
    p97 = 1237940039285380274899124225
    p98 = 2475880078570760549798248449
    p99 = 4951760157141521099596496897
    p100 = 9903520314283042199192993793
    p101 = 19807040628566084398385987585
    p102 = 39614081257132168796771975169
    p103 = 79228162514264337593543950337
    p104 = 158456325028528675187087900673
    p105 = 316912650057057350374175801345
    p106 = 633825300114114700748351602689
    p107 = 1267650600228229401496703205377
    p108 = 2535301200456458802993406410753
    p109 = 5070602400912917605986812821505
    p110 = 10141204801825835211973625643009
    p111 = 20282409603651670423947251286017
    p112 = 40564819207303340847894502572033
    p113 = 81129638414606681695789005144065
    p114 = 162259276829213363391578010288129
    p115 = 324518553658426726783156020576257
    p116 = 649037107316853453566312041152513
    p117 = 1298074214633706907132624082305025
    p118 = 2596148429267413814265248164610049
    p119 = 5192296858534827628530496329220097
    p120 = 10384593717069655257060992658440193
    p121 = 20769187434139310514121985316880385
    p122 = 41538374868278621028243970633760769
    p123 = 83076749736557242056487941267521537
    p124 = 166153499473114484112975882535043073
    p125 = 332306998946228968225951765070086145
    p126 = 664613997892457936451903530140172289
    p127 = 1329227995784915872903807060280344577
    p128 = 2658455991569831745807614120560689153
    p129 = 5316911983139663491615228241121378305
    p130 = 10633823966279326983230456482242756609
    p131 = 21267647932558653966460912964485513217
    p132 = 42535295865117307932921825928971026433
    p133 = 85070591730234615865843651857942052865
    p134 = 170141183460469231731687303715884105729
    p135 = 340282366920938463463374607431768211457
    p136 = 680564733841876926926749214863536422913
    p137 = 1361129467683753853853498429727072845825
    p138 = 2722258935367507707706996859454145691649
    p139 = 5444517870735015415413993718908291383297
    p140 = 10889035741470030830827987437816582766593
    p141 = 21778071482940061661655974875633165533185
    p142 = 43556142965880123323311949751266331066369
    p143 = 87112285931760246646623899502532662132737
    p144 = 174224571863520493293247799005065324265473
    p145 = 348449143727040986586495598010130648530945
    p146 = 696898287454081973172991196020261297061889
    p147 = 1393796574908163946345982392040522594123777
    p148 = 2787593149816327892691964784081045188247553
    p149 = 5575186299632655785383929568162090376495105
    p150 = 11150372599265311570767859136324180752990209
    p151 = 22300745198530623141535718272648361505980417
    p152 = 44601490397061246283071436545296723011960833
    p153 = 89202980794122492566142873090593446023921665
    p154 = 178405961588244985132285746181186892047843329
    p155 = 356811923176489970264571492362373784095686657
    p156 = 713623846352979940529142984724747568191373313
    p157 = 1427247692705959881058285969449495136382746625
    p158 = 2854495385411919762116571938898990272765493249
    p159 = 5708990770823839524233143877797980545530986497
    p160 = 11417981541647679048466287755595961091061972993
    p161 = 22835963083295358096932575511191922182123945985
    p162 = 45671926166590716193865151022383844364247891969
    p163 = 91343852333181432387730302044767688728495783937
    p164 = 182687704666362864775460604089535377456991567873
    p165 = 365375409332725729550921208179070754913983135745
    p166 = 730750818665451459101842416358141509827966271489
    p167 = 1461501637330902918203684832716283019655932542977
    p168 = 2923003274661805836407369665432566039311865085953
    p169 = 5846006549323611672814739330865132078623730171905
    p170 = 11692013098647223345629478661730264157247460343809
    p171 = 23384026197294446691258957323460528314494920687617
    p172 = 46768052394588893382517914646921056628989841375233
    p173 = 93536104789177786765035829293842113257979682750465
    p174 = 187072209578355573530071658587684226515959365500929
    p175 = 374144419156711147060143317175368453031918731001857
    p176 = 748288838313422294120286634350736906063837462003713
    p177 = 1496577676626844588240573268701473812127674924007425
    p178 = 2993155353253689176481146537402947624255349848014849
    p179 = 5986310706507378352962293074805895248510699696029697
    p180 = 11972621413014756705924586149611790497021399392059393
    p181 = 23945242826029513411849172299223580994042798784118785
    p182 = 47890485652059026823698344598447161988085597568237569
    p183 = 95780971304118053647396689196894323976171195136475137
    p184 = 191561942608236107294793378393788647952342390272950273
    p185 = 383123885216472214589586756787577295904684780545900545
    p186 = 766247770432944429179173513575154591809369561091801089
    p187 = 1532495540865888858358347027150309183618739122183602177
    p188 = 3064991081731777716716694054300618367237478244367204353
    p189 = 6129982163463555433433388108601236734474956488734408705
    p190 = 12259964326927110866866776217202473468949912977468817409
    p191 = 24519928653854221733733552434404946937899825954937634817
    p192 = 49039857307708443467467104868809893875799651909875269633
    p193 = 98079714615416886934934209737619787751599303819750539265
    p194 = 196159429230833773869868419475239575503198607639501078529
    p195 = 392318858461667547739736838950479151006397215279002157057
    p196 = 784637716923335095479473677900958302012794430558004314113
    p197 = 1569275433846670190958947355801916604025588861116008628225
    p198 = 3138550867693340381917894711603833208051177722232017256449
    p199 = 6277101735386680763835789423207666416102355444464034512897
    p200 = 12554203470773361527671578846415332832204710888928069025793
    p201 = 25108406941546723055343157692830665664409421777856138051585
    p202 = 50216813883093446110686315385661331328818843555712276103169
    p203 = 100433627766186892221372630771322662657637687111424552206337
    p204 = 200867255532373784442745261542645325315275374222849104412673
    p205 = 401734511064747568885490523085290650630550748445698208825345
    p206 = 803469022129495137770981046170581301261101496891396417650689
    p207 = 1606938044258990275541962092341162602522202993782792835301377
    p208 = 3213876088517980551083924184682325205044405987565585670602753
    p209 = 6427752177035961102167848369364650410088811975131171341205505
    p210 = 12855504354071922204335696738729300820177623950262342682411009
    p211 = 25711008708143844408671393477458601640355247900524685364822017
    p212 = 51422017416287688817342786954917203280710495801049370729644033
    p213 = 102844034832575377634685573909834406561420991602098741459288065
    p214 = 205688069665150755269371147819668813122841983204197482918576129
    p215 = 411376139330301510538742295639337626245683966408394965837152257
    p216 = 822752278660603021077484591278675252491367932816789931674304513
    p217 = 1645504557321206042154969182557350504982735865633579863348609025
    p218 = 3291009114642412084309938365114701009965471731267159726697218049
    p219 = 6582018229284824168619876730229402019930943462534319453394436097
    p220 = 13164036458569648337239753460458804039861886925068638906788872193
    p221 = 26328072917139296674479506920917608079723773850137277813577744385
    p222 = 52656145834278593348959013841835216159447547700274555627155488769
    p223 = 105312291668557186697918027683670432318895095400549111254310977537
    p224 = 210624583337114373395836055367340864637790190801098222508621955073
    p225 = 421249166674228746791672110734681729275580381602196445017243910145
    p226 = 842498333348457493583344221469363458551160763204392890034487820289
    p227 = 1684996666696914987166688442938726917102321526408785780068975640577
    p228 = 3369993333393829974333376885877453834204643052817571560137951281153
    p229 = 6739986666787659948666753771754907668409286105635143120275902562305
    p230 = 13479973333575319897333507543509815336818572211270286240551805124609
    p231 = 26959946667150639794667015087019630673637144422540572481103610249217
    p232 = 53919893334301279589334030174039261347274288845081144962207220498433
    p233 = 107839786668602559178668060348078522694548577690162289924414440996865
    p234 = 215679573337205118357336120696157045389097155380324579848828881993729
    p235 = 431359146674410236714672241392314090778194310760649159697657763987457
    p236 = 862718293348820473429344482784628181556388621521298319395315527974913
    p237 = 1725436586697640946858688965569256363112777243042596638790631055949825
    p238 = 3450873173395281893717377931138512726225554486085193277581262111899649
    p239 = 6901746346790563787434755862277025452451108972170386555162524223799297
    p240 = 13803492693581127574869511724554050904902217944340773110325048447598593
    p241 = 27606985387162255149739023449108101809804435888681546220650096895197185
    p242 = 55213970774324510299478046898216203619608871777363092441300193790394369
    p243 = 110427941548649020598956093796432407239217743554726184882600387580788737
    p244 = 220855883097298041197912187592864814478435487109452369765200775161577473
    p245 = 441711766194596082395824375185729628956870974218904739530401550323154945
    p246 = 883423532389192164791648750371459257913741948437809479060803100646309889
    p247 = 1766847064778384329583297500742918515827483896875618958121606201292619777
    p248 = 3533694129556768659166595001485837031654967793751237916243212402585239553
    p249 = 7067388259113537318333190002971674063309935587502475832486424805170479105
    p250 = 14134776518227074636666380005943348126619871175004951664972849610340958209
    p251 = 28269553036454149273332760011886696253239742350009903329945699220681916417
    p252 = 56539106072908298546665520023773392506479484700019806659891398441363832833
    p253 = 113078212145816597093331040047546785012958969400039613319782796882727665665
    p254 = 226156424291633194186662080095093570025917938800079226639565593765455331329
    p255 = 452312848583266388373324160190187140051835877600158453279131187530910662657
    #-------------------------------------------------------------------------------------
    idx1,idx2,idx3 = (0,0,0)
    hashKey=privKey=privKey_C=bitAddr=bitAddr_C=searchKey = ""
    starting_key_hex = ""
    ending_key_hex = ""
    privateKey = privateKey_C = ""
    publicKey = publicKey_C = ""
    addresses = list()           
    arr = set()
    filename = "address.txt"
    print(f"Creating database from \"{filename}\"...Wait...")
    with open(filename) as in_file:
        for addr in in_file:
            bit_addr = addr.strip()
            arr.add(bit_addr)
    addr_count = len(arr)
    print("Addresses loaded: " + str(addr_count))
    foundling = ""
    balance_on_page = "False"        
    def RandomInteger(minN, maxN):
        return random.randrange(minN, maxN)
    ##########_webserver_work_############################################################
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<!DOCTYPE html>","utf-8"))
        self.wfile.write(bytes("<html>","utf-8"))
        self.wfile.write(bytes("<head>","utf-8"))
        self.wfile.write(bytes("<title>BTC&ETH_WebServer(Mizogg)</title>","utf-8"))
        self.wfile.write(bytes("<style>body{font-size:9.5pt;font-family:'Open Sans',sans-serif;}a{text-decoration:none}a:hover {text-decoration: underline}lol: target {background: #ccffcc; }</style>","utf-8"))
        self.wfile.write(bytes("</head>","utf-8"))
        self.wfile.write(bytes("<body link='#0000FF' vlink='#0000FF' alink='#0000FF'>","utf-8"))
        self.wfile.write(bytes("<h1><span style='color:#34495E;'>Bitcoin and ETH Private Key Database: " + str(__class__.addr_count) + " Addresses Loaded </span></h1>", "utf-8"))
        ###-------------------------------------------------------------------------------
        if self.path.startswith('/5H') or self.path.startswith('/5J') or self.path.startswith('/5K'):
            first_encode = base58.b58decode(self.path[1:])
            private_key_full = binascii.hexlify(first_encode)
            private_key = private_key_full[2:-8]
            private_key_hex = private_key.decode("utf-8")
            keyU = Key.from_int(int(private_key_hex,16))
            keyU._public_key = keyU._pk.public_key.format(compressed=False)
            __class__.searchKey = keyU.address
            __class__.num = int(private_key_hex,16);
            __class__.num = __class__.num // 128
            __class__.num = __class__.num + 1
            __class__.previous = __class__.num - 1
            if (__class__.previous == 0):
                __class__.previous = 1
            __class__.next = __class__.num + __class__.stride;                
            if (__class__.next > __class__.max):
                __class__.next = __class__.max
            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
        elif self.path.startswith('/K') or self.path.startswith('/L'):
            first_encode = base58.b58decode(self.path[1:])
            private_key_full = binascii.hexlify(first_encode)
            private_key = private_key_full[2:-8]
            private_key_hex = private_key.decode("utf-8")
            keyC = Key.from_int(int(private_key_hex[0:64],16))
            __class__.searchKey = keyC.address
            __class__.num = int(private_key_hex[0:64],16);
            __class__.num = __class__.num // 128
            __class__.num = __class__.num + 1
            __class__.previous = __class__.num - 1
            if (__class__.previous == 0):
                __class__.previous = 1
            __class__.next = __class__.num + __class__.stride                
            if (__class__.next > __class__.max):
                __class__.next = __class__.max
            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
        else:
            str_url = self.path[1:]
            if str_url.find("[") > 0:
                __class__.idx1 = str_url.index("[")
                __class__.idx2 = str_url.index("]")
                __class__.num = int(str_url[0:__class__.idx1],10)
                __class__.stride = int(str_url[__class__.idx1+1:__class__.idx2],10)
                __class__.previous = __class__.num - 1
                if __class__.previous == 0:
                    __class__.previous = 1
                __class__.next = __class__.num + __class__.stride                
                if __class__.next > __class__.max:
                    __class__.next = __class__.max
                __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            elif str_url.find("(") > 0:
                pass
            else:
                if str_url == 'favicon.ico':
                    pass
                else:
                    __class__.num = int(str_url,10)
                    __class__.previous = __class__.num - 1;
                    if __class__.previous == 0:
                        __class__.previous = 1
                    __class__.next = __class__.num + __class__.stride                
                    if __class__.next > __class__.max:
                        __class__.next = __class__.max
                    __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)                
        ###-------------------------------------------------------------------------------
        __class__.startPrivKey = (__class__.num - 1) * 128+1
        __class__.random5H = __class__.RandomInteger(__class__.rndMin,__class__.hj)
        __class__.random5J = __class__.RandomInteger(__class__.hj,__class__.jk)
        __class__.random5K = __class__.RandomInteger(__class__.jk,__class__.rndMax)
         
        __class__.randomKw = __class__.RandomInteger(__class__.rndMin,__class__.Kx)
        __class__.randomKx = __class__.RandomInteger(__class__.Kx,__class__.Ky)
        __class__.randomKy = __class__.RandomInteger(__class__.Ky,__class__.Kz)
        __class__.randomKz = __class__.RandomInteger(__class__.Kz,__class__.L1)
        
        __class__.randomL1 = __class__.RandomInteger(__class__.L1,__class__.L2) 
        __class__.randomL2 = __class__.RandomInteger(__class__.L2,__class__.L3)
        __class__.randomL3 = __class__.RandomInteger(__class__.L3,__class__.L4)
        __class__.randomL4 = __class__.RandomInteger(__class__.L4,__class__.L5)
        __class__.randomL5 = __class__.RandomInteger(__class__.L5,__class__.rndMax)
        #_________________________________________________________________________________                             
        self.wfile.write(bytes("<h2><span style='color:#D7DBDD;background-color:#145A32;padding:2px;border-radius: 2px;'>Page #</span> <span style='color:#145A32;padding:2px;background-color:#D7DBDD;border-radius: 2px;'>" + str(__class__.num) + "</span> <span style='color:#145A32;'><< out of >></span> <span style='color:#145A32;padding:2px;background-color:#D7DBDD;border-radius: 2px;'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h2>", "utf-8"))
        self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Current page increment for next = " + str(__class__.stride) + "</p>", "utf-8"))
        self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Current random range = " + str(__class__.randomMin) + " - " + str(__class__.randomMax) + "</p>", "utf-8"))
        self.wfile.write(bytes("<pre class='keys'>[&nbsp;<a id='backseq' href='/"+str(__class__.previous)+"'>previous</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='nextseq' href='/"+str(__class__.next)+"'>next</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randec' href='/"+str(__class__.random)+"'>random</a>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
        self.wfile.write(bytes("[&nbsp;<a id='first' href='/"+str(__class__.first)+"'>first</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='middle' href='/"+str(__class__.middle)+"'>middle</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='last' href='/"+str(__class__.max)+"'>last</a>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
        self.wfile.write(bytes("[&nbsp;<a id='5Jstart' href='/"+str(__class__.hj)+"'>5H(end)-5J(start)</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='5Kstart' href='/"+str(__class__.jk)+"'>5J(end)-5K(start)</a>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
        self.wfile.write(bytes("[&nbsp;<a id='random5H' href='/"+str(__class__.random5H)+"'>5H_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='random5J' href='/"+str(__class__.random5J)+"'>5J_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='random5K' href='/"+str(__class__.random5K)+"'>5K_random</a>&nbsp;]", "utf-8"))
        self.wfile.write(bytes("</pre>", "utf-8"))
        
        self.wfile.write(bytes("<pre class='keys'>[&nbsp;<a id='kxstart' href='/"+str(__class__.Kx)+"'>Kw(end)_Kx(start)</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='Kystart' href='/"+str(__class__.Ky)+"'>Kx(end)_Ky(start)</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='Kzstart' href='/"+str(__class__.Kz)+"'>Ky(end)_Kz(start)</a>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
        self.wfile.write(bytes("[&nbsp;<a id='L1start' href='/"+str(__class__.L1)+"'>Kz(end)-L1(start)</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='L2start' href='/"+str(__class__.L2)+"'>L1(end)_L2(start)</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='L3start' href='/"+str(__class__.L3)+"'>L2(end)_L3(start)</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='L4start' href='/"+str(__class__.L4)+"'>L3(end)_L4(start)</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='L5start' href='/"+str(__class__.L5)+"'>L4(end)_L5(start)</a>&nbsp;]", "utf-8"))
        self.wfile.write(bytes("</pre>", "utf-8"))
        
        self.wfile.write(bytes("<pre class='keys'>[&nbsp;<a id='randomKw' href='/"+str(__class__.randomKw)+"'>Kw_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randomKx' href='/"+str(__class__.randomKx)+"'>Kx_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randomKy' href='/"+str(__class__.randomKy)+"'>Ky_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randomKz' href='/"+str(__class__.randomKz)+"'>Kz_random</a>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
        self.wfile.write(bytes("[&nbsp;<a id='randomL1' href='/"+str(__class__.randomL1)+"'>L1_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randomL2' href='/"+str(__class__.randomL2)+"'>L2_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randomL3' href='/"+str(__class__.randomL3)+"'>L3_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randomL4' href='/"+str(__class__.randomL4)+"'>L4_random</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randomL5' href='/"+str(__class__.randomL5)+"'>L5_random</a>&nbsp;]", "utf-8"))
        self.wfile.write(bytes("</pre>", "utf-8"))
        
        self.wfile.write(bytes("<pre>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p255)+"'>2^255</a>|<a href='/"+str(__class__.p254)+"'>2^254</a>|<a href='/"+str(__class__.p253)+"'>2^253</a>|<a href='/"+str(__class__.p252)+"'>2^252</a>|<a href='/"+str(__class__.p251)+"'>2^251</a>|<a href='/"+str(__class__.p250)+"'>2^250</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p249)+"'>2^249</a>|<a href='/"+str(__class__.p248)+"'>2^248</a>|<a href='/"+str(__class__.p247)+"'>2^247</a>|<a href='/"+str(__class__.p246)+"'>2^246</a>|<a href='/"+str(__class__.p245)+"'>2^245</a>|<a href='/"+str(__class__.p244)+"'>2^244</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p243)+"'>2^243</a>|<a href='/"+str(__class__.p242)+"'>2^242</a>|<a href='/"+str(__class__.p241)+"'>2^241</a>|<a href='/"+str(__class__.p240)+"'>2^240</a>|<a href='/"+str(__class__.p239)+"'>2^239</a>|<a href='/"+str(__class__.p238)+"'>2^238</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p237)+"'>2^237</a>|<a href='/"+str(__class__.p236)+"'>2^236</a>|<a href='/"+str(__class__.p235)+"'>2^235</a>|<a href='/"+str(__class__.p234)+"'>2^234</a>|<a href='/"+str(__class__.p233)+"'>2^233</a>|<a href='/"+str(__class__.p232)+"'>2^232</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p231)+"'>2^231</a>|<a href='/"+str(__class__.p230)+"'>2^230</a>|<a href='/"+str(__class__.p229)+"'>2^229</a>|<a href='/"+str(__class__.p228)+"'>2^228</a>|<a href='/"+str(__class__.p227)+"'>2^227</a>|<a href='/"+str(__class__.p226)+"'>2^226</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p225)+"'>2^225</a>|<a href='/"+str(__class__.p224)+"'>2^224</a>|<a href='/"+str(__class__.p223)+"'>2^223</a>|<a href='/"+str(__class__.p222)+"'>2^222</a>|<a href='/"+str(__class__.p221)+"'>2^221</a>|<a href='/"+str(__class__.p220)+"'>2^220</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p219)+"'>2^219</a>|<a href='/"+str(__class__.p218)+"'>2^218</a>|<a href='/"+str(__class__.p217)+"'>2^217</a>|<a href='/"+str(__class__.p216)+"'>2^216</a>|<a href='/"+str(__class__.p215)+"'>2^215</a>|<a href='/"+str(__class__.p214)+"'>2^214|</a><br>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p213)+"'>2^213</a>|<a href='/"+str(__class__.p212)+"'>2^212</a>|<a href='/"+str(__class__.p211)+"'>2^211</a>|<a href='/"+str(__class__.p210)+"'>2^210</a>|<a href='/"+str(__class__.p209)+"'>2^209</a>|<a href='/"+str(__class__.p208)+"'>2^208</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p207)+"'>2^207</a>|<a href='/"+str(__class__.p206)+"'>2^206</a>|<a href='/"+str(__class__.p205)+"'>2^205</a>|<a href='/"+str(__class__.p204)+"'>2^204</a>|<a href='/"+str(__class__.p203)+"'>2^203</a>|<a href='/"+str(__class__.p202)+"'>2^202</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p201)+"'>2^201</a>|<a href='/"+str(__class__.p200)+"'>2^200</a>|<a href='/"+str(__class__.p199)+"'>2^199</a>|<a href='/"+str(__class__.p198)+"'>2^198</a>|<a href='/"+str(__class__.p197)+"'>2^197</a>|<a href='/"+str(__class__.p196)+"'>2^196</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p195)+"'>2^195</a>|<a href='/"+str(__class__.p194)+"'>2^194</a>|<a href='/"+str(__class__.p193)+"'>2^193</a>|<a href='/"+str(__class__.p192)+"'>2^192</a>|<a href='/"+str(__class__.p191)+"'>2^191</a>|<a href='/"+str(__class__.p190)+"'>2^190</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p189)+"'>2^189</a>|<a href='/"+str(__class__.p188)+"'>2^188</a>|<a href='/"+str(__class__.p187)+"'>2^187</a>|<a href='/"+str(__class__.p186)+"'>2^186</a>|<a href='/"+str(__class__.p185)+"'>2^185</a>|<a href='/"+str(__class__.p184)+"'>2^184</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p183)+"'>2^183</a>|<a href='/"+str(__class__.p182)+"'>2^182</a>|<a href='/"+str(__class__.p181)+"'>2^181</a>|<a href='/"+str(__class__.p180)+"'>2^180</a>|<a href='/"+str(__class__.p179)+"'>2^179</a>|<a href='/"+str(__class__.p178)+"'>2^178</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p177)+"'>2^177</a>|<a href='/"+str(__class__.p176)+"'>2^176</a>|<a href='/"+str(__class__.p175)+"'>2^175</a>|<a href='/"+str(__class__.p174)+"'>2^174</a>|<a href='/"+str(__class__.p173)+"'>2^173</a>|<a href='/"+str(__class__.p172)+"'>2^172|</a><br>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p171)+"'>2^171</a>|<a href='/"+str(__class__.p170)+"'>2^170</a>|<a href='/"+str(__class__.p169)+"'>2^169</a>|<a href='/"+str(__class__.p168)+"'>2^168</a>|<a href='/"+str(__class__.p167)+"'>2^167</a>|<a href='/"+str(__class__.p166)+"'>2^166</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p165)+"'>2^165</a>|<a href='/"+str(__class__.p164)+"'>2^164</a>|<a href='/"+str(__class__.p163)+"'>2^163</a>|<a href='/"+str(__class__.p162)+"'>2^162</a>|<a href='/"+str(__class__.p161)+"'>2^161</a>|<a href='/"+str(__class__.p160)+"'>2^160</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p159)+"'>2^159</a>|<a href='/"+str(__class__.p158)+"'>2^158</a>|<a href='/"+str(__class__.p157)+"'>2^157</a>|<a href='/"+str(__class__.p156)+"'>2^156</a>|<a href='/"+str(__class__.p155)+"'>2^155</a>|<a href='/"+str(__class__.p154)+"'>2^154</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p153)+"'>2^153</a>|<a href='/"+str(__class__.p152)+"'>2^152</a>|<a href='/"+str(__class__.p151)+"'>2^151</a>|<a href='/"+str(__class__.p150)+"'>2^150</a>|<a href='/"+str(__class__.p149)+"'>2^149</a>|<a href='/"+str(__class__.p148)+"'>2^148</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p147)+"'>2^147</a>|<a href='/"+str(__class__.p146)+"'>2^146</a>|<a href='/"+str(__class__.p145)+"'>2^145</a>|<a href='/"+str(__class__.p144)+"'>2^144</a>|<a href='/"+str(__class__.p143)+"'>2^143</a>|<a href='/"+str(__class__.p142)+"'>2^142</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p141)+"'>2^141</a>|<a href='/"+str(__class__.p140)+"'>2^140</a>|<a href='/"+str(__class__.p139)+"'>2^139</a>|<a href='/"+str(__class__.p138)+"'>2^138</a>|<a href='/"+str(__class__.p137)+"'>2^137</a>|<a href='/"+str(__class__.p136)+"'>2^136</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p135)+"'>2^135</a>|<a href='/"+str(__class__.p134)+"'>2^134</a>|<a href='/"+str(__class__.p133)+"'>2^133</a>|<a href='/"+str(__class__.p132)+"'>2^132</a>|<a href='/"+str(__class__.p131)+"'>2^131</a>|<a href='/"+str(__class__.p130)+"'>2^130|</a><br>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p129)+"'>2^129</a>|<a href='/"+str(__class__.p128)+"'>2^128</a>|<a href='/"+str(__class__.p127)+"'>2^127</a>|<a href='/"+str(__class__.p126)+"'>2^126</a>|<a href='/"+str(__class__.p125)+"'>2^125</a>|<a href='/"+str(__class__.p124)+"'>2^124</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p123)+"'>2^123</a>|<a href='/"+str(__class__.p122)+"'>2^122</a>|<a href='/"+str(__class__.p121)+"'>2^121</a>|<a href='/"+str(__class__.p120)+"'>2^120</a>|<a href='/"+str(__class__.p119)+"'>2^119</a>|<a href='/"+str(__class__.p118)+"'>2^118</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p117)+"'>2^117</a>|<a href='/"+str(__class__.p116)+"'>2^116</a>|<a href='/"+str(__class__.p115)+"'>2^115</a>|<a href='/"+str(__class__.p114)+"'>2^114</a>|<a href='/"+str(__class__.p113)+"'>2^113</a>|<a href='/"+str(__class__.p112)+"'>2^112</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p111)+"'>2^111</a>|<a href='/"+str(__class__.p110)+"'>2^110</a>|<a href='/"+str(__class__.p109)+"'>2^109</a>|<a href='/"+str(__class__.p108)+"'>2^108</a>|<a href='/"+str(__class__.p107)+"'>2^107</a>|<a href='/"+str(__class__.p106)+"'>2^106</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p105)+"'>2^105</a>|<a href='/"+str(__class__.p104)+"'>2^104</a>|<a href='/"+str(__class__.p103)+"'>2^103</a>|<a href='/"+str(__class__.p102)+"'>2^102</a>|<a href='/"+str(__class__.p101)+"'>2^101</a>|<a href='/"+str(__class__.p100)+"'>2^100</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p99)+"'>2^99</a>|<a href='/"+str(__class__.p98)+"'>2^98</a>|<a href='/"+str(__class__.p97)+"'>2^97</a>|<a href='/"+str(__class__.p96)+"'>2^96</a>|<a href='/"+str(__class__.p95)+"'>2^95</a>|<a href='/"+str(__class__.p94)+"'>2^94</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p93)+"'>2^93</a>|<a href='/"+str(__class__.p92)+"'>2^92</a>|<a href='/"+str(__class__.p91)+"'>2^91</a>|<a href='/"+str(__class__.p90)+"'>2^90</a>|<a href='/"+str(__class__.p89)+"'>2^89</a>|<a href='/"+str(__class__.p88)+"'>2^88</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p87)+"'>2^87</a>|<a href='/"+str(__class__.p86)+"'>2^86|</a><br>|<a href='/"+str(__class__.p85)+"'>2^85</a>|<a href='/"+str(__class__.p84)+"'>2^84</a>|<a href='/"+str(__class__.p83)+"'>2^83</a>|<a href='/"+str(__class__.p82)+"'>2^82</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p81)+"'>2^81</a>|<a href='/"+str(__class__.p82)+"'>2^82</a>|<a href='/"+str(__class__.p81)+"'>2^81</a>|<a href='/"+str(__class__.p80)+"'>2^80</a>|<a href='/"+str(__class__.p79)+"'>2^79</a>|<a href='/"+str(__class__.p78)+"'>2^78</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p77)+"'>2^77</a>|<a href='/"+str(__class__.p76)+"'>2^76</a>|<a href='/"+str(__class__.p75)+"'>2^75</a>|<a href='/"+str(__class__.p74)+"'>2^74</a>|<a href='/"+str(__class__.p73)+"'>2^73</a>|<a href='/"+str(__class__.p72)+"'>2^72</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p71)+"'>2^71</a>|<a href='/"+str(__class__.p70)+"'>2^70</a>|<a href='/"+str(__class__.p69)+"'>2^69</a>|<a href='/"+str(__class__.p68)+"'>2^68</a>|<a href='/"+str(__class__.p67)+"'>2^67</a>|<a href='/"+str(__class__.p66)+"'>2^66</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p65)+"'>2^65</a>|<a href='/"+str(__class__.p64)+"'>2^64</a>|<a href='/"+str(__class__.p63)+"'>2^63</a>|<a href='/"+str(__class__.p62)+"'>2^62</a>|<a href='/"+str(__class__.p61)+"'>2^61</a>|<a href='/"+str(__class__.p60)+"'>2^60</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p59)+"'>2^59</a>|<a href='/"+str(__class__.p58)+"'>2^58</a>|<a href='/"+str(__class__.p57)+"'>2^57</a>|<a href='/"+str(__class__.p56)+"'>2^56</a>|<a href='/"+str(__class__.p55)+"'>2^55</a>|<a href='/"+str(__class__.p54)+"'>2^54</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p53)+"'>2^53</a>|<a href='/"+str(__class__.p52)+"'>2^52</a>|<a href='/"+str(__class__.p51)+"'>2^51</a>|<a href='/"+str(__class__.p50)+"'>2^50</a>|<a href='/"+str(__class__.p49)+"'>2^49</a>|<a href='/"+str(__class__.p48)+"'>2^48</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p47)+"'>2^47</a>|<a href='/"+str(__class__.p46)+"'>2^46</a>|<a href='/"+str(__class__.p45)+"'>2^45</a>|<a href='/"+str(__class__.p44)+"'>2^44</a>|<a href='/"+str(__class__.p43)+"'>2^43</a>|<a href='/"+str(__class__.p42)+"'>2^42</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p41)+"'>2^41</a>|<a href='/"+str(__class__.p40)+"'>2^40</a>|<a href='/"+str(__class__.p39)+"'>2^39</a>|<a href='/"+str(__class__.p38)+"'>2^38|</a><br>|<a href='/"+str(__class__.p37)+"'>2^37</a>|<a href='/"+str(__class__.p36)+"'>2^36</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p35)+"'>2^35</a>|<a href='/"+str(__class__.p34)+"'>2^34</a>|<a href='/"+str(__class__.p33)+"'>2^33</a>|<a href='/"+str(__class__.p32)+"'>2^32</a>|<a href='/"+str(__class__.p31)+"'>2^31</a>|<a href='/"+str(__class__.p30)+"'>2^30</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p29)+"'>2^29</a>|<a href='/"+str(__class__.p28)+"'>2^28</a>|<a href='/"+str(__class__.p27)+"'>2^27</a>|<a href='/"+str(__class__.p26)+"'>2^26</a>|<a href='/"+str(__class__.p25)+"'>2^25</a>|<a href='/"+str(__class__.p24)+"'>2^24</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p23)+"'>2^23</a>|<a href='/"+str(__class__.p22)+"'>2^22</a>|<a href='/"+str(__class__.p21)+"'>2^21</a>|<a href='/"+str(__class__.p20)+"'>2^20</a>|<a href='/"+str(__class__.p19)+"'>2^19</a>|<a href='/"+str(__class__.p18)+"'>2^18</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p17)+"'>2^17</a>|<a href='/"+str(__class__.p16)+"'>2^16</a>|<a href='/"+str(__class__.p15)+"'>2^15</a>|<a href='/"+str(__class__.p14)+"'>2^14</a>|<a href='/"+str(__class__.p13)+"'>2^13</a>|<a href='/"+str(__class__.p12)+"'>2^12</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p11)+"'>2^11</a>|<a href='/"+str(__class__.p10)+"'>2^10</a>|<a href='/"+str(__class__.p9)+"'>2^9</a>|<a href='/"+str(__class__.p8)+"'>2^8</a>|<a href='/"+str(__class__.p7)+"'>2^7</a>|<a href='/"+str(__class__.p6)+"'>2^6</a>", "utf-8"))
        self.wfile.write(bytes("|<a href='/"+str(__class__.p5)+"'>2^5</a>|<a href='/"+str(__class__.p4)+"'>2^4</a>|<a href='/"+str(__class__.p3)+"'>2^3</a>|<a href='/"+str(__class__.p2)+"'>2^2</a>|<a href='/"+str(__class__.p1)+"'>2^1|</a>", "utf-8"))
        self.wfile.write(bytes("</pre>", "utf-8"))
        
        __class__.starting_key_hex = hex(__class__.startPrivKey)[2:].zfill(64)
        if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494273:
            __class__.ending_key_hex = hex(__class__.startPrivKey+63)[2:].zfill(64)
        else:
            __class__.ending_key_hex = hex(__class__.startPrivKey+127)[2:].zfill(64)
            
        self.wfile.write(bytes("<p style='color:gray;font-weight:bold;'>*Starting Private Key Hex: " + str(__class__.starting_key_hex) + "</p>", "utf-8"))
        self.wfile.write(bytes("<p style='color:gray;font-weight:bold;'>**Ending Private Key Hex: " + str(__class__.ending_key_hex) + "</p>", "utf-8"))
        self.wfile.write(bytes("<p id='balance' style='color:brown;font-weight:bold;'>Balance on this Page: False</p>", "utf-8"))
        self.wfile.write(bytes("<pre class='keys'><strong>Private Key Hex</strong>                                                          <strong>Uncompressed Address</strong>                <strong>Compressed Address</strong>                       <strong>SegWit 3 Address</strong>                  <strong>bech32 bc1 Address</strong>                           <strong>ETH Address</strong>                           <strong>WIF Private Key Uncompressed</strong>                            <strong>WIF Private Key Compressed</strong><br>", "utf-8"))
        ###---Loop---******************************************************************
        for i in range(0,128):
            dec = int(__class__.startPrivKey)
            HEX = "%064x" % dec
            __class__.privKey_C = ice.btc_pvk_to_wif(HEX)
            __class__.privKey = ice.btc_pvk_to_wif(HEX, False)
            __class__.bitAddr_C = ice.privatekey_to_address(0, True, dec) #Compressed
            __class__.bitAddr = ice.privatekey_to_address(0, False, dec)  #Uncompressed
            __class__.bitAddr_S = ice.privatekey_to_address(1, True, dec) #p2sh
            __class__.bitAddr_bech32 = ice.privatekey_to_address(2, True, dec)  #bech32
            __class__.bitAddr_eth = ice.privatekey_to_ETH_address(dec)
            __class__.addresses.append(__class__.bitAddr.strip());
            __class__.addresses.append(__class__.bitAddr_C.strip());
            __class__.addresses.append(__class__.bitAddr_S.strip());
            __class__.addresses.append(__class__.bitAddr_bech32.strip());
            __class__.addresses.append(__class__.bitAddr_eth.strip());
            __class__.starting_key_hex = hex(__class__.startPrivKey)[2:].zfill(64)
            if __class__.bitAddr in  __class__.arr or __class__.bitAddr_C in __class__.arr or __class__.bitAddr_S in __class__.arr or __class__.bitAddr_bech32 in __class__.arr or __class__.bitAddr_eth in __class__.arr:
                print (f"""\n
Bitcoin Address UnCompressed :  {__class__.bitAddr}
Private Key WIF UnCompressed : {__class__.privKey}
Bitcoin Address Compressed   :  {__class__.bitAddr_C}
Private Key WIF Compressed   : {__class__.privKey_C}
Bitcoin Address SegWit 3    :  {__class__.bitAddr_S}
Bitcoin Address bc1   :  {__class__.bitAddr_bech32}
Ethereum  Address       :  {__class__.bitAddr_eth}
Private Key HEX: {__class__.starting_key_hex}        """)
                with open("winner.txt", "a", encoding="utf-8") as f:
                    f.write(f"""\n
Bitcoin Address UnCompressed :  {__class__.bitAddr}
Private Key WIF UnCompressed : {__class__.privKey}
Bitcoin Address Compressed   :  {__class__.bitAddr_C}
Private Key WIF Compressed   : {__class__.privKey_C}
Bitcoin Address SegWit 3    :  {__class__.bitAddr_S}
Bitcoin Address bc1   :  {__class__.bitAddr_bech32}
Ethereum  Address       :  {__class__.bitAddr_eth}
Private Key HEX: {__class__.starting_key_hex}        """)
            if __class__.bitAddr == __class__.searchKey or __class__.bitAddr_C == __class__.searchKey or __class__.bitAddr_S == __class__.searchKey or __class__.bitAddr_bech32 == __class__.searchKey or __class__.bitAddr_eth == __class__.searchKey:
                self.wfile.write(bytes("<lol>" + __class__.starting_key_hex + "</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#DE3163;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr + "'>" +"<strong>"+ __class__.bitAddr+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C+"'>"+"<strong>"+ __class__.bitAddr_C + "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_S+"'>"+"<strong>"+ __class__.bitAddr_S + "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32+"'>"+"<strong>"+ __class__.bitAddr_bech32 + "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://ethplorer.io/address/" + __class__.bitAddr_eth+"'>"+"<strong>"+ __class__.bitAddr_eth +"</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol>" +"&nbsp;&nbsp;<lol>"+"<strong>"+ __class__.privKey+ "</strong>"+"</lol><lol style='color:#145A32;'>" +"&nbsp;&nbsp;<lol>"+"<strong>"+ __class__.privKey_C+ "</strong>"+"</lol></br>", "utf-8"))
                __class__.searchKey = ""
            else:
                self.wfile.write(bytes("<lol style='color:#DE3163;'>" + __class__.starting_key_hex + "</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a>" + "&nbsp<span>"  + "</span>&nbsp" + "</lol>&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_S + "'>" + __class__.bitAddr_S + "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32 + "'>" + __class__.bitAddr_bech32 + "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://ethplorer.io/address/" + __class__.bitAddr_eth + "'>" + __class__.bitAddr_eth + "</a></lol>&nbsp;&nbsp;<lol style='color:#145A32;'>" + "&nbsp;&nbsp;<lol>" + "&nbsp;&nbsp<span>"  + "</span>&nbsp;&nbsp</lol>&nbsp;&nbsp;" + __class__.privKey + "</lol><lol style='color:#145A32;'>" +"&nbsp;&nbsp;<lol>"+__class__.privKey_C+"</lol></br>", "utf-8"))
            if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                 break
            __class__.startPrivKey += 1
        ###---Loop---******************************************************************
        for addr in __class__.addresses:
            if addr in __class__.arr:
                __class__.balance_on_page = "True"
                __class__.foundling = addr + " "
        self.wfile.write(bytes("</pre><pre class='keys'>[&nbsp;<a id='backseq' href='/"+str(__class__.previous)+"'>previous</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='nextseq' href='/"+str(__class__.next)+"'>next</a> | ", "utf-8"))
        self.wfile.write(bytes("<a id='randec' href='/"+str(__class__.random)+"'>random</a>&nbsp;]", "utf-8"))
        self.wfile.write(bytes("</pre>", "utf-8"))
        self.wfile.write(bytes("<p id='found' style='color:brown;font-weight:bold;'>Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "</p>", "utf-8"))
        self.wfile.write(bytes("<script>var elem = document.getElementById('balance');elem.innerHTML = 'Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "'</script>", "utf-8"))
        self.wfile.write(bytes("<h3><span style='color:#34495E;'>Mizogg's Version 2022 https://mizogg.co.uk</span></h3>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        __class__.addresses.clear()
        __class__.balance_on_page = "False"
        __class__.foundling = ""
    ######################################################################################
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), WebServer)
    print("Server started at http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
