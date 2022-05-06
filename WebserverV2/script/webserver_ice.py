#28/04/2022
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import secp256k1 as ice
import hashlib
import base58
import binascii
import random
import sys
import os
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate
from pathlib import Path

hostName = "localhost"
serverPort = 3333

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
    
class WebServer(BaseHTTPRequestHandler):
    ##########_class_attributes_###########################################################
    num,startPrivKey,random,random5H,random5J,random5K = (0,0,0,0,0,0) #num(page number) startPrivKey(key to start generating 128U and 128C addresses on the page from)
    randomKw=randomKx=randomKy=randomKz=0
    randomL1=randomL2=randomL3=randomL4=randomL5=0
    previous = 0
    next = 0
    max = 904625697166532776746648320380374280100293470930272690489102837043110636675    # max page
    #unique X coords : 57896044618658097711785492504343953926418782139537452191302581570759080747168
    #unique Y coords : 19298681539552699237261830834781317975472927379845817397100860523586360249056(points have three different X-coordinates with the same Y-coordinate)
    #Add Y three time: 57896044618658097711785492504343953926418782139537452191302581570759080747168
    #*******Add X + X: 115792089237316195423570985008687907852837564279074904382605163141518161494336(all possible private keys(Group elements in terms of Group Theory)
    # page middle of range(7fffffffffffffffffffffffffffffff5d576e7357a4501ddfe92f46681b20a0 and next have the same X right in the middle(then x coordinates go in the mirror order)
    middle = 452312848583266388373324160190187140050146735465136345244551418521555318338 
    #---------------------------------------------------------------------------------------
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
    randomMin = 1
    randomMax = max
    rndMin = 1
    rndMax = max
    first = 1
    stride = 1
    #---pages numbers from 2**1 to 2**255----------------------------------
    p1=p2=p3=p4=p5=p6=1
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
    idx1,idx2,idx3 = (0,0,0) #index values when we parse different page requests
    privKey=privKey_C=bitAddr=bitAddr_C=searchKey=searchKey_U = "" #searchKey when we search for page by pasting privatekey hex in url localhost:3333/$fff 
    starting_key_hex = ""                                          #searchKeyU when we search for page by pasting privatekey decimal in url localhost:3333/@10985746
    ending_key_hex = ""
    privateKey = privateKey_C = ""
    publicKey = publicKey_C = ""
    addresses = list()  #saves all generated addresses on page here to check if any in loaded arr set
    #-------creating set in memory with addresses(probably the best option for fast elements search but takes more memory because of hashtable)               
    bloombtc = Path(__file__).resolve()
    ressbtc = bloombtc.parents[1] / 'datafiles/BF/btc.bf'
    bloometh = Path(__file__).resolve()
    resseth = bloometh.parents[1] / 'datafiles/BF/eth.bf'
    
    
    with open(resseth, "rb") as fp:
        bloom_filter1 = BloomFilter.load(fp)   

    with open(ressbtc, "rb") as fp:
        bloom_filter = BloomFilter.load(fp)
    
    addr_count = len(bloom_filter)+len(bloom_filter1)
    #--------------------------------------------
    foundling = "" #string for found addresses
    balance_on_page = "False"
    #---check if string is hex value---------------
    def isHex(s):
        for ch in s:
            if ((ch < '0' or ch > '9') and
                (ch < 'A' or ch > 'F') and
                (ch < 'a' or ch > 'f')):                 
                return False
        return True
    #---function for random pages----------      
    def RandomInteger(minN, maxN):
        return random.randrange(minN, maxN)
    #---shut server logging the fuck up----in case you need it just comment this function
    #def log_message(self, format, *args):
        #pass
    ##########_webserver_work_############################################################
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
#-------------------------------------------------------------------------------------------------AJAX Fetch Page PART---------------------------------------
        str_url = self.path[1:] #removing / from url as we do not need it
        if str_url.startswith("!"): # handle ajax request to get all data for modal popup window
            idxN = str_url.index("!") #find ! after goes the number we need
            numb = int(str_url[idxN+1:],10) #get the number from url
            P = ice.scalar_multiplication(numb).hex() #getting point coordinates
            P_X = P[2:66]
            P_Y = P[66:]
            #---getting additive inverse point coordinates and checking addresses for balance
            #(additive inverse points have the same X-coords but different Y-coords thus when added yield Point at Infinity(0,0)) 
            add_inv = 115792089237316195423570985008687907852837564279074904382605163141518161494337 - numb
            addrC = ice.privatekey_to_address(0, True, add_inv)   #Compressed
            addrU = ice.privatekey_to_address(0, False, add_inv)  #Uncompressed
            a2 = list()
            b_word = "No"
            a2.append(addrC)
            a2.append(addrU)
            for addr in a2:
                if addr in __class__.arr:
                    b_word = "Yes"
            AP = ice.scalar_multiplication(add_inv).hex()            
            AP_X = AP[2:66]
            AP_Y = AP[66:]
            #---getting two other points X-coordinates with same Y-coordinate(will generate all three from P_Y one we already have=P_X)
            y = int(P_Y, 16)
            p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f  ## Field parameters
            beta = 0x7ae96a2b657c07106e64479eac3434e99cf0497512f58995c1396c28719501ee # Cube root
            xcubed = (y*y - 7) % p
            x = pow(xcubed, (p + 2) * pow(9, p - 2, p) % p , p)
            plist = list()#start calculating X-coords and putting them in plist will get two as result(because one we already have from P_X)
            x1 = str(hex(x))[2:].zfill(64)
            if x1 != P_X:
                plist.append(x1)
            x2 = str(hex((x * beta % p)))[2:].zfill(64)
            if x2 != P_X:
                plist.append(x2)
            x3 = str(hex((x * beta * beta % p)))[2:].zfill(64)
            if x3 != P_X:
                plist.append(x3)
            #getting addresses and check if they are in arr set(two times necessary to know which pair exactly has it)
            sameaddr1U = ice.pubkey_to_address(0, False, bytes(bytearray.fromhex('04'+plist[0]+P_Y)))
            sameaddr1C = ice.pubkey_to_address(0, True, bytes(bytearray.fromhex('04'+plist[0]+P_Y)))
            same_1 = list()
            b_word_same1 = "No"
            same_1.append(sameaddr1U)
            same_1.append(sameaddr1C)
            for addr in same_1:
                if addr in __class__.arr:
                    b_word_same1 = "Yes"
            sameaddr2U = ice.pubkey_to_address(0, False, bytes(bytearray.fromhex('04'+plist[1]+P_Y)))
            sameaddr2C = ice.pubkey_to_address(0, True, bytes(bytearray.fromhex('04'+plist[1]+P_Y)))
            same_2 = list()
            b_word_same2 = "No"
            same_2.append(sameaddr2U)
            same_2.append(sameaddr2C)
            for addr in same_2:
                if addr in __class__.arr:
                    b_word_same2 = "Yes"             
            #----getting compressed public key format
            if (ord(bytearray.fromhex(P[-2:])) % 2 == 0):
                pubkey_compressed = '02'
            else:
                pubkey_compressed = '03'
            pubkey_compressed += P[2:66]
            #-----getting ripemd160 hash----------------------
            rmdU = ice.privatekey_to_h160(0, False, numb).hex()  #Uncompressed RIPEMD160
            rmdC = ice.privatekey_to_h160(0, True, numb).hex()  #Compressed RIPEMD160
            #---sending ajax response (" " to split data elements)
            self.wfile.write(bytes(P_X+" "+P_Y+" " \
            +str(int(P_X,16))+" "+str(int(P_Y,16))+" " \
            +rmdU+" "+rmdC+" "+str(bin(numb)[2:])+" " \
            +pubkey_compressed+ " "+AP_X+" "+AP_Y+ " "+addrU+" "+addrC+" " \
            +str(hex(add_inv)[2:].zfill(64))+" "+b_word+" " \
            +plist[0]+" "+sameaddr1U+" "+sameaddr1C+" "+b_word_same1+" " \
            +plist[1]+" "+sameaddr2U+" "+sameaddr2C+" "+b_word_same2+" "+str(numb)+" "+str(hex(numb)[2:].zfill(64)),"utf-8"))
#---------End for AJAX modal windows---------------------------------------------------------------------------------------------
        elif str_url.startswith("P"): #Pilot mode
            addresses = list()
            str_url = self.path[2:]
            page_num = int(str_url,10)               
            ###---------setting startPrivKey(start to generate addresses from)----------------
            startPrivKey = (page_num - 1) * 128+1
            for i in range(0,128): #generating addresses and WIFS to show on page
                dec = int(startPrivKey)
                HEX = "%064x" % dec
                privKey_C = ice.btc_pvk_to_wif(HEX)
                privKey = ice.btc_pvk_to_wif(HEX, False)
                bitAddr_C = ice.privatekey_to_address(0, True, dec) #Compressed
                bitAddr = ice.privatekey_to_address(0, False, dec)  #Uncompressed
                bitAddr_bech32 = ice.privatekey_to_address(2, True, dec)  #bech32
                bitAddr_eth = ice.privatekey_to_ETH_address(dec)
                bitAddr_S = ice.privatekey_to_address(1, True, dec) #p2sh
                addresses.append(bitAddr.strip());
                addresses.append(bitAddr_C.strip());
                addresses.append(bitAddr_S.strip());
                addresses.append(bitAddr_bech32.strip());
                addresses.append(bitAddr_eth.strip());
                if startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                startPrivKey += 1
            ###---Loop---checking if generated addresses are in arr set(if yes then we found address with balance)
            status = 'No'
            for addr in addresses:
                if addr in __class__.bloom_filter or addr in __class__.bloom_filter1:
                    status = 'Yes'
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"Bitcoin or ETH Address: {addr}  Found on Page# {page_num} \n") #saving if found: address page#

            self.wfile.write(bytes(status, "utf-8"))
            addresses.clear()
            ###__Loop End-------------------------------------------------------------------
#-------#--------Search Field-----------------------------------------------------------------------------------------------------------------
        elif str_url.startswith("S"):
            self.wfile.write(bytes("""
<div class='overlay_popup'></div>
<div class='popup' id='popup1'>
<div class='object'>
<h4 style='color:brown;font-weight:bold;text-align:right;'>Private ECDSA Key&nbsp;&nbsp;
<button class='arrow' id='arrow_left' style='color:blue;margin-left:132px;'><<<</button>&nbsp;&nbsp;
<span style='color:brown;' id='arrow_num'>1</span> <span style='color:brown;'>of</span> <span  id='all_num' style='color:brown;'>128</span>&nbsp;&nbsp;
<button class='arrow' id='arrow_right' style='color:blue;'>>>></button>&nbsp;&nbsp;</h4>
<p id='funbin' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;word-wrap: break-word;'></p>
<p id='funhex' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<h4 style='color:brown;font-weight:bold;'>Public ECDSA Key</h4>
<p id='fun2x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun2y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun3x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun3y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun5' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>           
<h4 style='color:brown;font-weight:bold;'>Additive Inverse Point</h4>
<p id='addinvn' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addinvx' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addinvy' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addrinv' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<h4 style='color:brown;font-weight:bold;'>Two More Points same Y different X</h4>
<p id='same1x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same1y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same1addr' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2addr' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<h4 style='color:brown;font-weight:bold;'>RIPEMD-160 Hash</h4>
<p id='fun4' style='color:#34495E ;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>"
</div></div>""", "utf-8"))
            str_url = self.path[2:] #gettin / outta way from url we do not need
            if str_url.startswith('5H') or str_url.startswith('5J') or str_url.startswith('5K'): # if url starts with 5H 5J 5K we request page by 5WIF
                first_encode = base58.b58decode(self.path[2:])
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                keyU = int(private_key_hex,16)
                __class__.searchKey = ice.privatekey_to_address(0, False, keyU)
                __class__.num = int(private_key_hex,16)
                __class__.num = __class__.num // 128
                __class__.num = __class__.num + 1
                __class__.previous = __class__.num - 1
                if (__class__.previous == 0):
                    __class__.previous = 1
                __class__.next = __class__.num + __class__.stride;                
                if (__class__.next > __class__.max):
                    __class__.next = __class__.max
                __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            elif str_url.startswith('K') or str_url.startswith('L'): # if url starts with L K we request page by LWIF KWIF
                first_encode = base58.b58decode(self.path[2:])
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                keyC = int(private_key_hex[0:64],16)
                __class__.searchKey = ice.privatekey_to_address(0, True, keyC)
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
                if str_url.find("[") >= 0: # if url has [ after page number localhost:3333/123[33]  we want to change increment for next 
                    __class__.idx1 = str_url.index("[")
                    __class__.idx2 = str_url.index("]")
                    #__class__.num = int(str_url[0:__class__.idx1],10)
                    __class__.num = 1
                    __class__.stride = int(str_url[__class__.idx1+1:__class__.idx2],10)
                    __class__.previous = __class__.num - 1
                    if __class__.previous == 0:
                        __class__.previous = 1
                    __class__.next = __class__.num + __class__.stride                
                    if __class__.next > __class__.max:
                        __class__.next = __class__.max
                    __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                elif str_url.find("(") >= 0: # if url has ( after page number localhost:3333/123(100-333) we want to change random range for pages starting with 100 up to 333              
                    __class__.idx1 = str_url.index("(")
                    __class__.idx2 = str_url.index("-")
                    __class__.idx3 = str_url.index(")")
                    __class__.randomMin = int(str_url[__class__.idx1+1:__class__.idx2],10)
                    __class__.randomMax = int(str_url[__class__.idx2+1:__class__.idx3],10)
                    __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                    #__class__.num = int(str_url[0:__class__.idx1],10)
                    __class__.num = 1
                    __class__.previous = __class__.num - 1
                    if __class__.previous == 0:
                        __class__.previous = 1
                    __class__.next = __class__.num + __class__.stride                
                    if __class__.next > __class__.max:
                        __class__.next = __class__.max
                elif str_url.find("$") >= 0:  #if url starts with $ localhost:3333/$f78feb18a  we want to search page by hex value of privatekey              
                    __class__.idx1 = str_url.index("$")
                    if __class__.isHex(str_url[__class__.idx1+1:]) and len(str_url[__class__.idx1+1:]) > 0:                    
                        __class__.num = int(str_url[__class__.idx1+1:],16)
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        __class__.searchKey_U = ice.privatekey_to_address(0, False, __class__.num)
                        __class__.num = __class__.num // 128
                        __class__.num = __class__.num + 1                
                        __class__.previous = __class__.num - 1
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                    else:
                        __class__.num = 1
                        __class__.previous = __class__.num - 1;
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                elif str_url.find("@") >= 0: #if url starts with @ localhost:3333/@186732 we want to search page by decimal value of privatekey               
                    __class__.idx1 = str_url.index("@")
                    if str_url[__class__.idx1+1:].isnumeric():                    
                        __class__.num = int(str_url[__class__.idx1+1:],10)
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        __class__.searchKey_U = ice.privatekey_to_address(0, False, __class__.num)
                        __class__.num = __class__.num // 128
                        __class__.num = __class__.num + 1                
                        __class__.previous = __class__.num - 1
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                    else:
                        __class__.num = 1
                        __class__.previous = __class__.num - 1;
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                else:
                    if str_url == 'favicon.ico': #favicon.ico request gag
                        pass
                    else:
                        if str_url.isnumeric(): #if url contains just page number in decimal localhost:3333/123456 that is correct
                            __class__.num = int(str_url,10)
                            if __class__.num > __class__.max: #if requested page number more than max(last) we set it to max(last)
                                __class__.num = __class__.max
                            __class__.previous = __class__.num - 1;
                            if __class__.previous == 0:
                                 __class__.previous = 1
                            __class__.next = __class__.num + __class__.stride                
                            if __class__.next > __class__.max:
                                 __class__.next = __class__.max
                            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        else: # if page number has not just decimal numbers we set it to first 
                            __class__.num = 1
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
            self.wfile.write(bytes("<h3><span style='color:#D7DBDD;background-color:#145A32;padding:2px;border-radius: 2px;'>Page #</span> <span id='current_page' style='color: #145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>" + str(__class__.num) + "</span> <span style='color:#145A32;'><< out of >></span> <span style='color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h3>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Current page increment for next = <span id='cur_inc'>" + str(__class__.stride) + "</span></p>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Current random range = <span id='rand_min'>" + str(__class__.randomMin) + "</span> - <span id='rand_max'>" + str(__class__.randomMax) + "</span></p>", "utf-8"))
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.first)+"'>first</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.middle)+"'>middle</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.max)+"'>last</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.hj)+"'>5H(end)-5J(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.jk)+"'>5J(end)-5K(start)</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.random5H)+"'>5H_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random5J)+"'>5J_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random5K)+"'>5K_random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.Kx)+"'>Kw(end)_Kx(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.Ky)+"'>Kx(end)_Ky(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.Kz)+"'>Ky(end)_Kz(start)</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.L1)+"'>Kz(end)-L1(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.L2)+"'>L1(end)_L2(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.L3)+"'>L2(end)_L3(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.L4)+"'>L3(end)_L4(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.L5)+"'>L4(end)_L5(start)</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span class='ajax' style='color:blue;' page='/"+str(__class__.randomKw)+"'>Kw_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomKx)+"'>Kx_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomKy)+"'>Ky_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomKz)+"'>Kz_random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL1)+"'>L1_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL2)+"'>L2_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL3)+"'>L3_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL4)+"'>L4_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL5)+"'>L5_random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p255)+"'>2^255</a>|<a href='/"+str(__class__.p254)+"'>2^254</a>|<a href='/"+str(__class__.p253)+"'>2^253</a>|<a href='/"+str(__class__.p252)+"'>2^252</a>|<a href='/"+str(__class__.p251)+"'>2^251</a>|<a href='/"+str(__class__.p250)+"'>2^250</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p249)+"'>2^249</a>|<a href='/"+str(__class__.p248)+"'>2^248</a>|<a href='/"+str(__class__.p247)+"'>2^247</a>|<a href='/"+str(__class__.p246)+"'>2^246</a>|<a href='/"+str(__class__.p245)+"'>2^245</a>|<a href='/"+str(__class__.p244)+"'>2^244</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p243)+"'>2^243</a>|<a href='/"+str(__class__.p242)+"'>2^242</a>|<a href='/"+str(__class__.p241)+"'>2^241</a>|<a href='/"+str(__class__.p240)+"'>2^240</a>|<a href='/"+str(__class__.p239)+"'>2^239</a>|<a href='/"+str(__class__.p238)+"'>2^238</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p237)+"'>2^237</a>|<a href='/"+str(__class__.p236)+"'>2^236</a>|<a href='/"+str(__class__.p235)+"'>2^235</a>|<a href='/"+str(__class__.p234)+"'>2^234</a>|<a href='/"+str(__class__.p233)+"'>2^233</a>|<a href='/"+str(__class__.p232)+"'>2^232</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p231)+"'>2^231</a>|<a href='/"+str(__class__.p230)+"'>2^230</a>|<a href='/"+str(__class__.p229)+"'>2^229</a>|<a href='/"+str(__class__.p228)+"'>2^228</a>|<a href='/"+str(__class__.p227)+"'>2^227</a>|<a href='/"+str(__class__.p226)+"'>2^226</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p225)+"'>2^225</a>|<a href='/"+str(__class__.p224)+"'>2^224</a>|<a href='/"+str(__class__.p223)+"'>2^223</a>|<a href='/"+str(__class__.p222)+"'>2^222</a>|<a href='/"+str(__class__.p221)+"'>2^221</a>|<a href='/"+str(__class__.p220)+"'>2^220</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p219)+"'>2^219</a>|<a href='/"+str(__class__.p218)+"'>2^218</a>|<a href='/"+str(__class__.p217)+"'>2^217</a>|<a href='/"+str(__class__.p216)+"'>2^216</a>|<a href='/"+str(__class__.p215)+"'>2^215</a>|<a href='/"+str(__class__.p214)+"'>2^214</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p213)+"'>2^213</a>|<a href='/"+str(__class__.p212)+"'>2^212</a>|<a href='/"+str(__class__.p211)+"'>2^211</a>|<a href='/"+str(__class__.p210)+"'>2^210</a>|<a href='/"+str(__class__.p209)+"'>2^209</a>|<a href='/"+str(__class__.p208)+"'>2^208</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p207)+"'>2^207</a>|<a href='/"+str(__class__.p206)+"'>2^206</a>|<a href='/"+str(__class__.p205)+"'>2^205</a>|<a href='/"+str(__class__.p204)+"'>2^204</a>|<a href='/"+str(__class__.p203)+"'>2^203</a>|<a href='/"+str(__class__.p202)+"'>2^202</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p201)+"'>2^201</a>|<a href='/"+str(__class__.p200)+"'>2^200</a>|<a href='/"+str(__class__.p199)+"'>2^199</a>|<a href='/"+str(__class__.p198)+"'>2^198</a>|<a href='/"+str(__class__.p197)+"'>2^197</a>|<a href='/"+str(__class__.p196)+"'>2^196</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p195)+"'>2^195</a>|<a href='/"+str(__class__.p194)+"'>2^194</a>|<a href='/"+str(__class__.p193)+"'>2^193</a>|<a href='/"+str(__class__.p192)+"'>2^192</a>|<a href='/"+str(__class__.p191)+"'>2^191</a>|<a href='/"+str(__class__.p190)+"'>2^190</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p189)+"'>2^189</a>|<a href='/"+str(__class__.p188)+"'>2^188</a>|<a href='/"+str(__class__.p187)+"'>2^187</a>|<a href='/"+str(__class__.p186)+"'>2^186</a>|<a href='/"+str(__class__.p185)+"'>2^185</a>|<a href='/"+str(__class__.p184)+"'>2^184</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p183)+"'>2^183</a>|<a href='/"+str(__class__.p182)+"'>2^182</a>|<a href='/"+str(__class__.p181)+"'>2^181</a>|<a href='/"+str(__class__.p180)+"'>2^180</a>|<a href='/"+str(__class__.p179)+"'>2^179</a>|<a href='/"+str(__class__.p178)+"'>2^178</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p177)+"'>2^177</a>|<a href='/"+str(__class__.p176)+"'>2^176</a>|<a href='/"+str(__class__.p175)+"'>2^175</a>|<a href='/"+str(__class__.p174)+"'>2^174</a>|<a href='/"+str(__class__.p173)+"'>2^173</a>|<a href='/"+str(__class__.p172)+"'>2^172</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p171)+"'>2^171</a>|<a href='/"+str(__class__.p170)+"'>2^170</a>|<a href='/"+str(__class__.p169)+"'>2^169</a>|<a href='/"+str(__class__.p168)+"'>2^168</a>|<a href='/"+str(__class__.p167)+"'>2^167</a>|<a href='/"+str(__class__.p166)+"'>2^166</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p165)+"'>2^165</a>|<a href='/"+str(__class__.p164)+"'>2^164</a>|<a href='/"+str(__class__.p163)+"'>2^163</a>|<a href='/"+str(__class__.p162)+"'>2^162</a>|<a href='/"+str(__class__.p161)+"'>2^161</a>|<a href='/"+str(__class__.p160)+"'>2^160</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p159)+"'>2^159</a>|<a href='/"+str(__class__.p158)+"'>2^158</a>|<a href='/"+str(__class__.p157)+"'>2^157</a>|<a href='/"+str(__class__.p156)+"'>2^156</a>|<a href='/"+str(__class__.p155)+"'>2^155</a>|<a href='/"+str(__class__.p154)+"'>2^154</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p153)+"'>2^153</a>|<a href='/"+str(__class__.p152)+"'>2^152</a>|<a href='/"+str(__class__.p151)+"'>2^151</a>|<a href='/"+str(__class__.p150)+"'>2^150</a>|<a href='/"+str(__class__.p149)+"'>2^149</a>|<a href='/"+str(__class__.p148)+"'>2^148</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p147)+"'>2^147</a>|<a href='/"+str(__class__.p146)+"'>2^146</a>|<a href='/"+str(__class__.p145)+"'>2^145</a>|<a href='/"+str(__class__.p144)+"'>2^144</a>|<a href='/"+str(__class__.p143)+"'>2^143</a>|<a href='/"+str(__class__.p142)+"'>2^142</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p141)+"'>2^141</a>|<a href='/"+str(__class__.p140)+"'>2^140</a>|<a href='/"+str(__class__.p139)+"'>2^139</a>|<a href='/"+str(__class__.p138)+"'>2^138</a>|<a href='/"+str(__class__.p137)+"'>2^137</a>|<a href='/"+str(__class__.p136)+"'>2^136</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p135)+"'>2^135</a>|<a href='/"+str(__class__.p134)+"'>2^134</a>|<a href='/"+str(__class__.p133)+"'>2^133</a>|<a href='/"+str(__class__.p132)+"'>2^132</a>|<a href='/"+str(__class__.p131)+"'>2^131</a>|<a href='/"+str(__class__.p130)+"'>2^130</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p129)+"'>2^129</a>|<a href='/"+str(__class__.p128)+"'>2^128</a>|<a href='/"+str(__class__.p127)+"'>2^127</a>|<a href='/"+str(__class__.p126)+"'>2^126</a>|<a href='/"+str(__class__.p125)+"'>2^125</a>|<a href='/"+str(__class__.p124)+"'>2^124</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p123)+"'>2^123</a>|<a href='/"+str(__class__.p122)+"'>2^122</a>|<a href='/"+str(__class__.p121)+"'>2^121</a>|<a href='/"+str(__class__.p120)+"'>2^120</a>|<a href='/"+str(__class__.p119)+"'>2^119</a>|<a href='/"+str(__class__.p118)+"'>2^118</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p117)+"'>2^117</a>|<a href='/"+str(__class__.p116)+"'>2^116</a>|<a href='/"+str(__class__.p115)+"'>2^115</a>|<a href='/"+str(__class__.p114)+"'>2^114</a>|<a href='/"+str(__class__.p113)+"'>2^113</a>|<a href='/"+str(__class__.p112)+"'>2^112</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p111)+"'>2^111</a>|<a href='/"+str(__class__.p110)+"'>2^110</a>|<a href='/"+str(__class__.p109)+"'>2^109</a>|<a href='/"+str(__class__.p108)+"'>2^108</a>|<a href='/"+str(__class__.p107)+"'>2^107</a>|<a href='/"+str(__class__.p106)+"'>2^106</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p105)+"'>2^105</a>|<a href='/"+str(__class__.p104)+"'>2^104</a>|<a href='/"+str(__class__.p103)+"'>2^103</a>|<a href='/"+str(__class__.p102)+"'>2^102</a>|<a href='/"+str(__class__.p101)+"'>2^101</a>|<a href='/"+str(__class__.p100)+"'>2^100</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p99)+"'>2^99</a>|<a href='/"+str(__class__.p98)+"'>2^98</a>|<a href='/"+str(__class__.p97)+"'>2^97</a>|<a href='/"+str(__class__.p96)+"'>2^96</a>|<a href='/"+str(__class__.p95)+"'>2^95</a>|<a href='/"+str(__class__.p94)+"'>2^94</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p93)+"'>2^93</a>|<a href='/"+str(__class__.p92)+"'>2^92</a>|<a href='/"+str(__class__.p91)+"'>2^91</a>|<a href='/"+str(__class__.p90)+"'>2^90</a>|<a href='/"+str(__class__.p89)+"'>2^89</a>|<a href='/"+str(__class__.p88)+"'>2^88</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p87)+"'>2^87</a>|<a href='/"+str(__class__.p86)+"'>2^86</a>|<a href='/"+str(__class__.p85)+"'>2^85</a>|<a href='/"+str(__class__.p84)+"'>2^84</a>|<a href='/"+str(__class__.p83)+"'>2^83</a>|<a href='/"+str(__class__.p82)+"'>2^82</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p81)+"'>2^81</a>|<a href='/"+str(__class__.p82)+"'>2^82</a>|<a href='/"+str(__class__.p81)+"'>2^81</a>|<a href='/"+str(__class__.p80)+"'>2^80</a>|<a href='/"+str(__class__.p79)+"'>2^79</a>|<a href='/"+str(__class__.p78)+"'>2^78</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p77)+"'>2^77</a>|<a href='/"+str(__class__.p76)+"'>2^76</a>|<a href='/"+str(__class__.p75)+"'>2^75</a>|<a href='/"+str(__class__.p74)+"'>2^74</a>|<a href='/"+str(__class__.p73)+"'>2^73</a>|<br>|<a href='/"+str(__class__.p72)+"'>2^72</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p71)+"'>2^71</a>|<a href='/"+str(__class__.p70)+"'>2^70</a>|<a href='/"+str(__class__.p69)+"'>2^69</a>|<a href='/"+str(__class__.p68)+"'>2^68</a>|<a href='/"+str(__class__.p67)+"'>2^67</a>|<a href='/"+str(__class__.p66)+"'>2^66</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p65)+"'>2^65</a>|<a href='/"+str(__class__.p64)+"'>2^64</a>|<a href='/"+str(__class__.p63)+"'>2^63</a>|<a href='/"+str(__class__.p62)+"'>2^62</a>|<a href='/"+str(__class__.p61)+"'>2^61</a>|<a href='/"+str(__class__.p60)+"'>2^60</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p59)+"'>2^59</a>|<a href='/"+str(__class__.p58)+"'>2^58</a>|<a href='/"+str(__class__.p57)+"'>2^57</a>|<a href='/"+str(__class__.p56)+"'>2^56</a>|<a href='/"+str(__class__.p55)+"'>2^55</a>|<a href='/"+str(__class__.p54)+"'>2^54</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p53)+"'>2^53</a>|<a href='/"+str(__class__.p52)+"'>2^52</a>|<a href='/"+str(__class__.p51)+"'>2^51</a>|<a href='/"+str(__class__.p50)+"'>2^50</a>|<a href='/"+str(__class__.p49)+"'>2^49</a>|<a href='/"+str(__class__.p48)+"'>2^48</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p47)+"'>2^47</a>|<a href='/"+str(__class__.p46)+"'>2^46</a>|<a href='/"+str(__class__.p45)+"'>2^45</a>|<a href='/"+str(__class__.p44)+"'>2^44</a>|<a href='/"+str(__class__.p43)+"'>2^43</a>|<a href='/"+str(__class__.p42)+"'>2^42</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p41)+"'>2^41</a>|<a href='/"+str(__class__.p40)+"'>2^40</a>|<a href='/"+str(__class__.p39)+"'>2^39</a>|<a href='/"+str(__class__.p38)+"'>2^38</a>|<a href='/"+str(__class__.p37)+"'>2^37</a>|<a href='/"+str(__class__.p36)+"'>2^36</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p35)+"'>2^35</a>|<a href='/"+str(__class__.p34)+"'>2^34</a>|<a href='/"+str(__class__.p33)+"'>2^33</a>|<a href='/"+str(__class__.p32)+"'>2^32</a>|<a href='/"+str(__class__.p31)+"'>2^31</a>|<a href='/"+str(__class__.p30)+"'>2^30</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p29)+"'>2^29</a>|<a href='/"+str(__class__.p28)+"'>2^28</a>|<a href='/"+str(__class__.p27)+"'>2^27</a>|<a href='/"+str(__class__.p26)+"'>2^26</a>|<a href='/"+str(__class__.p25)+"'>2^25</a>|<a href='/"+str(__class__.p24)+"'>2^24</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p23)+"'>2^23</a>|<a href='/"+str(__class__.p22)+"'>2^22</a>|<a href='/"+str(__class__.p21)+"'>2^21</a>|<a href='/"+str(__class__.p20)+"'>2^20</a>|<a href='/"+str(__class__.p19)+"'>2^19</a>|<a href='/"+str(__class__.p18)+"'>2^18</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p17)+"'>2^17</a>|<a href='/"+str(__class__.p16)+"'>2^16</a>|<a href='/"+str(__class__.p15)+"'>2^15</a>|<a href='/"+str(__class__.p14)+"'>2^14</a>|<a href='/"+str(__class__.p13)+"'>2^13</a>|<a href='/"+str(__class__.p12)+"'>2^12</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p11)+"'>2^11</a>|<a href='/"+str(__class__.p10)+"'>2^10</a>|<a href='/"+str(__class__.p9)+"'>2^9</a>|<a href='/"+str(__class__.p8)+"'>2^8</a>|<a href='/"+str(__class__.p7)+"'>2^7</a>|<a href='/"+str(__class__.p6)+"'>2^6</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p5)+"'>2^5</a>|<a href='/"+str(__class__.p4)+"'>2^4</a>|<a href='/"+str(__class__.p3)+"'>2^3</a>|<a href='/"+str(__class__.p2)+"'>2^2</a>|<a href='/"+str(__class__.p1)+"'>2^1</a>|", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            #generating hex values for starting and ending key
            __class__.starting_key_hex = hex(__class__.startPrivKey)[2:].zfill(64)
            if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494273:
                __class__.ending_key_hex = hex(__class__.startPrivKey+63)[2:].zfill(64)
            else:
                __class__.ending_key_hex = hex(__class__.startPrivKey+127)[2:].zfill(64)
            #----------------------------------------------------------------------------------
            self.wfile.write(bytes("<p style='color:gray;font-weight:bold;'>*Starting Private Key Hex: " + str(__class__.starting_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p style='color:gray;font-weight:bold;'>**Ending Private Key Hex: " + str(__class__.ending_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p id='balance' style='color:brown;font-weight:bold;'>Balance on this Page: False</p>", "utf-8"))
            if sys.platform == 'linux' or sys.platform == 'darwin':
                self.wfile.write(bytes("<pre class='keys'><strong>Private Key Hex</strong>                                                          <strong>Uncompressed Address</strong>                <strong>Compressed Address</strong>                       <strong>SegWit 3 Address</strong>                  <strong>bech32 bc1 Address</strong>                           <strong>ETH Address</strong>                           <strong>WIF Private Key Uncompressed</strong>                            <strong>WIF Private Key Compressed</strong><br>", "utf-8"))
            if sys.platform == 'win32':
                self.wfile.write(bytes("<pre class='keys'><strong>Private Key Hex</strong>                                                          <strong>Uncompressed Address</strong>                <strong>Compressed Address</strong>                       <strong>SegWit 3 Address</strong>                  <strong>bech32 bc1 Address</strong>                           <strong>ETH Address</strong>                           <strong>WIF Private Key Uncompressed</strong>                            <strong>WIF Private Key Compressed</strong><br>", "utf-8"))
            ###---Loop---******************************************************************
            for i in range(0,128): #generating addresses and WIFS to show on page
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
                if __class__.bitAddr == __class__.searchKey or __class__.bitAddr_C == __class__.searchKey or __class__.bitAddr_S == __class__.searchKey or __class__.bitAddr_bech32 == __class__.searchKey or __class__.bitAddr_eth == __class__.searchKey:
                    self.wfile.write(bytes("<lol style='color:#DE3163;'>" +"<lol class='show_popup' rel='popup1' style='color:#DE3163;font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr + "'>" +"<strong>"+ __class__.bitAddr+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C+"'>"+"<strong>"+ __class__.bitAddr_C +"</strong>"+ "</a></lol>&nbsp;&nbsp;<lol>" +"&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr_S + "'>" +"<strong>"+ __class__.bitAddr_S+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32+"'>"+"<strong>"+ __class__.bitAddr_bech32 + "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://ethplorer.io/address/" + __class__.bitAddr_eth+"'>"+"<strong>"+ __class__.bitAddr_eth +"</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='color:#DE3163;'>" +"&nbsp;&nbsp;<lol>"+"<strong>"+ __class__.privKey+ "</strong>"+"</lol><lol style='color:#DE3163;'>" +"&nbsp;&nbsp;<lol>"+"<strong>"+ __class__.privKey_C+ "</strong>"+"</lol></br>", "utf-8"))
                    __class__.searchKey = ""
                elif __class__.bitAddr == __class__.searchKey_U:
                    self.wfile.write(bytes("<lol style='color:#DE3163;'>" +"<lol class='show_popup' rel='popup1' style='color:#red;font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr + "'>" +"<strong>"+ __class__.bitAddr+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C+"'>"+"<strong>"+ __class__.bitAddr_C +"</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol>" +"&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr_S + "'>" +"<strong>"+ __class__.bitAddr_S+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32+"'>"+"<strong>"+ __class__.bitAddr_bech32 +"</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol>" +"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://ethplorer.io/address/"+ __class__.bitAddr_eth + "'>" +"<strong>"+ __class__.bitAddr_eth+ "</strong>"+ "</a></lol><lol>" + "&nbsp;&nbsp<span>&nbsp;&nbsp;&nbsp;&nbsp;"  + "</span>&nbsp;&nbsp</lol>&nbsp;&nbsp;<lol style='color:#DE3163;'>" +"<strong>"+ __class__.privKey +"</strong>"+ "</lol>&nbsp;&nbsp;<lol style='color:#DE3163;'>"+"<strong>"+__class__.privKey_C+"</strong>"+"</lol></br>", "utf-8"))
                    __class__.searchKey_U = ""
                else:
                    self.wfile.write(bytes("<lol style='color:#DE3163;'>" +"<lol class='show_popup' rel='popup1' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a>" + "&nbsp<span>"  + "</span>&nbsp" + "</lol>&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_S + "'>" + __class__.bitAddr_S + "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32 + "'>" + __class__.bitAddr_bech32 + "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://ethplorer.io/address/" + __class__.bitAddr_eth + "'>" + __class__.bitAddr_eth + "</a></lol>&nbsp;&nbsp;<lol style='color:#145A32;'>" + "&nbsp;&nbsp;<lol>" + "&nbsp;&nbsp<span>"  + "</span>&nbsp;&nbsp</lol>&nbsp;&nbsp;" + __class__.privKey + "</lol><lol style='color:#145A32;'>" +"&nbsp;&nbsp;<lol>"+__class__.privKey_C+"</lol></br>", "utf-8"))
                if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                __class__.startPrivKey += 1
            ###---Loop---checking if generated addresses are in arr set(if yes then we found address with balance)
            for addr in __class__.addresses:
                if addr in __class__.bloom_filter or addr in __class__.bloom_filter1:
                    __class__.balance_on_page = "True"
                    __class__.foundling = addr + " "
                    with open("found.txt", "a", encoding="utf-8") as f: #saving if found: address page#
                        f.write(f"Bitcoin or ETH Address: {addr} Found on Page# {__class__.num} \n")
            #-------------------------------------------------------------------------------
            self.wfile.write(bytes("</pre><pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "</p>", "utf-8"))
            self.wfile.write(bytes("<script>var elem = document.getElementById('balance');elem.innerHTML = 'Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "'</script>", "utf-8"))
            self.wfile.write(bytes("""
<script>                       
$('.show_popup').click(function() {
    var path = window.location.pathname;
    if(path == '/904625697166532776746648320380374280100293470930272690489102837043110636675') { $('#all_num').html(64); }           
    var val = $(this).attr('value');
    var num = $(this).attr('num');
    $('#arrow_num').html(num);
    var decNum = BigInt("0x"+val);
    $('#arrow_num').attr('dec', decNum);
    $.get("http://localhost:3333/!"+decNum, function(data, status){
        const myArray = data.split(" ");
        $('#fun2x').html('x: '+myArray[0]);
        $('#fun2y').html('y: '+myArray[1]);
        $('#fun3x').html('x: '+myArray[2]);
        $('#fun3y').html('y: '+myArray[3]);
        $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
        if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
        else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
        $('#fun5').html('x: ' +myArray[7]);
        $('#addinvx').html('x: ' +myArray[8]);
        $('#addinvy').html('y: ' +myArray[9]);
        $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
        $('#addinvn').html(myArray[12]);
        $('#same1x').html('x: ' +myArray[14]);
        $('#same1y').html('y: ' +myArray[1]);
        $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
        $('#same2x').html('x: ' +myArray[18]);
        $('#same2y').html('y: ' +myArray[1]);
        $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
        $('#fun').html(myArray[22]);
        $('#funhex').html(myArray[23]);
    })           
    var popup_id = $('#' + $(this).attr('rel'));
    $(popup_id).show();
    $('.overlay_popup').show();
    $(this).attr('style',  'color:#DE3163;font-weight:bold;');                
})
$('.overlay_popup').click(function() {
    $('.overlay_popup, .popup').hide();
})
$('.ajax').click(function() { 
    var pnum = $(this).attr('page');
    pnum = pnum.substring(1);
    $.get("http://localhost:3333/A"+pnum, function(data, status){
        $('#main_content').html(data)
        history.pushState({}, null, "http://localhost:3333/"+pnum); 
    })
})
$('#arrow_left').click(function() {
    var item_num = parseInt($('#arrow_num').html());
    if(item_num > 1) { 
        $('#arrow_num').html(item_num - 1);
        var decNum = $('#arrow_num').attr('dec');
        var bigNum = BigInt(decNum);
        $.get("http://localhost:3333/!"+(--bigNum), function(data, status){
            const myArray = data.split(" ");
            $('#fun2x').html('x: '+myArray[0]);
            $('#fun2y').html('y: '+myArray[1]);
            $('#fun3x').html('x: '+myArray[2]);
            $('#fun3y').html('y: '+myArray[3]);
            $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
            if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
            else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
            $('#fun5').html('x: ' +myArray[7]);
            $('#addinvx').html('x: ' +myArray[8]);
            $('#addinvy').html('y: ' +myArray[9]);
            $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
            $('#addinvn').html(myArray[12]);
            $('#same1x').html('x: ' +myArray[14]);
            $('#same1y').html('y: ' +myArray[1]);
            $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
            $('#same2x').html('x: ' +myArray[18]);
            $('#same2y').html('y: ' +myArray[1]);
            $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
            $('#fun').html(myArray[22]);
            $('#funhex').html(myArray[23]);
        })
        $('#arrow_num').attr('dec', bigNum);
        var set_style = parseInt($('#arrow_num').html());
        $('*[num="'+(set_style)+'"]').attr('style',  'color:#DE3163;font-weight:bold;');
        $('html, body').animate({scrollTop: $('*[num="'+(set_style)+'"]').offset().top}, 200); 
    }
    else {
        $('#arrow_num').html(item_num); 
    }
})
$('#arrow_right').click(function() {
    var last = 128;
    var path = window.location.pathname;
    if(path == '/904625697166532776746648320380374280100293470930272690489102837043110636675') { last = 64; $('#all_num').html(64); }
    var item_num = parseInt($('#arrow_num').html());
    if(item_num != last) { 
        $('#arrow_num').html(item_num + 1);
        var decNum = $('#arrow_num').attr('dec');
        var bigNum = BigInt(decNum);
        $.get("http://localhost:3333/!"+(++bigNum), function(data, status){
            const myArray = data.split(" ");
            $('#fun2x').html('x: '+myArray[0]);
            $('#fun2y').html('y: '+myArray[1]);
            $('#fun3x').html('x: '+myArray[2]);
            $('#fun3y').html('y: '+myArray[3]);
            $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
            if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
            else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
            $('#fun5').html('x: ' +myArray[7]);
            $('#addinvx').html('x: ' +myArray[8]);
            $('#addinvy').html('y: ' +myArray[9]);
            $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
            $('#addinvn').html(myArray[12]);
            $('#same1x').html('x: ' +myArray[14]);
            $('#same1y').html('y: ' +myArray[1]);
            $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
            $('#same2x').html('x: ' +myArray[18]);
            $('#same2y').html('y: ' +myArray[1]);
            $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
            $('#fun').html(myArray[22]);
            $('#funhex').html(myArray[23]);
        })
        $('#arrow_num').attr('dec', bigNum);
        var set_style = parseInt($('#arrow_num').html());
        $('*[num="'+(set_style)+'"]').attr('style',  'color:#DE3163;font-weight:bold;');
        $('html, body').animate({scrollTop: $('*[num="'+(set_style)+'"]').offset().top}, 200);
    }
    else { 
        $('#arrow_num').html(last); 
    }
})
</script>""", "utf-8")) 
            __class__.addresses.clear() #clearing generated addresses list so we can use it fresh with next page request
            #dropping values to defaults
            __class__.balance_on_page = "False"
            __class__.foundling = ""
#-------#--------Search Field End-----------------------------------------------------------
        elif str_url.startswith("A"): #AJAX Full Page Refresh
            self.wfile.write(bytes("""
<div class='overlay_popup'></div>
<div class='popup' id='popup1'>
<div class='object'>
<h4 style='color:brown;font-weight:bold;text-align:right;'>Private ECDSA Key&nbsp;&nbsp;
<button class='arrow' id='arrow_left' style='color:blue;margin-left:132px;'><<<</button>&nbsp;&nbsp;
<span style='color:brown;' id='arrow_num'>1</span> <span style='color:brown;'>of</span> <span  id='all_num' style='color:brown;'>128</span>&nbsp;&nbsp;
<button class='arrow' id='arrow_right' style='color:blue;'>>>></button>&nbsp;&nbsp;</h4>
<p id='funbin' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;word-wrap: break-word;'></p>
<p id='funhex' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<h4 style='color:brown;font-weight:bold;'>Public ECDSA Key</h4>
<p id='fun2x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun2y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun3x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun3y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun5' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>           
<h4 style='color:brown;font-weight:bold;'>Additive Inverse Point</h4>
<p id='addinvn' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addinvx' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addinvy' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addrinv' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<h4 style='color:brown;font-weight:bold;'>Two More Points same Y different X</h4>
<p id='same1x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same1y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same1addr' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2addr' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<h4 style='color:brown;font-weight:bold;'>RIPEMD-160 Hash</h4>
<p id='fun4' style='color:#34495E ;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>"
</div></div>""", "utf-8"))
            #self.wfile.write(bytes("<p style='color:#34495E;font-weight:bold;'>123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz - Base58</p>", "utf-8"))
            #self.wfile.write(bytes("<h2><span style='color:#34495E;'>Bitcoin and ETH Addresses Database. Total Addresses Loaded&nbsp;***|&nbsp;" + str(__class__.addr_count) + "&nbsp;|</span></h2>", "utf-8")) 
            ###--------setting values for num(page number) previous and next page------------       
            str_url = self.path[2:]
            __class__.num = int(str_url,10)
            __class__.previous = __class__.num - 1;
            if __class__.previous == 0:
                __class__.previous = 1
            __class__.next = __class__.num + __class__.stride                
            if __class__.next > __class__.max:
                __class__.next = __class__.max
            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)                
            ###---------setting startPrivKey(start to generate addresses from)----------------
            __class__.startPrivKey = (__class__.num - 1) * 128+1
            #setting random pages
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
            self.wfile.write(bytes("<h3><span style='color:#D7DBDD;background-color:#145A32;padding:2px;border-radius: 2px;'>Page #</span> <span id='current_page' style='color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>" + str(__class__.num) + "</span> <span style='color:#145A32;'><< out of >></span> <span style='color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h3>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Current page increment for next = <span id='cur_inc'>" + str(__class__.stride) + "</span></p>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Current random range = <span id='rand_min'>" + str(__class__.randomMin) + "</span> - <span id='rand_max'>" + str(__class__.randomMax) + "</span></p>", "utf-8"))
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.first)+"'>first</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.middle)+"'>middle</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.max)+"'>last</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax'  page='/"+str(__class__.hj)+"'>5H(end)-5J(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.jk)+"'>5J(end)-5K(start)</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax'  page='/"+str(__class__.random5H)+"'>5H_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.random5J)+"'>5J_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.random5K)+"'>5K_random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax'  page='/"+str(__class__.Kx)+"'>Kw(end)_Kx(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.Ky)+"'>Kx(end)_Ky(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.Kz)+"'>Ky(end)_Kz(start)</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax'  page='/"+str(__class__.L1)+"'>Kz(end)-L1(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.L2)+"'>L1(end)_L2(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.L3)+"'>L2(end)_L3(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.L4)+"'>L3(end)_L4(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.L5)+"'>L4(end)_L5(start)</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomKw)+"'>Kw_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomKx)+"'>Kx_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomKy)+"'>Ky_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomKz)+"'>Kz_random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomL1)+"'>L1_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomL2)+"'>L2_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomL3)+"'>L3_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomL4)+"'>L4_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax'  page='/"+str(__class__.randomL5)+"'>L5_random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p255)+"'>2^255</a>|<a href='/"+str(__class__.p254)+"'>2^254</a>|<a href='/"+str(__class__.p253)+"'>2^253</a>|<a href='/"+str(__class__.p252)+"'>2^252</a>|<a href='/"+str(__class__.p251)+"'>2^251</a>|<a href='/"+str(__class__.p250)+"'>2^250</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p249)+"'>2^249</a>|<a href='/"+str(__class__.p248)+"'>2^248</a>|<a href='/"+str(__class__.p247)+"'>2^247</a>|<a href='/"+str(__class__.p246)+"'>2^246</a>|<a href='/"+str(__class__.p245)+"'>2^245</a>|<a href='/"+str(__class__.p244)+"'>2^244</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p243)+"'>2^243</a>|<a href='/"+str(__class__.p242)+"'>2^242</a>|<a href='/"+str(__class__.p241)+"'>2^241</a>|<a href='/"+str(__class__.p240)+"'>2^240</a>|<a href='/"+str(__class__.p239)+"'>2^239</a>|<a href='/"+str(__class__.p238)+"'>2^238</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p237)+"'>2^237</a>|<a href='/"+str(__class__.p236)+"'>2^236</a>|<a href='/"+str(__class__.p235)+"'>2^235</a>|<a href='/"+str(__class__.p234)+"'>2^234</a>|<a href='/"+str(__class__.p233)+"'>2^233</a>|<a href='/"+str(__class__.p232)+"'>2^232</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p231)+"'>2^231</a>|<a href='/"+str(__class__.p230)+"'>2^230</a>|<a href='/"+str(__class__.p229)+"'>2^229</a>|<a href='/"+str(__class__.p228)+"'>2^228</a>|<a href='/"+str(__class__.p227)+"'>2^227</a>|<a href='/"+str(__class__.p226)+"'>2^226</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p225)+"'>2^225</a>|<a href='/"+str(__class__.p224)+"'>2^224</a>|<a href='/"+str(__class__.p223)+"'>2^223</a>|<a href='/"+str(__class__.p222)+"'>2^222</a>|<a href='/"+str(__class__.p221)+"'>2^221</a>|<a href='/"+str(__class__.p220)+"'>2^220</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p219)+"'>2^219</a>|<a href='/"+str(__class__.p218)+"'>2^218</a>|<a href='/"+str(__class__.p217)+"'>2^217</a>|<a href='/"+str(__class__.p216)+"'>2^216</a>|<a href='/"+str(__class__.p215)+"'>2^215</a>|<a href='/"+str(__class__.p214)+"'>2^214</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p213)+"'>2^213</a>|<a href='/"+str(__class__.p212)+"'>2^212</a>|<a href='/"+str(__class__.p211)+"'>2^211</a>|<a href='/"+str(__class__.p210)+"'>2^210</a>|<a href='/"+str(__class__.p209)+"'>2^209</a>|<a href='/"+str(__class__.p208)+"'>2^208</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p207)+"'>2^207</a>|<a href='/"+str(__class__.p206)+"'>2^206</a>|<a href='/"+str(__class__.p205)+"'>2^205</a>|<a href='/"+str(__class__.p204)+"'>2^204</a>|<a href='/"+str(__class__.p203)+"'>2^203</a>|<a href='/"+str(__class__.p202)+"'>2^202</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p201)+"'>2^201</a>|<a href='/"+str(__class__.p200)+"'>2^200</a>|<a href='/"+str(__class__.p199)+"'>2^199</a>|<a href='/"+str(__class__.p198)+"'>2^198</a>|<a href='/"+str(__class__.p197)+"'>2^197</a>|<a href='/"+str(__class__.p196)+"'>2^196</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p195)+"'>2^195</a>|<a href='/"+str(__class__.p194)+"'>2^194</a>|<a href='/"+str(__class__.p193)+"'>2^193</a>|<a href='/"+str(__class__.p192)+"'>2^192</a>|<a href='/"+str(__class__.p191)+"'>2^191</a>|<a href='/"+str(__class__.p190)+"'>2^190</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p189)+"'>2^189</a>|<a href='/"+str(__class__.p188)+"'>2^188</a>|<a href='/"+str(__class__.p187)+"'>2^187</a>|<a href='/"+str(__class__.p186)+"'>2^186</a>|<a href='/"+str(__class__.p185)+"'>2^185</a>|<a href='/"+str(__class__.p184)+"'>2^184</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p183)+"'>2^183</a>|<a href='/"+str(__class__.p182)+"'>2^182</a>|<a href='/"+str(__class__.p181)+"'>2^181</a>|<a href='/"+str(__class__.p180)+"'>2^180</a>|<a href='/"+str(__class__.p179)+"'>2^179</a>|<a href='/"+str(__class__.p178)+"'>2^178</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p177)+"'>2^177</a>|<a href='/"+str(__class__.p176)+"'>2^176</a>|<a href='/"+str(__class__.p175)+"'>2^175</a>|<a href='/"+str(__class__.p174)+"'>2^174</a>|<a href='/"+str(__class__.p173)+"'>2^173</a>|<a href='/"+str(__class__.p172)+"'>2^172</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p171)+"'>2^171</a>|<a href='/"+str(__class__.p170)+"'>2^170</a>|<a href='/"+str(__class__.p169)+"'>2^169</a>|<a href='/"+str(__class__.p168)+"'>2^168</a>|<a href='/"+str(__class__.p167)+"'>2^167</a>|<a href='/"+str(__class__.p166)+"'>2^166</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p165)+"'>2^165</a>|<a href='/"+str(__class__.p164)+"'>2^164</a>|<a href='/"+str(__class__.p163)+"'>2^163</a>|<a href='/"+str(__class__.p162)+"'>2^162</a>|<a href='/"+str(__class__.p161)+"'>2^161</a>|<a href='/"+str(__class__.p160)+"'>2^160</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p159)+"'>2^159</a>|<a href='/"+str(__class__.p158)+"'>2^158</a>|<a href='/"+str(__class__.p157)+"'>2^157</a>|<a href='/"+str(__class__.p156)+"'>2^156</a>|<a href='/"+str(__class__.p155)+"'>2^155</a>|<a href='/"+str(__class__.p154)+"'>2^154</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p153)+"'>2^153</a>|<a href='/"+str(__class__.p152)+"'>2^152</a>|<a href='/"+str(__class__.p151)+"'>2^151</a>|<a href='/"+str(__class__.p150)+"'>2^150</a>|<a href='/"+str(__class__.p149)+"'>2^149</a>|<a href='/"+str(__class__.p148)+"'>2^148</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p147)+"'>2^147</a>|<a href='/"+str(__class__.p146)+"'>2^146</a>|<a href='/"+str(__class__.p145)+"'>2^145</a>|<a href='/"+str(__class__.p144)+"'>2^144</a>|<a href='/"+str(__class__.p143)+"'>2^143</a>|<a href='/"+str(__class__.p142)+"'>2^142</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p141)+"'>2^141</a>|<a href='/"+str(__class__.p140)+"'>2^140</a>|<a href='/"+str(__class__.p139)+"'>2^139</a>|<a href='/"+str(__class__.p138)+"'>2^138</a>|<a href='/"+str(__class__.p137)+"'>2^137</a>|<a href='/"+str(__class__.p136)+"'>2^136</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p135)+"'>2^135</a>|<a href='/"+str(__class__.p134)+"'>2^134</a>|<a href='/"+str(__class__.p133)+"'>2^133</a>|<a href='/"+str(__class__.p132)+"'>2^132</a>|<a href='/"+str(__class__.p131)+"'>2^131</a>|<a href='/"+str(__class__.p130)+"'>2^130</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p129)+"'>2^129</a>|<a href='/"+str(__class__.p128)+"'>2^128</a>|<a href='/"+str(__class__.p127)+"'>2^127</a>|<a href='/"+str(__class__.p126)+"'>2^126</a>|<a href='/"+str(__class__.p125)+"'>2^125</a>|<a href='/"+str(__class__.p124)+"'>2^124</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p123)+"'>2^123</a>|<a href='/"+str(__class__.p122)+"'>2^122</a>|<a href='/"+str(__class__.p121)+"'>2^121</a>|<a href='/"+str(__class__.p120)+"'>2^120</a>|<a href='/"+str(__class__.p119)+"'>2^119</a>|<a href='/"+str(__class__.p118)+"'>2^118</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p117)+"'>2^117</a>|<a href='/"+str(__class__.p116)+"'>2^116</a>|<a href='/"+str(__class__.p115)+"'>2^115</a>|<a href='/"+str(__class__.p114)+"'>2^114</a>|<a href='/"+str(__class__.p113)+"'>2^113</a>|<a href='/"+str(__class__.p112)+"'>2^112</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p111)+"'>2^111</a>|<a href='/"+str(__class__.p110)+"'>2^110</a>|<a href='/"+str(__class__.p109)+"'>2^109</a>|<a href='/"+str(__class__.p108)+"'>2^108</a>|<a href='/"+str(__class__.p107)+"'>2^107</a>|<a href='/"+str(__class__.p106)+"'>2^106</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p105)+"'>2^105</a>|<a href='/"+str(__class__.p104)+"'>2^104</a>|<a href='/"+str(__class__.p103)+"'>2^103</a>|<a href='/"+str(__class__.p102)+"'>2^102</a>|<a href='/"+str(__class__.p101)+"'>2^101</a>|<a href='/"+str(__class__.p100)+"'>2^100</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p99)+"'>2^99</a>|<a href='/"+str(__class__.p98)+"'>2^98</a>|<a href='/"+str(__class__.p97)+"'>2^97</a>|<a href='/"+str(__class__.p96)+"'>2^96</a>|<a href='/"+str(__class__.p95)+"'>2^95</a>|<a href='/"+str(__class__.p94)+"'>2^94</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p93)+"'>2^93</a>|<a href='/"+str(__class__.p92)+"'>2^92</a>|<a href='/"+str(__class__.p91)+"'>2^91</a>|<a href='/"+str(__class__.p90)+"'>2^90</a>|<a href='/"+str(__class__.p89)+"'>2^89</a>|<a href='/"+str(__class__.p88)+"'>2^88</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p87)+"'>2^87</a>|<a href='/"+str(__class__.p86)+"'>2^86</a>|<a href='/"+str(__class__.p85)+"'>2^85</a>|<a href='/"+str(__class__.p84)+"'>2^84</a>|<a href='/"+str(__class__.p83)+"'>2^83</a>|<a href='/"+str(__class__.p82)+"'>2^82</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p81)+"'>2^81</a>|<a href='/"+str(__class__.p82)+"'>2^82</a>|<a href='/"+str(__class__.p81)+"'>2^81</a>|<a href='/"+str(__class__.p80)+"'>2^80</a>|<a href='/"+str(__class__.p79)+"'>2^79</a>|<a href='/"+str(__class__.p78)+"'>2^78</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p77)+"'>2^77</a>|<a href='/"+str(__class__.p76)+"'>2^76</a>|<a href='/"+str(__class__.p75)+"'>2^75</a>|<a href='/"+str(__class__.p74)+"'>2^74</a>|<a href='/"+str(__class__.p73)+"'>2^73</a>|<br>|<a href='/"+str(__class__.p72)+"'>2^72</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p71)+"'>2^71</a>|<a href='/"+str(__class__.p70)+"'>2^70</a>|<a href='/"+str(__class__.p69)+"'>2^69</a>|<a href='/"+str(__class__.p68)+"'>2^68</a>|<a href='/"+str(__class__.p67)+"'>2^67</a>|<a href='/"+str(__class__.p66)+"'>2^66</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p65)+"'>2^65</a>|<a href='/"+str(__class__.p64)+"'>2^64</a>|<a href='/"+str(__class__.p63)+"'>2^63</a>|<a href='/"+str(__class__.p62)+"'>2^62</a>|<a href='/"+str(__class__.p61)+"'>2^61</a>|<a href='/"+str(__class__.p60)+"'>2^60</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p59)+"'>2^59</a>|<a href='/"+str(__class__.p58)+"'>2^58</a>|<a href='/"+str(__class__.p57)+"'>2^57</a>|<a href='/"+str(__class__.p56)+"'>2^56</a>|<a href='/"+str(__class__.p55)+"'>2^55</a>|<a href='/"+str(__class__.p54)+"'>2^54</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p53)+"'>2^53</a>|<a href='/"+str(__class__.p52)+"'>2^52</a>|<a href='/"+str(__class__.p51)+"'>2^51</a>|<a href='/"+str(__class__.p50)+"'>2^50</a>|<a href='/"+str(__class__.p49)+"'>2^49</a>|<a href='/"+str(__class__.p48)+"'>2^48</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p47)+"'>2^47</a>|<a href='/"+str(__class__.p46)+"'>2^46</a>|<a href='/"+str(__class__.p45)+"'>2^45</a>|<a href='/"+str(__class__.p44)+"'>2^44</a>|<a href='/"+str(__class__.p43)+"'>2^43</a>|<a href='/"+str(__class__.p42)+"'>2^42</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p41)+"'>2^41</a>|<a href='/"+str(__class__.p40)+"'>2^40</a>|<a href='/"+str(__class__.p39)+"'>2^39</a>|<a href='/"+str(__class__.p38)+"'>2^38</a>|<a href='/"+str(__class__.p37)+"'>2^37</a>|<a href='/"+str(__class__.p36)+"'>2^36</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p35)+"'>2^35</a>|<a href='/"+str(__class__.p34)+"'>2^34</a>|<a href='/"+str(__class__.p33)+"'>2^33</a>|<a href='/"+str(__class__.p32)+"'>2^32</a>|<a href='/"+str(__class__.p31)+"'>2^31</a>|<a href='/"+str(__class__.p30)+"'>2^30</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p29)+"'>2^29</a>|<a href='/"+str(__class__.p28)+"'>2^28</a>|<a href='/"+str(__class__.p27)+"'>2^27</a>|<a href='/"+str(__class__.p26)+"'>2^26</a>|<a href='/"+str(__class__.p25)+"'>2^25</a>|<a href='/"+str(__class__.p24)+"'>2^24</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p23)+"'>2^23</a>|<a href='/"+str(__class__.p22)+"'>2^22</a>|<a href='/"+str(__class__.p21)+"'>2^21</a>|<a href='/"+str(__class__.p20)+"'>2^20</a>|<a href='/"+str(__class__.p19)+"'>2^19</a>|<a href='/"+str(__class__.p18)+"'>2^18</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p17)+"'>2^17</a>|<a href='/"+str(__class__.p16)+"'>2^16</a>|<a href='/"+str(__class__.p15)+"'>2^15</a>|<a href='/"+str(__class__.p14)+"'>2^14</a>|<a href='/"+str(__class__.p13)+"'>2^13</a>|<a href='/"+str(__class__.p12)+"'>2^12</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p11)+"'>2^11</a>|<a href='/"+str(__class__.p10)+"'>2^10</a>|<a href='/"+str(__class__.p9)+"'>2^9</a>|<a href='/"+str(__class__.p8)+"'>2^8</a>|<a href='/"+str(__class__.p7)+"'>2^7</a>|<a href='/"+str(__class__.p6)+"'>2^6</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p5)+"'>2^5</a>|<a href='/"+str(__class__.p4)+"'>2^4</a>|<a href='/"+str(__class__.p3)+"'>2^3</a>|<a href='/"+str(__class__.p2)+"'>2^2</a>|<a href='/"+str(__class__.p1)+"'>2^1</a>|", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            #getting hex values for starting and ending key on the page
            __class__.starting_key_hex = hex(__class__.startPrivKey)[2:].zfill(64)
            if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494273:
                __class__.ending_key_hex = hex(__class__.startPrivKey+63)[2:].zfill(64)
            else:
                __class__.ending_key_hex = hex(__class__.startPrivKey+127)[2:].zfill(64)
                
            self.wfile.write(bytes("<p style='color:gray;font-weight:bold;'>*Starting Private Key Hex: " + str(__class__.starting_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p style='color:gray;font-weight:bold;'>**Ending Private Key Hex: " + str(__class__.ending_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p id='balance' style='color:brown;font-weight:bold;'>Balance on this Page: False</p>", "utf-8"))
            if sys.platform == 'linux' or sys.platform == 'darwin':
                self.wfile.write(bytes("<pre class='keys'><strong>Private Key Hex</strong>                                                          <strong>Uncompressed Address</strong>                <strong>Compressed Address</strong>                       <strong>SegWit 3 Address</strong>                  <strong>bech32 bc1 Address</strong>                           <strong>ETH Address</strong>                           <strong>WIF Private Key Uncompressed</strong>                            <strong>WIF Private Key Compressed</strong><br>", "utf-8"))   
            if sys.platform == 'win32':
                self.wfile.write(bytes("<pre class='keys'><strong>Private Key Hex</strong>                                                          <strong>Uncompressed Address</strong>                <strong>Compressed Address</strong>                       <strong>SegWit 3 Address</strong>                  <strong>bech32 bc1 Address</strong>                           <strong>ETH Address</strong>                           <strong>WIF Private Key Uncompressed</strong>                            <strong>WIF Private Key Compressed</strong><br>", "utf-8"))                   
            ###---Loop---******************************************************************
            for i in range(0,128): #generating addresses and WIFS to show on page
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
                self.wfile.write(bytes("<lol style='color:#DE3163;'>" +"<lol class='show_popup' rel='popup1' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a>" + "&nbsp<span>"  + "</span>&nbsp" + "</lol>&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_S + "'>" + __class__.bitAddr_S + "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32 + "'>" + __class__.bitAddr_bech32 + "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://ethplorer.io/address/" + __class__.bitAddr_eth + "'>" + __class__.bitAddr_eth + "</a></lol>&nbsp;&nbsp;<lol style='color:#145A32;'>" + "&nbsp;&nbsp;<lol>" + "&nbsp;&nbsp<span>"  + "</span>&nbsp;&nbsp</lol>&nbsp;&nbsp;" + __class__.privKey + "</lol><lol style='color:#145A32;'>" +"&nbsp;&nbsp;<lol>"+__class__.privKey_C+"</lol></br>", "utf-8"))
                if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                __class__.startPrivKey += 1
            ###---Loop---checking if generated addresses are in arr set(if yes then we found address with balance)
            for addr in __class__.addresses:
                if addr in __class__.bloom_filter or addr in __class__.bloom_filter1:
                    __class__.balance_on_page = "True"
                    __class__.foundling = addr + " "
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"Bitcoin Address: {addr} Page# {__class__.num} \n") #saving if found: address page#
            ###__Loop End-------------------------------------------------------------------
            self.wfile.write(bytes("</pre><pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "</p>", "utf-8"))
            self.wfile.write(bytes("<script>var elem = document.getElementById('balance');elem.innerHTML = 'Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "'</script>", "utf-8"))
            self.wfile.write(bytes("""
<script>                       
$('.show_popup').click(function() {
    var path = window.location.pathname;
    if(path == '/904625697166532776746648320380374280100293470930272690489102837043110636675') { $('#all_num').html(64); }           
    var val = $(this).attr('value');
    var num = $(this).attr('num');
    $('#arrow_num').html(num);
    var decNum = BigInt("0x"+val);
    $('#arrow_num').attr('dec', decNum);
    $.get("http://localhost:3333/!"+decNum, function(data, status){
        const myArray = data.split(" ");
        $('#fun2x').html('x: '+myArray[0]);
        $('#fun2y').html('y: '+myArray[1]);
        $('#fun3x').html('x: '+myArray[2]);
        $('#fun3y').html('y: '+myArray[3]);
        $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
        if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
        else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
        $('#fun5').html('x: ' +myArray[7]);
        $('#addinvx').html('x: ' +myArray[8]);
        $('#addinvy').html('y: ' +myArray[9]);
        $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
        $('#addinvn').html(myArray[12]);
        $('#same1x').html('x: ' +myArray[14]);
        $('#same1y').html('y: ' +myArray[1]);
        $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
        $('#same2x').html('x: ' +myArray[18]);
        $('#same2y').html('y: ' +myArray[1]);
        $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
        $('#fun').html(myArray[22]);
        $('#funhex').html(myArray[23]);
    })           
    var popup_id = $('#' + $(this).attr('rel'));
    $(popup_id).show();
    $('.overlay_popup').show();
    $(this).attr('style',  'color:#DE3163;font-weight:bold;');                
})
$('.overlay_popup').click(function() {
    $('.overlay_popup, .popup').hide();
})
$('.ajax').click(function() { 
    var pnum = $(this).attr('page');
    pnum = pnum.substring(1);
    $.get("http://localhost:3333/A"+pnum, function(data, status){
        $('#main_content').html(data)
        history.pushState({}, null, "http://localhost:3333/"+pnum); 
    })
})
$('#arrow_left').click(function() {
    var item_num = parseInt($('#arrow_num').html());
    if(item_num > 1) { 
        $('#arrow_num').html(item_num - 1);
        var decNum = $('#arrow_num').attr('dec');
        var bigNum = BigInt(decNum);
        $.get("http://localhost:3333/!"+(--bigNum), function(data, status){
            const myArray = data.split(" ");
            $('#fun2x').html('x: '+myArray[0]);
            $('#fun2y').html('y: '+myArray[1]);
            $('#fun3x').html('x: '+myArray[2]);
            $('#fun3y').html('y: '+myArray[3]);
            $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
            if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
            else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
            $('#fun5').html('x: ' +myArray[7]);
            $('#addinvx').html('x: ' +myArray[8]);
            $('#addinvy').html('y: ' +myArray[9]);
            $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
            $('#addinvn').html(myArray[12]);
            $('#same1x').html('x: ' +myArray[14]);
            $('#same1y').html('y: ' +myArray[1]);
            $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
            $('#same2x').html('x: ' +myArray[18]);
            $('#same2y').html('y: ' +myArray[1]);
            $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
            $('#fun').html(myArray[22]);
            $('#funhex').html(myArray[23]);
        })
        $('#arrow_num').attr('dec', bigNum);
        var set_style = parseInt($('#arrow_num').html());
        $('*[num="'+(set_style)+'"]').attr('style',  'color:#DE3163;font-weight:bold;');
        $('html, body').animate({scrollTop: $('*[num="'+(set_style)+'"]').offset().top}, 200); 
    }
    else {
        $('#arrow_num').html(item_num); 
    }
})
$('#arrow_right').click(function() {
    var last = 128;
    var path = window.location.pathname;
    if(path == '/904625697166532776746648320380374280100293470930272690489102837043110636675') { last = 64; $('#all_num').html(64); }
    var item_num = parseInt($('#arrow_num').html());
    if(item_num != last) { 
        $('#arrow_num').html(item_num + 1);
        var decNum = $('#arrow_num').attr('dec');
        var bigNum = BigInt(decNum);
        $.get("http://localhost:3333/!"+(++bigNum), function(data, status){
            const myArray = data.split(" ");
            $('#fun2x').html('x: '+myArray[0]);
            $('#fun2y').html('y: '+myArray[1]);
            $('#fun3x').html('x: '+myArray[2]);
            $('#fun3y').html('y: '+myArray[3]);
            $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
            if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
            else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
            $('#fun5').html('x: ' +myArray[7]);
            $('#addinvx').html('x: ' +myArray[8]);
            $('#addinvy').html('y: ' +myArray[9]);
            $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
            $('#addinvn').html(myArray[12]);
            $('#same1x').html('x: ' +myArray[14]);
            $('#same1y').html('y: ' +myArray[1]);
            $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
            $('#same2x').html('x: ' +myArray[18]);
            $('#same2y').html('y: ' +myArray[1]);
            $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
            $('#fun').html(myArray[22]);
            $('#funhex').html(myArray[23]);
        })
        $('#arrow_num').attr('dec', bigNum);
        var set_style = parseInt($('#arrow_num').html());
        $('*[num="'+(set_style)+'"]').attr('style',  'color:#DE3163;font-weight:bold;');
        $('html, body').animate({scrollTop: $('*[num="'+(set_style)+'"]').offset().top}, 200);
    }
    else { 
        $('#arrow_num').html(last); 
    }
})
</script>""", "utf-8")) 
            __class__.addresses.clear() #clearing generated addresses list so we can use it fresh with next page request
            #dropping values to defaults
            __class__.balance_on_page = "False"
            __class__.foundling = ""
            #self.wfile.write(bytes("<button id='up' style='float:right;margin-top:-2%;text-align:center;'>Go Up</button>", "utf-8"))
#---------------------------------------------------------Full Page(Without Ajax(when sending requests from url))---------------------
        else: #full page content
            self.wfile.write(bytes("""
<!DOCTYPE html>
<html>
<head>
<title>BTC & ETH Web Server (Mizogg)</title>
<link rel='shortcut icon' href='https://i1.wp.com/mizogg.co.uk/wp-content/uploads/2021/02/MizoggFace.png?resize=768%2C680&ssl=1' type='image/x-icon'> 
<style>
body{font-size:9.3pt;font-family:'Open Sans',sans-serif;}
a{text-decoration:none}
a:hover {text-decoration: underline}
lol:target {background: #ccffcc; }
.overlay_popup {display:none;position:fixed;z-index: 999;top:0;right:0;left:0;bottom:0;background:#000;opacity:0.5;}
.popup {display: none;position: relative;z-index: 1000;margin:0 25% 0 25%;width:50%;}
.object{z-index: 2;background-color: #eee;margin: 0 auto;position: fixed;top: 50%;left: 50%;transform: translate(-50%, -50%);width: 700px;height: 920px;text-align: center;}
.show_popup:hover {cursor:pointer;text-decoration: underline;}
.ajax:hover {cursor:pointer;text-decoration: underline;}
.arrow:hover {cursor:pointer;box-shadow:0 0 3px #656D9E;cursor:pointer;border:2px solid white;}
.auto_button:hover {box-shadow:0 0 3px #656D9E;cursor:pointer;border:2px solid white;}
.auto_button{height:30px;width:120px;padding:4px;}
#up:hover{box-shadow:0 0 3px #656D9E;cursor:pointer;border:2px solid white;}
#down:hover{box-shadow:0 0 3px #656D9E;cursor:pointer;border:2px solid white;}
.arrow:focus {outline: none;}
input[type=text], select {width:640px;padding:8px 10px;margin: 2px 0;display: inline-block;border: 1px solid #ccc;border-radius: 4px;box-sizing: border-box;text-align:center;}
#search_line:focus {outline: none !important;border:1px solid #D5DBDB;box-shadow: 0 0 4px #719ECE;}
</style>""", "utf-8"))
            #----------jquery library load------------------------------------        
            with open("jquery-3.6.0.js", "r") as f:  
                data = f.read()
            self.wfile.write(bytes("<script>"+str(data)+"</script>", "utf-8"))
            #-----------------------------------------------------------------
            self.wfile.write(bytes("""
</head>
<body link='#0000FF' vlink='#0000FF' alink='#0000FF'>""", "utf-8"))
            self.wfile.write(bytes("<h3><span style='color:#DE3163;'><id='informationauto' >&nbsp;&nbsp;&nbsp;Auto Start& AutoSeq with screen refresh. StartAuto Pilot or Start PilotSeq without screen refresh FASTER &nbsp;</span></h3><h4><span style='color:#DE3163;'><id='informationcommands' >&nbsp;&nbsp;&nbsp;search field added. To use:(paste and remove focus by clicking) WIF search by WIF 1878574747  search by page number @764523535  search page by privatekey decimal $ffff or $FFFFF search page by privatekey hex [123] change increment (2345-8856464646) change random range (72057594037927937-144115188075855873) random range puzzle 64 &nbsp;</span></h4>", "utf-8")) 
            self.wfile.write(bytes("<h2><span style='color:#34495E;'><input type='text' id='search_line' name='lastname' placeholder='Search Field' autocomplete='off'>&nbsp;&nbsp;&nbsp;Bitcoin & ETH Addresses Database. Total Addresses Loaded&nbsp;***|&nbsp;" + str(__class__.addr_count) + "&nbsp;|</span></h2>", "utf-8"))
            self.wfile.write(bytes("<h2><span style='color:#34495E;'><id='information' >&nbsp;&nbsp;&nbsp;Python-WebServer for more information about Python-WebServer.py Visit https://github.com/Mizogg/Python-WebServer or https://mizogg.co.uk &nbsp;</span></h2>", "utf-8"))           
            self.wfile.write(bytes("""
<div id='auto' style='padding-bottom:3px;'> 
<button class='auto_button' id='start_auto'>Auto Start</button>
<button class='auto_button' id='stop_auto'>Auto Stop</button> &nbsp;&nbsp;&nbsp;
<span id='status_str' style='color:brown;font-weight: bold;'>Found [&nbsp;<span id='found_num'>0</span>&nbsp;]&nbsp;
Pages checked:&nbsp;<span id='p_checked'>0</span></span>&nbsp;&nbsp;&nbsp;&nbsp;
<button class='auto_button' id='start_auto_seq'>Start AutoSeq</button>
<button class='auto_button' id='stop_auto_seq'>Stop AutoSeq</button> &nbsp;&nbsp;&nbsp;
<span id='status_str_seq' style='color:brown;font-weight: bold;'>Found [&nbsp;<span id='found_num_seq'>0</span>&nbsp;]&nbsp;&nbsp;&nbsp;
Pages checked:&nbsp;<span id='p_checked_seq'>0</span></span>&nbsp;&nbsp;&nbsp;&nbsp;
<button class='auto_button' id='start_auto_pilot'>Start AutoPilot</button>
<button class='auto_button' id='stop_auto_pilot'>Stop AutoPilot</button> &nbsp;&nbsp;&nbsp;
<span id='status_str_pilot' style='color:brown;font-weight: bold;'>Found [&nbsp;<span id='found_num_pilot'>0</span>&nbsp;]&nbsp;&nbsp;&nbsp;
Pages checked:&nbsp;<span id='p_checked_pilot'>0</span> &nbsp;&nbsp;Total addresses scanned: <span id='t_scanned_pilot'></span></span>&nbsp;&nbsp;&nbsp;&nbsp;
<button class='auto_button' id='start_auto_pilot_seq'>Start PilotSeq</button>
<button class='auto_button' id='stop_auto_pilot_seq'>Stop PilotSeq</button> &nbsp;&nbsp;&nbsp;
<span id='status_str_pilot_seq' style='color:brown;font-weight: bold;'>Found [&nbsp;<span id='found_num_pilot_seq'>0</span>&nbsp;]&nbsp;&nbsp;&nbsp;
Pages checked:&nbsp;<span id='p_checked_pilot_seq'>0</span> &nbsp;&nbsp;Total addresses scanned: <span id='t_scanned_pilot_seq'></span><br>
<span id='status_page' style='margin-left:592px'>Current page: <span id='pilot_page_seq_num'></span></span></span></div>
<script>
var page_number = BigInt(0);
var checked_pages = BigInt(0);
var increment = BigInt(0);
var RandomMin = BigInt(0);
var RandomMax = BigInt(0);
var numPage = BigInt(0);
$('#status_str').hide();
$('#status_str_seq').hide();
$('#status_str_pilot').hide();
$('#status_str_pilot_seq').hide();
$('#stop_auto').hide();
$('#stop_auto_pilot').hide();
$('#stop_auto_pilot_seq').hide();
$('#stop_auto_seq').hide();
$('#search_line').focus(function() {
   $('#search_line').val("");
})
$('#search_line').blur(function() {
   var input_val = $('#search_line').val();
   $.get("http://localhost:3333/S"+ input_val.trim(), function(data, status){
            $('#main_content').html(data);
            history.pushState({}, null, "http://localhost:3333/"+$('#current_page').html());
    })
})
function generateRandomBigInt(lowBigInt, highBigInt) {
    if (lowBigInt >= highBigInt) {
        throw new Error('lowBigInt must be smaller than highBigInt');
    }
    const difference = highBigInt - lowBigInt;
    const differenceLength = difference.toString().length;
    let multiplier = '';
    while (multiplier.length < differenceLength) {
        multiplier += Math.random()
        .toString()
        .split('.')[1];
    }
    multiplier = multiplier.slice(0, differenceLength);
    const divisor = '1' + '0'.repeat(differenceLength);
    const randomDifference = (BigInt(difference) * BigInt(multiplier)) / BigInt(divisor);
    var result = BigInt(lowBigInt) + BigInt(randomDifference)
    return result.toString();
}
function rolling(){                
    numPage = generateRandomBigInt(RandomMin,RandomMax);
    $.get("http://localhost:3333/A"+numPage, function(data, status){
        $('#main_content').html(data)
        history.pushState({}, null, "http://localhost:3333/"+numPage);
        var f_num = parseInt($('#found_num').html()); 
        var found_str = $('#balance').html();
        if(found_str.includes("False") && f_num == 0 ) { 
            $('#found_num').html("0"); 
        }
        if(found_str.includes("False") && f_num > 0 ) {
            $('#found_num').html(f_num);
        }
        if(found_str.includes("True")) {                    
            f_num = f_num + 1;
            $('#found_num').html(f_num); 
        }
    })
    checked_pages++;
    $('#p_checked').html(checked_pages);
}
$('#start_auto').click(function() {  
    $(this).hide();
    $('#stop_auto').show();      
    checked_pages = 0;
    RandomMin = BigInt($('#rand_min').html())
    RandomMax = BigInt($('#rand_max').html())
    $('#start_auto_seq').prop('disabled', true);
    $('#start_auto_pilot').prop('disabled', true);
    $('#start_auto_pilot_seq').prop('disabled', true);
    $('#search_line').prop('disabled', true);
    $('#p_checked').html("0");
    $('#found_num').html("0");
    $('#status_str').show();    
    play_random = setInterval("rolling()",100); 
})
$('#stop_auto').click(function() {
    clearInterval(play_random);                    
    $('#start_auto_seq').prop('disabled', false);
    $('#start_auto_pilot').prop('disabled', false);
    $('#start_auto_pilot_seq').prop('disabled', false);
    $('#search_line').prop('disabled', false);
    $(this).hide();
    $('#start_auto').show();
    $('#status_str').fadeOut(1000);     
})
function sequence() {
    page_number += increment;                
    if (page_number > BigInt("904625697166532776746648320380374280100293470930272690489102837043110636675")) {
        $('#start_auto_seq').prop('disabled', false);
        $('#start_auto').prop('disabled', false);
        $('#start_auto_pilot').prop('disabled', false);
        $('#stop_auto_seq').hide();
        $('#start_auto_seq').show();
        $('#status_str_seq').fadeOut(1500);
        checked_pages = 0;
        clearInterval(play_sequence);         
        return false;
    }
    else {
        $.get("http://localhost:3333/A"+ page_number, function(data, status){
            $('#main_content').html(data);
            history.pushState({}, null, "http://localhost:3333/"+$('#current_page').html());
            var f_num = parseInt($('#found_num_seq').html()); 
            var found_str = $('#balance').html();                    
            if(found_str.includes("False") && f_num == 0 ) { 
                $('#found_num_seq').html("0"); 
            }
            if(found_str.includes("False") && f_num > 0 ) {
                $('#found_num_seq').html(f_num);
            }
            if(found_str.includes("True")) {                    
                f_num = f_num + 1;
                $('#found_num_seq').html(f_num); 
            }
        })
    }
    checked_pages++;
    $('#p_checked_seq').html(checked_pages);                                              
}
$('#start_auto_seq').click(function() {
    $(this).hide();
    $('#stop_auto_seq').show();
    checked_pages = 0;
    page_number = BigInt($('#current_page').html());                
    increment = BigInt($('#cur_inc').html());
    $('#start_auto').prop('disabled', true);
    $('#start_auto_pilot').prop('disabled', true);
    $('#start_auto_pilot_seq').prop('disabled', true);
    $('#search_line').prop('disabled', true);               
    $('#p_checked_seq').html("0");
    $('#found_num_seq').html("0");
    $('#status_str_seq').show();
    play_sequence = setInterval("sequence()",100); 
})
$('#stop_auto_seq').click(function() {
    clearInterval(play_sequence);    
    $('#start_auto').prop('disabled', false);
    $('#start_auto_seq').prop('disabled', false);
    $('#start_auto_pilot').prop('disabled', false);
    $('#start_auto_pilot_seq').prop('disabled', false);
    $('#search_line').prop('disabled', false);
    $(this).hide();
    $('#start_auto_seq').show();
    $('#status_str_seq').fadeOut(1000);                               
})
function pilot(){                
    numPage = generateRandomBigInt(RandomMin,RandomMax);
    $.get("http://localhost:3333/P"+numPage, function(data, status){
        //history.pushState({}, null, "http://localhost:3333/"+numPage);
        var status_str = data;
        var f_num = parseInt($('#found_num_pilot').html());
        if(status_str == "Yes" ) { 
            f_num = f_num + 1;
            $('#found_num_pilot').html(f_num); 
        }
        if(status_str == "No" ) {
            $('#found_num_pilot').html(f_num);
        }
    })
    checked_pages++;
    $('#p_checked_pilot').html(checked_pages);
    $('#t_scanned_pilot').html((checked_pages *256));
}
$('#start_auto_pilot').click(function() {
    RandomMin = BigInt($('#rand_min').html())
    RandomMax = BigInt($('#rand_max').html())
    $('#start_auto').prop('disabled', true);
    $('#start_auto_seq').prop('disabled', true);
    $('#start_auto_pilot_seq').prop('disabled', true);
    checked_pages = 0;
    $('#p_checked_pilot').html("0");
    $('#found_num_pilot').html("0");
    $('#t_scanned_pilot').html("0");
    $('#status_str_pilot').show();
    $(this).hide();
    $('#stop_auto_pilot').show();
    play_pilot = setInterval("pilot()",50);
})
$('#stop_auto_pilot').click(function() {
    clearInterval(play_pilot);
    $('#start_auto').prop('disabled', false);
    $('#start_auto_seq').prop('disabled', false);
    $('#start_auto_pilot_seq').prop('disabled', false);    
    $(this).hide();
    $('#start_auto_pilot').show();    
    $('#status_str_pilot').fadeOut(1000);                                                        
})
function pilot_sequence() {
    page_number += increment;                
    if (page_number > BigInt("904625697166532776746648320380374280100293470930272690489102837043110636675")) {
        $('#start_auto_seq').prop('disabled', false);
        $('#start_auto').prop('disabled', false);
        $('#start_auto_pilot').prop('disabled', false);
        $('#stop_auto_pilot_seq').hide();
        $('#start_auto_pilot_seq').show();
        $('#status_str_pilot_seq').fadeOut(1500);
        checked_pages = 0;
        clearInterval(play_pilot_sequence);         
        return false;
    }
    else {
        $.get("http://localhost:3333/P"+ page_number, function(data, status){
            //history.pushState({}, null, "http://localhost:3333/"+page_number);
            var status_str = data;
            var f_num = parseInt($('#found_num_pilot_seq').html());
            if(status_str == "Yes" ) { 
                f_num = f_num + 1;
                $('#found_num_pilot_seq').html(f_num); 
            }
            if(status_str == "No" ) {
                $('#found_num_pilot_seq').html(f_num);
            }
        })
    }
    checked_pages++;
    $('#p_checked_pilot_seq').html(checked_pages);
    $('#t_scanned_pilot_seq').html((checked_pages *256));
    $('#pilot_page_seq_num').html(page_number);                                              
}
$('#start_auto_pilot_seq').click(function() {
    $(this).hide();
    $('#stop_auto_pilot_seq').show();
    checked_pages = 0;
    page_number = BigInt($('#current_page').html());                
    increment = BigInt($('#cur_inc').html());
    $('#start_auto').prop('disabled', true);
    $('#start_auto_seq').prop('disabled', true);
    $('#start_auto_pilot').prop('disabled', true);               
    $('#p_checked_pilot_seq').html("0");
    $('#found_num_pilot_seq').html("0");
    $('#t_scanned_pilot_seq').html("0");
    $('#status_str_pilot_seq').show();
    play_pilot_sequence = setInterval("pilot_sequence()",50); 
})
$('#stop_auto_pilot_seq').click(function() {
    clearInterval(play_pilot_sequence);
    $('#start_auto').prop('disabled', false);
    $('#start_auto_seq').prop('disabled', false);
    $('#start_auto_pilot').prop('disabled', false);
    $(this).hide();
    $('#start_auto_pilot_seq').show();    
    $('#status_str_pilot_seq').fadeOut(1000);                               
})
</script>
<div id='main_content'>
<div class='overlay_popup'></div>
<div class='popup' id='popup1'>
<div class='object'>
<h4 style='color:brown;font-weight:bold;text-align:right;'>Private ECDSA Key&nbsp;&nbsp;
<button class='arrow' id='arrow_left' style='color:blue;margin-left:132px;'><<<</button>&nbsp;&nbsp;
<span style='color:brown;' id='arrow_num'>1</span> <span style='color:brown;'>of</span> <span  id='all_num' style='color:brown;'>128</span>&nbsp;&nbsp;
<button class='arrow' id='arrow_right' style='color:blue;'>>>></button>&nbsp;&nbsp;</h4>            
<p id='funbin' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;word-wrap: break-word;'></p>            
<p id='funhex' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<h4 style='color:brown;font-weight:bold;'>Public ECDSA Key</h4>
<p id='fun2x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun2y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun3x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun3y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun5' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>           
<h4 style='color:brown;font-weight:bold;'>Additive Inverse Point</h4>
<p id='addinvn' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<p id='addinvx' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<p id='addinvy' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<p id='addrinv' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<h4 style='color:brown;font-weight:bold;'>Two More Points same Y different X</h4>
<p id='same1x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<p id='same1y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<p id='same1addr' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<p id='same2x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<p id='same2y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<p id='same2addr' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;''></p>
<h4 style='color:brown;font-weight:bold;'>RIPEMD-160 Hash</h4>
<p id='fun4' style='color:#34495E ;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
</div></div>""", "utf-8"))
            #self.wfile.write(bytes("<p style='color:#34495E;font-weight:bold;'>123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz - Base58</p>", "utf-8"))      
            ###-----------------------------------------------------------------------------------------
            str_url = self.path[1:] #gettin / outta way from url we do not need
            if str_url.startswith('5H') or str_url.startswith('5J') or str_url.startswith('5K'): # if url starts with 5H 5J 5K we request page by 5WIF
                first_encode = base58.b58decode(self.path[1:])
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                keyU = int(private_key_hex,16)
                __class__.searchKey = ice.privatekey_to_address(0, False, keyU)
                __class__.num = int(private_key_hex,16)
                __class__.num = __class__.num // 128
                __class__.num = __class__.num + 1
                __class__.previous = __class__.num - 1
                if (__class__.previous == 0):
                    __class__.previous = 1
                __class__.next = __class__.num + __class__.stride;                
                if (__class__.next > __class__.max):
                    __class__.next = __class__.max
                __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            elif str_url.startswith('K') or str_url.startswith('L'): # if url starts with L K we request page by LWIF KWIF
                first_encode = base58.b58decode(self.path[1:])
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                keyC = int(private_key_hex[0:64],16)
                __class__.searchKey = ice.privatekey_to_address(0, True, keyC)
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
                if str_url.find("[") >= 0: # if url has [ after page number localhost:3333/123[33]  we want to change increment for next 
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
                elif str_url.find("(") >= 0: # if url has ( after page number localhost:3333/123(100-333) we want to change random range for pages starting with 100 up to 333              
                    __class__.idx1 = str_url.index("(")
                    __class__.idx2 = str_url.index("-")
                    __class__.idx3 = str_url.index(")")
                    __class__.randomMin = int(str_url[__class__.idx1+1:__class__.idx2],10)
                    __class__.randomMax = int(str_url[__class__.idx2+1:__class__.idx3],10)
                    __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                    __class__.num = int(str_url[0:__class__.idx1],10)
                    __class__.previous = __class__.num - 1
                    if __class__.previous == 0:
                        __class__.previous = 1
                    __class__.next = __class__.num + __class__.stride                
                    if __class__.next > __class__.max:
                        __class__.next = __class__.max
                elif str_url.find("$") >= 0:  #if url starts with $ localhost:3333/$f78feb18a  we want to search page by hex value of privatekey              
                    __class__.idx1 = str_url.index("$")
                    if __class__.isHex(str_url[__class__.idx1+1:]) and len(str_url[__class__.idx1+1:]) > 0:                    
                        __class__.num = int(str_url[__class__.idx1+1:],16)
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        __class__.searchKey_U = ice.privatekey_to_address(0, False, __class__.num)
                        __class__.num = __class__.num // 128
                        __class__.num = __class__.num + 1                
                        __class__.previous = __class__.num - 1
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                    else:
                        __class__.num = 1
                        __class__.previous = __class__.num - 1;
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                elif str_url.find("@") >= 0: #if url starts with @ localhost:3333/@186732 we want to search page by decimal value of privatekey               
                    __class__.idx1 = str_url.index("@")
                    if str_url[__class__.idx1+1:].isnumeric():                    
                        __class__.num = int(str_url[__class__.idx1+1:],10)
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        __class__.searchKey_U = ice.privatekey_to_address(0, False, __class__.num)
                        __class__.num = __class__.num // 128
                        __class__.num = __class__.num + 1                
                        __class__.previous = __class__.num - 1
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                    else:
                        __class__.num = 1
                        __class__.previous = __class__.num - 1;
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                else:
                    if str_url == 'favicon.ico': #favicon.ico request gag
                        pass
                    else:
                        if str_url.isnumeric(): #if url contains just page number in decimal localhost:3333/123456 that is correct
                            __class__.num = int(str_url,10)
                            if __class__.num > __class__.max: #if requested page number more than max(last) we set it to max(last)
                                __class__.num = __class__.max
                            __class__.previous = __class__.num - 1;
                            if __class__.previous == 0:
                                 __class__.previous = 1
                            __class__.next = __class__.num + __class__.stride                
                            if __class__.next > __class__.max:
                                 __class__.next = __class__.max
                            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        else: # if page number has not just decimal numbers we set it to first 
                            __class__.num = 1
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
            self.wfile.write(bytes("<h3><span style='color:#D7DBDD;background-color:#145A32;padding:2px;border-radius: 2px;'>Page #</span> <span id='current_page' style='color: #145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>" + str(__class__.num) + "</span> <span style='color:#145A32;'><< out of >></span> <span style='color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h3>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Current page increment for next = <span id='cur_inc'>" + str(__class__.stride) + "</span></p>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Current random range = <span id='rand_min'>" + str(__class__.randomMin) + "</span> - <span id='rand_max'>" + str(__class__.randomMax) + "</span></p>", "utf-8"))
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.first)+"'>first</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.middle)+"'>middle</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.max)+"'>last</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.hj)+"'>5H(end)-5J(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.jk)+"'>5J(end)-5K(start)</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.random5H)+"'>5H_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random5J)+"'>5J_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random5K)+"'>5K_random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.Kx)+"'>Kw(end)_Kx(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.Ky)+"'>Kx(end)_Ky(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.Kz)+"'>Ky(end)_Kz(start)</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.L1)+"'>Kz(end)-L1(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.L2)+"'>L1(end)_L2(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.L3)+"'>L2(end)_L3(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.L4)+"'>L3(end)_L4(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.L5)+"'>L4(end)_L5(start)</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span class='ajax' style='color:blue;' page='/"+str(__class__.randomKw)+"'>Kw_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomKx)+"'>Kx_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomKy)+"'>Ky_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomKz)+"'>Kz_random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL1)+"'>L1_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL2)+"'>L2_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL3)+"'>L3_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL4)+"'>L4_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.randomL5)+"'>L5_random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p255)+"'>2^255</a>|<a href='/"+str(__class__.p254)+"'>2^254</a>|<a href='/"+str(__class__.p253)+"'>2^253</a>|<a href='/"+str(__class__.p252)+"'>2^252</a>|<a href='/"+str(__class__.p251)+"'>2^251</a>|<a href='/"+str(__class__.p250)+"'>2^250</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p249)+"'>2^249</a>|<a href='/"+str(__class__.p248)+"'>2^248</a>|<a href='/"+str(__class__.p247)+"'>2^247</a>|<a href='/"+str(__class__.p246)+"'>2^246</a>|<a href='/"+str(__class__.p245)+"'>2^245</a>|<a href='/"+str(__class__.p244)+"'>2^244</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p243)+"'>2^243</a>|<a href='/"+str(__class__.p242)+"'>2^242</a>|<a href='/"+str(__class__.p241)+"'>2^241</a>|<a href='/"+str(__class__.p240)+"'>2^240</a>|<a href='/"+str(__class__.p239)+"'>2^239</a>|<a href='/"+str(__class__.p238)+"'>2^238</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p237)+"'>2^237</a>|<a href='/"+str(__class__.p236)+"'>2^236</a>|<a href='/"+str(__class__.p235)+"'>2^235</a>|<a href='/"+str(__class__.p234)+"'>2^234</a>|<a href='/"+str(__class__.p233)+"'>2^233</a>|<a href='/"+str(__class__.p232)+"'>2^232</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p231)+"'>2^231</a>|<a href='/"+str(__class__.p230)+"'>2^230</a>|<a href='/"+str(__class__.p229)+"'>2^229</a>|<a href='/"+str(__class__.p228)+"'>2^228</a>|<a href='/"+str(__class__.p227)+"'>2^227</a>|<a href='/"+str(__class__.p226)+"'>2^226</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p225)+"'>2^225</a>|<a href='/"+str(__class__.p224)+"'>2^224</a>|<a href='/"+str(__class__.p223)+"'>2^223</a>|<a href='/"+str(__class__.p222)+"'>2^222</a>|<a href='/"+str(__class__.p221)+"'>2^221</a>|<a href='/"+str(__class__.p220)+"'>2^220</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p219)+"'>2^219</a>|<a href='/"+str(__class__.p218)+"'>2^218</a>|<a href='/"+str(__class__.p217)+"'>2^217</a>|<a href='/"+str(__class__.p216)+"'>2^216</a>|<a href='/"+str(__class__.p215)+"'>2^215</a>|<a href='/"+str(__class__.p214)+"'>2^214</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p213)+"'>2^213</a>|<a href='/"+str(__class__.p212)+"'>2^212</a>|<a href='/"+str(__class__.p211)+"'>2^211</a>|<a href='/"+str(__class__.p210)+"'>2^210</a>|<a href='/"+str(__class__.p209)+"'>2^209</a>|<a href='/"+str(__class__.p208)+"'>2^208</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p207)+"'>2^207</a>|<a href='/"+str(__class__.p206)+"'>2^206</a>|<a href='/"+str(__class__.p205)+"'>2^205</a>|<a href='/"+str(__class__.p204)+"'>2^204</a>|<a href='/"+str(__class__.p203)+"'>2^203</a>|<a href='/"+str(__class__.p202)+"'>2^202</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p201)+"'>2^201</a>|<a href='/"+str(__class__.p200)+"'>2^200</a>|<a href='/"+str(__class__.p199)+"'>2^199</a>|<a href='/"+str(__class__.p198)+"'>2^198</a>|<a href='/"+str(__class__.p197)+"'>2^197</a>|<a href='/"+str(__class__.p196)+"'>2^196</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p195)+"'>2^195</a>|<a href='/"+str(__class__.p194)+"'>2^194</a>|<a href='/"+str(__class__.p193)+"'>2^193</a>|<a href='/"+str(__class__.p192)+"'>2^192</a>|<a href='/"+str(__class__.p191)+"'>2^191</a>|<a href='/"+str(__class__.p190)+"'>2^190</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p189)+"'>2^189</a>|<a href='/"+str(__class__.p188)+"'>2^188</a>|<a href='/"+str(__class__.p187)+"'>2^187</a>|<a href='/"+str(__class__.p186)+"'>2^186</a>|<a href='/"+str(__class__.p185)+"'>2^185</a>|<a href='/"+str(__class__.p184)+"'>2^184</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p183)+"'>2^183</a>|<a href='/"+str(__class__.p182)+"'>2^182</a>|<a href='/"+str(__class__.p181)+"'>2^181</a>|<a href='/"+str(__class__.p180)+"'>2^180</a>|<a href='/"+str(__class__.p179)+"'>2^179</a>|<a href='/"+str(__class__.p178)+"'>2^178</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p177)+"'>2^177</a>|<a href='/"+str(__class__.p176)+"'>2^176</a>|<a href='/"+str(__class__.p175)+"'>2^175</a>|<a href='/"+str(__class__.p174)+"'>2^174</a>|<a href='/"+str(__class__.p173)+"'>2^173</a>|<a href='/"+str(__class__.p172)+"'>2^172</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p171)+"'>2^171</a>|<a href='/"+str(__class__.p170)+"'>2^170</a>|<a href='/"+str(__class__.p169)+"'>2^169</a>|<a href='/"+str(__class__.p168)+"'>2^168</a>|<a href='/"+str(__class__.p167)+"'>2^167</a>|<a href='/"+str(__class__.p166)+"'>2^166</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p165)+"'>2^165</a>|<a href='/"+str(__class__.p164)+"'>2^164</a>|<a href='/"+str(__class__.p163)+"'>2^163</a>|<a href='/"+str(__class__.p162)+"'>2^162</a>|<a href='/"+str(__class__.p161)+"'>2^161</a>|<a href='/"+str(__class__.p160)+"'>2^160</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p159)+"'>2^159</a>|<a href='/"+str(__class__.p158)+"'>2^158</a>|<a href='/"+str(__class__.p157)+"'>2^157</a>|<a href='/"+str(__class__.p156)+"'>2^156</a>|<a href='/"+str(__class__.p155)+"'>2^155</a>|<a href='/"+str(__class__.p154)+"'>2^154</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p153)+"'>2^153</a>|<a href='/"+str(__class__.p152)+"'>2^152</a>|<a href='/"+str(__class__.p151)+"'>2^151</a>|<a href='/"+str(__class__.p150)+"'>2^150</a>|<a href='/"+str(__class__.p149)+"'>2^149</a>|<a href='/"+str(__class__.p148)+"'>2^148</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p147)+"'>2^147</a>|<a href='/"+str(__class__.p146)+"'>2^146</a>|<a href='/"+str(__class__.p145)+"'>2^145</a>|<a href='/"+str(__class__.p144)+"'>2^144</a>|<a href='/"+str(__class__.p143)+"'>2^143</a>|<a href='/"+str(__class__.p142)+"'>2^142</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p141)+"'>2^141</a>|<a href='/"+str(__class__.p140)+"'>2^140</a>|<a href='/"+str(__class__.p139)+"'>2^139</a>|<a href='/"+str(__class__.p138)+"'>2^138</a>|<a href='/"+str(__class__.p137)+"'>2^137</a>|<a href='/"+str(__class__.p136)+"'>2^136</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p135)+"'>2^135</a>|<a href='/"+str(__class__.p134)+"'>2^134</a>|<a href='/"+str(__class__.p133)+"'>2^133</a>|<a href='/"+str(__class__.p132)+"'>2^132</a>|<a href='/"+str(__class__.p131)+"'>2^131</a>|<a href='/"+str(__class__.p130)+"'>2^130</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p129)+"'>2^129</a>|<a href='/"+str(__class__.p128)+"'>2^128</a>|<a href='/"+str(__class__.p127)+"'>2^127</a>|<a href='/"+str(__class__.p126)+"'>2^126</a>|<a href='/"+str(__class__.p125)+"'>2^125</a>|<a href='/"+str(__class__.p124)+"'>2^124</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p123)+"'>2^123</a>|<a href='/"+str(__class__.p122)+"'>2^122</a>|<a href='/"+str(__class__.p121)+"'>2^121</a>|<a href='/"+str(__class__.p120)+"'>2^120</a>|<a href='/"+str(__class__.p119)+"'>2^119</a>|<a href='/"+str(__class__.p118)+"'>2^118</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p117)+"'>2^117</a>|<a href='/"+str(__class__.p116)+"'>2^116</a>|<a href='/"+str(__class__.p115)+"'>2^115</a>|<a href='/"+str(__class__.p114)+"'>2^114</a>|<a href='/"+str(__class__.p113)+"'>2^113</a>|<a href='/"+str(__class__.p112)+"'>2^112</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p111)+"'>2^111</a>|<a href='/"+str(__class__.p110)+"'>2^110</a>|<a href='/"+str(__class__.p109)+"'>2^109</a>|<a href='/"+str(__class__.p108)+"'>2^108</a>|<a href='/"+str(__class__.p107)+"'>2^107</a>|<a href='/"+str(__class__.p106)+"'>2^106</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p105)+"'>2^105</a>|<a href='/"+str(__class__.p104)+"'>2^104</a>|<a href='/"+str(__class__.p103)+"'>2^103</a>|<a href='/"+str(__class__.p102)+"'>2^102</a>|<a href='/"+str(__class__.p101)+"'>2^101</a>|<a href='/"+str(__class__.p100)+"'>2^100</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p99)+"'>2^99</a>|<a href='/"+str(__class__.p98)+"'>2^98</a>|<a href='/"+str(__class__.p97)+"'>2^97</a>|<a href='/"+str(__class__.p96)+"'>2^96</a>|<a href='/"+str(__class__.p95)+"'>2^95</a>|<a href='/"+str(__class__.p94)+"'>2^94</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p93)+"'>2^93</a>|<a href='/"+str(__class__.p92)+"'>2^92</a>|<a href='/"+str(__class__.p91)+"'>2^91</a>|<a href='/"+str(__class__.p90)+"'>2^90</a>|<a href='/"+str(__class__.p89)+"'>2^89</a>|<a href='/"+str(__class__.p88)+"'>2^88</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p87)+"'>2^87</a>|<a href='/"+str(__class__.p86)+"'>2^86</a>|<a href='/"+str(__class__.p85)+"'>2^85</a>|<a href='/"+str(__class__.p84)+"'>2^84</a>|<a href='/"+str(__class__.p83)+"'>2^83</a>|<a href='/"+str(__class__.p82)+"'>2^82</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p81)+"'>2^81</a>|<a href='/"+str(__class__.p82)+"'>2^82</a>|<a href='/"+str(__class__.p81)+"'>2^81</a>|<a href='/"+str(__class__.p80)+"'>2^80</a>|<a href='/"+str(__class__.p79)+"'>2^79</a>|<a href='/"+str(__class__.p78)+"'>2^78</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p77)+"'>2^77</a>|<a href='/"+str(__class__.p76)+"'>2^76</a>|<a href='/"+str(__class__.p75)+"'>2^75</a>|<a href='/"+str(__class__.p74)+"'>2^74</a>|<a href='/"+str(__class__.p73)+"'>2^73</a>|<br>|<a href='/"+str(__class__.p72)+"'>2^72</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p71)+"'>2^71</a>|<a href='/"+str(__class__.p70)+"'>2^70</a>|<a href='/"+str(__class__.p69)+"'>2^69</a>|<a href='/"+str(__class__.p68)+"'>2^68</a>|<a href='/"+str(__class__.p67)+"'>2^67</a>|<a href='/"+str(__class__.p66)+"'>2^66</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p65)+"'>2^65</a>|<a href='/"+str(__class__.p64)+"'>2^64</a>|<a href='/"+str(__class__.p63)+"'>2^63</a>|<a href='/"+str(__class__.p62)+"'>2^62</a>|<a href='/"+str(__class__.p61)+"'>2^61</a>|<a href='/"+str(__class__.p60)+"'>2^60</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p59)+"'>2^59</a>|<a href='/"+str(__class__.p58)+"'>2^58</a>|<a href='/"+str(__class__.p57)+"'>2^57</a>|<a href='/"+str(__class__.p56)+"'>2^56</a>|<a href='/"+str(__class__.p55)+"'>2^55</a>|<a href='/"+str(__class__.p54)+"'>2^54</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p53)+"'>2^53</a>|<a href='/"+str(__class__.p52)+"'>2^52</a>|<a href='/"+str(__class__.p51)+"'>2^51</a>|<a href='/"+str(__class__.p50)+"'>2^50</a>|<a href='/"+str(__class__.p49)+"'>2^49</a>|<a href='/"+str(__class__.p48)+"'>2^48</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p47)+"'>2^47</a>|<a href='/"+str(__class__.p46)+"'>2^46</a>|<a href='/"+str(__class__.p45)+"'>2^45</a>|<a href='/"+str(__class__.p44)+"'>2^44</a>|<a href='/"+str(__class__.p43)+"'>2^43</a>|<a href='/"+str(__class__.p42)+"'>2^42</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p41)+"'>2^41</a>|<a href='/"+str(__class__.p40)+"'>2^40</a>|<a href='/"+str(__class__.p39)+"'>2^39</a>|<a href='/"+str(__class__.p38)+"'>2^38</a>|<a href='/"+str(__class__.p37)+"'>2^37</a>|<a href='/"+str(__class__.p36)+"'>2^36</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p35)+"'>2^35</a>|<a href='/"+str(__class__.p34)+"'>2^34</a>|<a href='/"+str(__class__.p33)+"'>2^33</a>|<a href='/"+str(__class__.p32)+"'>2^32</a>|<a href='/"+str(__class__.p31)+"'>2^31</a>|<a href='/"+str(__class__.p30)+"'>2^30</a>|<br>", "utf-8"))
            self.wfile.write(bytes("|<a href='/"+str(__class__.p29)+"'>2^29</a>|<a href='/"+str(__class__.p28)+"'>2^28</a>|<a href='/"+str(__class__.p27)+"'>2^27</a>|<a href='/"+str(__class__.p26)+"'>2^26</a>|<a href='/"+str(__class__.p25)+"'>2^25</a>|<a href='/"+str(__class__.p24)+"'>2^24</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p23)+"'>2^23</a>|<a href='/"+str(__class__.p22)+"'>2^22</a>|<a href='/"+str(__class__.p21)+"'>2^21</a>|<a href='/"+str(__class__.p20)+"'>2^20</a>|<a href='/"+str(__class__.p19)+"'>2^19</a>|<a href='/"+str(__class__.p18)+"'>2^18</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p17)+"'>2^17</a>|<a href='/"+str(__class__.p16)+"'>2^16</a>|<a href='/"+str(__class__.p15)+"'>2^15</a>|<a href='/"+str(__class__.p14)+"'>2^14</a>|<a href='/"+str(__class__.p13)+"'>2^13</a>|<a href='/"+str(__class__.p12)+"'>2^12</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p11)+"'>2^11</a>|<a href='/"+str(__class__.p10)+"'>2^10</a>|<a href='/"+str(__class__.p9)+"'>2^9</a>|<a href='/"+str(__class__.p8)+"'>2^8</a>|<a href='/"+str(__class__.p7)+"'>2^7</a>|<a href='/"+str(__class__.p6)+"'>2^6</a>|", "utf-8"))
            self.wfile.write(bytes("<a href='/"+str(__class__.p5)+"'>2^5</a>|<a href='/"+str(__class__.p4)+"'>2^4</a>|<a href='/"+str(__class__.p3)+"'>2^3</a>|<a href='/"+str(__class__.p2)+"'>2^2</a>|<a href='/"+str(__class__.p1)+"'>2^1</a>|", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            #generating hex values for starting and ending key
            __class__.starting_key_hex = hex(__class__.startPrivKey)[2:].zfill(64)
            if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494273:
                __class__.ending_key_hex = hex(__class__.startPrivKey+63)[2:].zfill(64)
            else:
                __class__.ending_key_hex = hex(__class__.startPrivKey+127)[2:].zfill(64)
            #----------------------------------------------------------------------------------
            self.wfile.write(bytes("<p style='color:gray;font-weight:bold;'>*Starting Private Key Hex: " + str(__class__.starting_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p style='color:gray;font-weight:bold;'>**Ending Private Key Hex: " + str(__class__.ending_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p id='balance' style='color:brown;font-weight:bold;'>Balance on this Page: False</p>", "utf-8"))
            if sys.platform == 'linux' or sys.platform == 'darwin':
                self.wfile.write(bytes("<pre class='keys'><strong>Private Key Hex</strong>                                                          <strong>Uncompressed Address</strong>                <strong>Compressed Address</strong>                       <strong>SegWit 3 Address</strong>                  <strong>bech32 bc1 Address</strong>                           <strong>ETH Address</strong>                           <strong>WIF Private Key Uncompressed</strong>                            <strong>WIF Private Key Compressed</strong><br>", "utf-8"))
            if sys.platform == 'win32':
                self.wfile.write(bytes("<pre class='keys'><strong>Private Key Hex</strong>                                                          <strong>Uncompressed Address</strong>                <strong>Compressed Address</strong>                       <strong>SegWit 3 Address</strong>                  <strong>bech32 bc1 Address</strong>                           <strong>ETH Address</strong>                           <strong>WIF Private Key Uncompressed</strong>                            <strong>WIF Private Key Compressed</strong><br>", "utf-8"))
            ###---Loop---******************************************************************
            for i in range(0,128): #generating addresses and WIFS to show on page
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
                if __class__.bitAddr == __class__.searchKey or __class__.bitAddr_C == __class__.searchKey or __class__.bitAddr_S == __class__.searchKey or __class__.bitAddr_bech32 == __class__.searchKey or __class__.bitAddr_eth == __class__.searchKey:
                    self.wfile.write(bytes("<lol style='color:#DE3163;'>" +"<lol class='show_popup' rel='popup1' style='color:#DE3163;font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr + "'>" +"<strong>"+ __class__.bitAddr+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C+"'>"+"<strong>"+ __class__.bitAddr_C +"</strong>"+ "</a></lol>&nbsp;&nbsp;<lol>" +"&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr_S + "'>" +"<strong>"+ __class__.bitAddr_S+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32+"'>"+"<strong>"+ __class__.bitAddr_bech32 + "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://ethplorer.io/address/" + __class__.bitAddr_eth+"'>"+"<strong>"+ __class__.bitAddr_eth +"</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='color:#DE3163;'>" +"&nbsp;&nbsp;<lol>"+"<strong>"+ __class__.privKey+ "</strong>"+"</lol><lol style='color:#DE3163;'>" +"&nbsp;&nbsp;<lol>"+"<strong>"+ __class__.privKey_C+ "</strong>"+"</lol></br>", "utf-8"))
                    __class__.searchKey = ""
                elif __class__.bitAddr == __class__.searchKey_U:
                    self.wfile.write(bytes("<lol style='color:#DE3163;'>" +"<lol class='show_popup' rel='popup1' style='color:#red;font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr + "'>" +"<strong>"+ __class__.bitAddr+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C+"'>"+"<strong>"+ __class__.bitAddr_C +"</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol>" +"&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/"+ __class__.bitAddr_S + "'>" +"<strong>"+ __class__.bitAddr_S+ "</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32+"'>"+"<strong>"+ __class__.bitAddr_bech32 +"</strong>"+ "</a></lol>&nbsp;&nbsp;&nbsp;<lol>" +"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://ethplorer.io/address/"+ __class__.bitAddr_eth + "'>" +"<strong>"+ __class__.bitAddr_eth+ "</strong>"+ "</a></lol><lol>" + "&nbsp;&nbsp<span>&nbsp;&nbsp;&nbsp;&nbsp;"  + "</span>&nbsp;&nbsp</lol>&nbsp;&nbsp;<lol style='color:#DE3163;'>" +"<strong>"+ __class__.privKey +"</strong>"+ "</lol>&nbsp;&nbsp;<lol style='color:#DE3163;'>"+"<strong>"+__class__.privKey_C+"</strong>"+"</lol></br>", "utf-8"))
                    __class__.searchKey_U = ""
                else:
                    self.wfile.write(bytes("<lol style='color:#DE3163;'>" +"<lol class='show_popup' rel='popup1' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</lol>&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a>" + "&nbsp<span>"  + "</span>&nbsp" + "</lol>&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_S + "'>" + __class__.bitAddr_S + "</a></lol>&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#145A32;'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_bech32 + "'>" + __class__.bitAddr_bech32 + "</a></lol>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<lol style='display:inline-block;width:230px;color:#D35400;'><a target='_blank' href='https://ethplorer.io/address/" + __class__.bitAddr_eth + "'>" + __class__.bitAddr_eth + "</a></lol>&nbsp;&nbsp;<lol style='color:#145A32;'>" + "&nbsp;&nbsp;<lol>" + "&nbsp;&nbsp<span>"  + "</span>&nbsp;&nbsp</lol>&nbsp;&nbsp;" + __class__.privKey + "</lol><lol style='color:#145A32;'>" +"&nbsp;&nbsp;<lol>"+__class__.privKey_C+"</lol></br>", "utf-8"))
                if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                __class__.startPrivKey += 1
            ###---Loop---checking if generated addresses are in arr set(if yes then we found address with balance)
            for addr in __class__.addresses:
                if addr in __class__.bloom_filter or addr in __class__.bloom_filter1:
                    __class__.balance_on_page = "True"
                    __class__.foundling = addr + " "
                    with open("found.txt", "a", encoding="utf-8") as f: #saving if found: address page#
                        f.write(f"Bitcoin or ETH Address: {addr} Found on Page# {__class__.num} \n")
            #-------------------------------------------------------------------------------
            self.wfile.write(bytes("</pre><pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            self.wfile.write(bytes("<p style='color:brown;font-weight:bold;'>Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "</p>", "utf-8"))
            self.wfile.write(bytes("<script>var elem = document.getElementById('balance');elem.innerHTML = 'Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "'</script>", "utf-8"))
            self.wfile.write(bytes("</div>", "utf-8"))
            #----------handle using jquery(modal popup  - ajax requests send - forward backward on modal window)-------------------------------------
            self.wfile.write(bytes("""
<script>
$('.show_popup').click(function() {
    var path = window.location.pathname;
    if(path == '/904625697166532776746648320380374280100293470930272690489102837043110636675') { $('#all_num').html(64); }           
    var val = $(this).attr('value');
    var num = $(this).attr('num');
    $('#arrow_num').html(num);
    var decNum = BigInt("0x"+val);
    $('#arrow_num').attr('dec', decNum);
    $.get("http://localhost:3333/!"+decNum, function(data, status){
        const myArray = data.split(" ");
        $('#fun2x').html('x: '+myArray[0]);
        $('#fun2y').html('y: '+myArray[1]);
        $('#fun3x').html('x: '+myArray[2]);
        $('#fun3y').html('y: '+myArray[3]);
        $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
        if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
        else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
        $('#fun5').html('x: ' +myArray[7]);
        $('#addinvx').html('x: ' +myArray[8]);
        $('#addinvy').html('y: ' +myArray[9]);
        $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
        $('#addinvn').html(myArray[12]);
        $('#same1x').html('x: ' +myArray[14]);
        $('#same1y').html('y: ' +myArray[1]);
        $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
        $('#same2x').html('x: ' +myArray[18]);
        $('#same2y').html('y: ' +myArray[1]);
        $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
        $('#fun').html(myArray[22]);
        $('#funhex').html(myArray[23]);
    })            
    var popup_id = $('#' + $(this).attr('rel'));
    $(popup_id).show();
    $('.overlay_popup').show();
    $(this).attr('style',  'color:#DE3163;font-weight:bold;');
})
$('.overlay_popup').click(function() {
    $('.overlay_popup, .popup').hide();
})
$('.ajax').click(function() { 
    var pnum = $(this).attr('page');
    pnum = pnum.substring(1);
    $.get("http://localhost:3333/A"+pnum, function(data, status){
        $('#main_content').html(data)
        history.pushState({}, null, "http://localhost:3333/"+pnum); 
    })
})
$('#arrow_left').click(function() {
    var item_num = parseInt($('#arrow_num').html());
    if(item_num > 1) { 
        $('#arrow_num').html(item_num - 1);
        var decNum = $('#arrow_num').attr('dec');
        var bigNum = BigInt(decNum);
        $.get("http://localhost:3333/!"+(--bigNum), function(data, status){
            const myArray = data.split(" ");
            $('#fun2x').html('x: '+myArray[0]);
            $('#fun2y').html('y: '+myArray[1]);
            $('#fun3x').html('x: '+myArray[2]);
            $('#fun3y').html('y: '+myArray[3]);
            $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
            if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
            else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
            $('#fun5').html('x: ' +myArray[7]);
            $('#addinvx').html('x: ' +myArray[8]);
            $('#addinvy').html('y: ' +myArray[9]);
            $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
            $('#addinvn').html(myArray[12]);
            $('#same1x').html('x: ' +myArray[14]);
            $('#same1y').html('y: ' +myArray[1]);
            $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
            $('#same2x').html('x: ' +myArray[18]);
            $('#same2y').html('y: ' +myArray[1]);
            $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
            $('#fun').html(myArray[22]);
            $('#funhex').html(myArray[23]);
        })
        $('#arrow_num').attr('dec', bigNum);
        var set_style = parseInt($('#arrow_num').html());
        $('*[num="'+(set_style)+'"]').attr('style',  'color:#DE3163;font-weight:bold;');
        $('html, body').animate({scrollTop: $('*[num="'+(set_style)+'"]').offset().top}, 200); 
    }
    else { 
        $('#arrow_num').html(item_num); 
    }
})
$('#arrow_right').click(function() {
    var last = 128;
    var path = window.location.pathname;
    if(path == '/904625697166532776746648320380374280100293470930272690489102837043110636675') { last = 64; $('#all_num').html(64); }
    var item_num = parseInt($('#arrow_num').html());
    if(item_num != last) { 
        $('#arrow_num').html(item_num + 1);
        var decNum = $('#arrow_num').attr('dec');
        var bigNum = BigInt(decNum);
        $.get("http://localhost:3333/!"+(++bigNum), function(data, status){
            const myArray = data.split(" ");
            $('#fun2x').html('x: '+myArray[0]);
            $('#fun2y').html('y: '+myArray[1]);
            $('#fun3x').html('x: '+myArray[2]);
            $('#fun3y').html('y: '+myArray[3]);
            $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
            if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
            else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
            $('#fun5').html('x: ' +myArray[7]);
            $('#addinvx').html('x: ' +myArray[8]);
            $('#addinvy').html('y: ' +myArray[9]);
            $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
            $('#addinvn').html(myArray[12]);
            $('#same1x').html('x: ' +myArray[14]);
            $('#same1y').html('y: ' +myArray[1]);
            $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
            $('#same2x').html('x: ' +myArray[18]);
            $('#same2y').html('y: ' +myArray[1]);
            $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
            $('#fun').html(myArray[22]);
            $('#funhex').html(myArray[23]);
        })
        $('#arrow_num').attr('dec', bigNum);
        var set_style = parseInt($('#arrow_num').html());
        $('*[num="'+(set_style)+'"]').attr('style',  'color:#DE3163;font-weight:bold;');
        $('html, body').animate({scrollTop: $('*[num="'+(set_style)+'"]').offset().top}, 200);
    }
    else { 
        $('#arrow_num').html(last); 
    }
})                                                                       
$(function() {
    $('#up').click(function(){
        $('html,body').animate({scrollTop:0},400);
    });
})           
</script>""", "utf-8"))
            __class__.addresses.clear() #clearing generated addresses list so we can use it fresh with next page request
            #dropping values to defaults
            __class__.balance_on_page = "False" 
            __class__.foundling = ""
            self.wfile.write(bytes("<button id='up' style='float:right;margin-top:-2%;text-align:center;width:80px;height:30px;'>Go Up</button>", "utf-8"))             
            self.wfile.write(bytes("</body></html>", "utf-8")) # end of webpage
    ######################################################################################
if __name__ == "__main__":        
    webServer = ThreadedHTTPServer((hostName, serverPort), WebServer)
    print("Server started at http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
