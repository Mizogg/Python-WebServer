#29/07/2022 BTC & ETH
from __future__ import annotations
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import hashlib
import base58
import binascii
from typing import Optional, Tuple
import secp256k1 as ice
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate
from pathlib import Path
from pygame import mixer
from rich import print
Mizogg = '''[red]
                ╔═╗╔═╗                   
                ║║╚╝║║                   
                ║╔╗╔╗║╔╗╔═══╗╔══╗╔══╗╔══╗
                ║║║║║║╠╣╠══║║║╔╗║║╔╗║║╔╗║
                ║║║║║║║║║║══╣║╚╝║║╚╝║║╚╝║
                ╚╝╚╝╚╝╚╝╚═══╝╚══╝╚═╗║╚═╗║
                                 ╔═╝║╔═╝║
                                 ╚══╝╚══╝
                  ___            ___  
                 (o o)          (o o) 
                (  V  ) MIZOGG (  V  )
                --m-m------------m-m--
                Webserver.py BTC & ETH
                        BONUS
[/red]'''
print (Mizogg)

hostName = "localhost"
serverPort = 3334
G = bytes(bytearray.fromhex('0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8'))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
   
#**************************************************************Jacobian
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
gz = 0x1

def inverse_mod(a, m):
    if a < 0 or m <= a: a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod(d, c) + (c,)
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
    if ud > 0: return ud
    else: return ud + m

def from_jacobian(Xp, Yp, Zp):
    z = inverse_mod(Zp, p)
    return (Xp * z**2) % p, (Yp * z**3) % p

def checkpoint(x, y):
    if (x**3 + 7) % p == y**2 % p : return True
    else: return  False

def bit_to_add(a):
    d=[]
    bitl= a.bit_length()
    for i in range(bitl):
        c = a | (1 << i)
        if c == a: d.append(2**i)
    return d

def double_gen_point(x, y, z):
    points = {1: [x, y, z]}
    for i in range(1, r.bit_length()):
        x, y, z = double(x, y, z)
        points[2**i] = [x, y, z]
    return points

def double(x, y, z):
    s = 4 * x * y**2 % p
    m = 3 * x**2 % p
    x1 = (m**2 - 2 * s) % p
    y1 = (m * (s - x1) - 8 * y**4) % p
    z1 = 2 * y * z % p
    return x1, y1, z1

def add(Xp, Yp, Zp, Xq, Yq, Zq):
    if not Yp: return (Xq, Yq, Zq)
    if not Yq: return(Xp, Yp, Zp)
    u1 = (Xp * Zq**2) % p
    u2 = (Xq * Zp**2) % p
    s1 = (Yp * Zq**3) % p
    s2 = (Yq * Zp**3) % p
    if u1 == u2:
        if s1 != s2: return(0, 0, 1)
        return jacobian_double(Xp, Yp, Zp)
    h = u2 - u1
    rs = s2 - s1
    h2 = (h * h) % p
    h3 = (h * h2) % p
    u1h2 = (u1 * h2) % p
    nx = (rs**2 - h3 - 2 * u1h2) % p
    ny = (rs * (u1h2 - nx) - s1 * h3) % p
    nz = (h * Zp * Zq) % p
    return nx, ny, nz

dbgen = double_gen_point(gx, gy, gz)

def get_pubkey(n):
    if n >= r: return 'Out of range'
    if n in dbgen: return from_jacobian(dbgen[n][0], dbgen[n][1], dbgen[n][2])
    btad = bit_to_add(n)
    point = dbgen[btad[0]]
    for i in btad[1:]:
        point = add(point[0], point[1], point[2], dbgen[i][0], dbgen[i][1], dbgen[i][2])
    point = from_jacobian(point[0], point[1], point[2])
    check = checkpoint(point[0], point[1])
    if check : return point
    else: return 0, 0

#******************************************************************************************
class WebServer(BaseHTTPRequestHandler):
    ##########_class_attributes_###########################################################
    num=startPrivKey=0
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
    
    addresses = list()
    arr = set()    
    bloombtc = Path(__file__).resolve()
    ressbtc = bloombtc.parents[0] / 'btc.bf'
    bloometh = Path(__file__).resolve()
    resseth = bloometh.parents[0] / 'eth.bf'
    
    
    with open(resseth, "rb") as fp:
        bloom_filter1 = BloomFilter.load(fp)   

    with open(ressbtc, "rb") as fp:
        bloom_filter = BloomFilter.load(fp)
    
    addr_countbtc = len(bloom_filter)
    addr_countETH = len(bloom_filter1)
    addr_count = len(bloom_filter)+len(bloom_filter1)

    ##########_webserver_work_############################################################
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        str_url = self.path[1:]
        addresses = list()
        if str_url.startswith("A"): #Ajax
            str_url = self.path[2:]
            __class__.num = int(str_url,10)
            __class__.previous = __class__.num - 1;
            if __class__.previous == 0:
                __class__.previous = 1
            __class__.next = __class__.num + __class__.stride                
            if __class__.next > __class__.max:
                __class__.next = __class__.max
            __class__.startPrivKey = (__class__.num - 1) * 128+1
            self.wfile.write(bytes("<h3><a style='color:green;' href='http://localhost:3333/1'> **********MAIN VERSION********** BACK TO MAIN **********MAIN VERSION********** </a></h3>'", "utf-8"))
            self.wfile.write(bytes("<h2><span style='color:#34495E;'>&nbsp;&nbsp;&nbsp;Bitcoin & ETH Addresses Database. Total Addresses Loaded&nbsp;***|&nbsp;" + str(__class__.addr_count) + "&nbsp;|</span></h2>", "utf-8"))
            self.wfile.write(bytes("<h3><span style='color:#34495E;'>&nbsp;&nbsp;&nbsp;Bitcoin  Total Addresses Loaded&nbsp;***|&nbsp;" + str(__class__.addr_countbtc) + "&nbsp;|</span></h3>", "utf-8"))
            self.wfile.write(bytes("<h3><span style='color:#34495E;'>&nbsp;&nbsp;&nbsp; ETH Addresses Total Loaded&nbsp;***|&nbsp;" + str(__class__.addr_countETH) + "&nbsp;|</span></h3>", "utf-8"))
            self.wfile.write(bytes("<h2><span style='color:#34495E;'><id='information' >&nbsp;&nbsp;&nbsp;Python-WebServer for more information about Python-WebServer.py Visit" + "<a href='https://github.com/Mizogg/Python-WebServer'> Python-WebServer GitHub </a>" + " or " + "<a href='https://mizogg.co.uk/'> Mizogg Home Website </a></h2>", "utf-8")) 
            self.wfile.write(bytes("<h3><span style='color:#145A32;background-color:#f2f3f4;padding:2px;border-radius: 2px;'>Page #</span> <span id='current_page' style='color: #145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>" + str(__class__.num) + "</span> <span style='color:#145A32;'><< out of >></span> <span style='color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h3>", "utf-8"))
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span>&nbsp;]&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.first)+"'>first</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.middle)+"'>middle</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.max)+"'>last</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))            
            self.wfile.write(bytes("<pre>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p255)+"'>2^255</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p254)+"'>2^254</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p253)+"'>2^253</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p252)+"'>2^252</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p251)+"'>2^251</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p250)+"'>2^250</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p249)+"'>2^249</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p248)+"'>2^248</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p247)+"'>2^247</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p246)+"'>2^246</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p245)+"'>2^245</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p244)+"'>2^244</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p243)+"'>2^243</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p242)+"'>2^242</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p241)+"'>2^241</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p240)+"'>2^240</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p239)+"'>2^239</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p238)+"'>2^238</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p237)+"'>2^237</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p236)+"'>2^236</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p235)+"'>2^235</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p234)+"'>2^234</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p233)+"'>2^233</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p232)+"'>2^232</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p231)+"'>2^231</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p230)+"'>2^230</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p229)+"'>2^229</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p228)+"'>2^228</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p227)+"'>2^227</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p226)+"'>2^226</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p225)+"'>2^225</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p224)+"'>2^224</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p223)+"'>2^223</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p222)+"'>2^222</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p221)+"'>2^221</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p220)+"'>2^220</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p219)+"'>2^219</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p218)+"'>2^218</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p217)+"'>2^217</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p216)+"'>2^216</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p215)+"'>2^215</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p214)+"'>2^214</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p213)+"'>2^213</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p212)+"'>2^212</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p211)+"'>2^211</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p210)+"'>2^210</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p209)+"'>2^209</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p208)+"'>2^208</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p207)+"'>2^207</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p206)+"'>2^206</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p205)+"'>2^205</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p204)+"'>2^204</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p203)+"'>2^203</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p202)+"'>2^202</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p201)+"'>2^201</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p200)+"'>2^200</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p199)+"'>2^199</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p198)+"'>2^198</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p197)+"'>2^197</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p196)+"'>2^196</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p195)+"'>2^195</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p194)+"'>2^194</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p193)+"'>2^193</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p192)+"'>2^192</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p191)+"'>2^191</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p190)+"'>2^190</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p189)+"'>2^189</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p188)+"'>2^188</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p187)+"'>2^187</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p186)+"'>2^186</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p185)+"'>2^185</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p184)+"'>2^184</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p183)+"'>2^183</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p182)+"'>2^182</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p181)+"'>2^181</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p180)+"'>2^180</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p179)+"'>2^179</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p178)+"'>2^178</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p177)+"'>2^177</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p176)+"'>2^176</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p175)+"'>2^175</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p174)+"'>2^174</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p173)+"'>2^173</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p172)+"'>2^172</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p171)+"'>2^171</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p170)+"'>2^170</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p169)+"'>2^169</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p168)+"'>2^168</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p167)+"'>2^167</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p166)+"'>2^166</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p165)+"'>2^165</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p164)+"'>2^164</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p163)+"'>2^163</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p162)+"'>2^162</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p161)+"'>2^161</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p160)+"'>2^160</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p159)+"'>2^159</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p158)+"'>2^158</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p157)+"'>2^157</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p156)+"'>2^156</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p155)+"'>2^155</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p154)+"'>2^154</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p153)+"'>2^153</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p152)+"'>2^152</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p151)+"'>2^151</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p150)+"'>2^150</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p149)+"'>2^149</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p148)+"'>2^148</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p147)+"'>2^147</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p146)+"'>2^146</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p145)+"'>2^145</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p144)+"'>2^144</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p143)+"'>2^143</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p142)+"'>2^142</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p141)+"'>2^141</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p140)+"'>2^140</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p139)+"'>2^139</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p138)+"'>2^138</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p137)+"'>2^137</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p136)+"'>2^136</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p135)+"'>2^135</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p134)+"'>2^134</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p133)+"'>2^133</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p132)+"'>2^132</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p131)+"'>2^131</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p130)+"'>2^130</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p129)+"'>2^129</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p128)+"'>2^128</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p127)+"'>2^127</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p126)+"'>2^126</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p125)+"'>2^125</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p124)+"'>2^124</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p123)+"'>2^123</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p122)+"'>2^122</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p121)+"'>2^121</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p120)+"'>2^120</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p119)+"'>2^119</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p118)+"'>2^118</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p117)+"'>2^117</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p116)+"'>2^116</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p115)+"'>2^115</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p114)+"'>2^114</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p113)+"'>2^113</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p112)+"'>2^112</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p111)+"'>2^111</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p110)+"'>2^110</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p109)+"'>2^109</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p108)+"'>2^108</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p107)+"'>2^107</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p106)+"'>2^106</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p105)+"'>2^105</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p104)+"'>2^104</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p103)+"'>2^103</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p102)+"'>2^102</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p101)+"'>2^101</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p100)+"'>2^100</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p99)+"'>2^99</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p98)+"'>2^98</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p97)+"'>2^97</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p96)+"'>2^96</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p95)+"'>2^95</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p94)+"'>2^94</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p93)+"'>2^93</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p92)+"'>2^92</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p91)+"'>2^91</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p90)+"'>2^90</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p89)+"'>2^89</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p88)+"'>2^88</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p87)+"'>2^87</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p86)+"'>2^86</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p85)+"'>2^85</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p84)+"'>2^84</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p83)+"'>2^83</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p82)+"'>2^82</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p81)+"'>2^81</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p82)+"'>2^82</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p81)+"'>2^81</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p80)+"'>2^80</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p79)+"'>2^79</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p78)+"'>2^78</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p77)+"'>2^77</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p76)+"'>2^76</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p75)+"'>2^75</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p74)+"'>2^74</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p73)+"'>2^73</a><br><a style='color:blue;' class='ajax' page='/"+str(__class__.p72)+"'>2^72</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p71)+"'>2^71</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p70)+"'>2^70</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p69)+"'>2^69</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p68)+"'>2^68</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p67)+"'>2^67</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p66)+"'>2^66</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p65)+"'>2^65</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p64)+"'>2^64</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p63)+"'>2^63</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p62)+"'>2^62</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p61)+"'>2^61</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p60)+"'>2^60</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p59)+"'>2^59</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p58)+"'>2^58</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p57)+"'>2^57</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p56)+"'>2^56</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p55)+"'>2^55</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p54)+"'>2^54</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p53)+"'>2^53</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p52)+"'>2^52</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p51)+"'>2^51</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p50)+"'>2^50</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p49)+"'>2^49</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p48)+"'>2^48</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p47)+"'>2^47</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p46)+"'>2^46</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p45)+"'>2^45</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p44)+"'>2^44</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p43)+"'>2^43</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p42)+"'>2^42</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p41)+"'>2^41</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p40)+"'>2^40</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p39)+"'>2^39</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p38)+"'>2^38</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p37)+"'>2^37</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p36)+"'>2^36</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p35)+"'>2^35</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p34)+"'>2^34</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p33)+"'>2^33</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p32)+"'>2^32</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p31)+"'>2^31</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p30)+"'>2^30</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p29)+"'>2^29</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p28)+"'>2^28</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p27)+"'>2^27</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p26)+"'>2^26</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p25)+"'>2^25</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p24)+"'>2^24</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p23)+"'>2^23</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p22)+"'>2^22</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p21)+"'>2^21</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p20)+"'>2^20</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p19)+"'>2^19</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p18)+"'>2^18</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p17)+"'>2^17</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p16)+"'>2^16</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p15)+"'>2^15</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p14)+"'>2^14</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p13)+"'>2^13</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p12)+"'>2^12</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p11)+"'>2^11</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p10)+"'>2^10</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p9)+"'>2^9</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p8)+"'>2^8</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p7)+"'>2^7</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p6)+"'>2^6</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p5)+"'>2^5</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p4)+"'>2^4</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p3)+"'>2^3</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p2)+"'>2^2</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p1)+"'>2^1</a>", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            ###---Loop---******************************************************************
            for i in range(0,128):
                #pubkey = get_pubkey(__class__.startPrivKey)
                pub = ice.point_multiplication(__class__.startPrivKey,G).hex()
                addrU = ice.pubkey_to_address(0, False, bytes(bytearray.fromhex(pub)))
                addrC = ice.pubkey_to_address(0, True, bytes(bytearray.fromhex(pub)))
                addrS = ice.privatekey_to_address(1, True, __class__.startPrivKey) #p2sh
                addrbech32 = ice.privatekey_to_address(2, True, __class__.startPrivKey) #bech32
                addrETH = ice.privatekey_to_ETH_address(__class__.startPrivKey)[2:]
                self.wfile.write(bytes("<div style='background-color:#D7DBDD;text-align:center;padding:4px;margin:4px;width:98%;height:160px;'>", "utf-8"))
                self.wfile.write(bytes("<p style='text-align:left;'><span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+addrU+"'>"+addrU+"</a></span>&nbsp;&nbsp;&nbsp;<span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>C: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+addrC+"'>"+addrC+"</a></span>&nbsp;&nbsp;&nbsp;<span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>3: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+addrS+"'>"+addrS+"</a></span>&nbsp;&nbsp;&nbsp;<span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>BC1: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+addrbech32+"'>"+addrbech32+"</a></span>&nbsp;&nbsp;&nbsp;<span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>ETH: <a target='_blank'  href='https://ethplorer.io/address/0x"+addrETH+"'>0x"+addrETH+"</a></span></p>","utf-8"))
                self.wfile.write(bytes("<p style='text-align:left;font-weight:bold;'><span style='color:#34495E;background-color:white;padding:3px;font-size:12px;'><span style='color:brown;'>DEC: </span>"+str(__class__.startPrivKey)+"</span><span style='color:#DE3163;margin-left:12px;background-color:white;padding:3px;font-size:12px;'><span style='color:brown;f'>HEX: </span>"+str(hex(__class__.startPrivKey)[2:].zfill(64))+"</span><span style='color:brown;margin-left:12px;background-color:white;padding:3px;font-size:12px;'>"+str(len(bin(__class__.startPrivKey)[2:]))+"bit</span></p>", "utf-8"))
                self.wfile.write(bytes("<p style='text-align:left;font-weight:bold;'><span style='color:brown;background-color:white;padding:3px;font-size:12px;'>"+str(bin(__class__.startPrivKey)[2:])+"</span>", "utf-8"))
                self.wfile.write(bytes("<p>"+"<span style='color:#21618C;padding:3px;font-weight:bold;font-size: 12px;'>X: "+str(int(pub[2:66],16))+"</span> "+"<span style='color:#239B56;padding:3px;font-weight:bold;font-size: 12px;'>Y: "+str(int(pub[66:],16))+"</span></p>", "utf-8"))
                self.wfile.write(bytes("<p>"+"<span style='color:#21618C;padding:3px;font-weight:bold;font-size: 12px;'>X: "+str(pub[2:66])+"</span> "+"<span style='color:#239B56;padding:3px;font-weight:bold;font-size: 12px;'>Y: "+str(pub[66:])+"</span></p>", "utf-8"))
                self.wfile.write(bytes("</div>", "utf-8"))
                if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                __class__.startPrivKey += 1
            for addr in addresses:
                if addr in __class__.bloom_filter:
                    status = 'Yes'
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"Bitcoin Address: {addr}  Found on Page# {__class__.num} \n")
                if addr in __class__.bloom_filter1:
                    status = 'Yes'
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"ETH Address: 0x{addr}  Found on Page# {__class__.num} \n")
                    if status == "Yes":
                        mixer.init()
                        mixer.music.load("success.mp3")
                        mixer.music.play()
            ###---Loop---******************************************************************
            self.wfile.write(bytes("</pre><pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            self.wfile.write(bytes("""
            <script>
            $('.ajax').click(function() { 
                var pnum = $(this).attr('page');
                pnum = pnum.substring(1);
                $.get("http://localhost:3334/A"+pnum, function(data, status){
                    $('#main_content').html(data)
                    history.pushState({}, null, "http://localhost:3334/"+pnum); 
                })
            })           
            </script>""", "utf-8"))
        else: #Full Page
            #str_url = self.path[1:]
            __class__.num = int(str_url,10)
            __class__.previous = __class__.num - 1;
            if __class__.previous == 0:
                __class__.previous = 1
            __class__.next = __class__.num + __class__.stride                
            if __class__.next > __class__.max:
                __class__.next = __class__.max               
            __class__.startPrivKey = (__class__.num - 1) * 128+1
            
            self.wfile.write(bytes("<!DOCTYPE html>","utf-8"))
            self.wfile.write(bytes("<html>","utf-8"))
            self.wfile.write(bytes("<head>","utf-8"))
            self.wfile.write(bytes("<title>Webserver.py Bonus</title>","utf-8"))
            self.wfile.write(bytes("<link rel='shortcut icon' href='https://i1.wp.com/mizogg.co.uk/wp-content/uploads/2021/02/MizoggFace.png?resize=768%2C680&ssl=1' type='image/x-icon'>", "utf-8")) 
            self.wfile.write(bytes("""
<style>
body{font-size:9.3pt;font-family:'Open Sans',sans-serif;}
a{text-decoration:none}
a:hover {text-decoration: underline}
.ajax:hover {cursor:pointer;text-decoration: underline;}
#up:hover{box-shadow:0 0 3px #656D9E;cursor:pointer;border:2px solid white;}
</style>""", "utf-8"))
            self.wfile.write(bytes("<script src='https://code.jquery.com/jquery-3.6.0.min.js' integrity='sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=' crossorigin='anonymous'></script>","utf-8"))
            self.wfile.write(bytes("</head>","utf-8"))
            self.wfile.write(bytes("<body link='#0000FF' vlink='#0000FF' alink='#0000FF'>","utf-8"))
            self.wfile.write(bytes("<div id='main_content'>", "utf-8"))
            self.wfile.write(bytes("<h3><a style='color:green;' href='http://localhost:3333/1'> **********MAIN VERSION********** BACK TO MAIN **********MAIN VERSION********** </a></h3>'", "utf-8"))
            self.wfile.write(bytes("<h2><span style='color:#34495E;'>Bitcoin Address Loaded&nbsp;" + str(__class__.addr_countbtc) + "</span><span style='color:#34495E;'>      ETH Address Loaded&nbsp;" + str(__class__.addr_countETH) + "</span><span style='color:#34495E;'>    Total Bitcoin & ETH Addresses Database. Total Addresses Loaded&nbsp;***|&nbsp;" + str(__class__.addr_count) + "&nbsp;|</span></h2>", "utf-8"))
            self.wfile.write(bytes("<h2><span style='color:#34495E;'><id='information' >&nbsp;&nbsp;&nbsp;Python-WebServer for more information about Python-WebServer.py Visit" + "<a href='https://github.com/Mizogg/Python-WebServer'> Python-WebServer GitHub </a>" + " or " + "<a href='https://mizogg.co.uk/'> Mizogg Home Website </a></h2>", "utf-8")) 
            self.wfile.write(bytes("<h3><span style='color:#145A32;background-color:#f2f3f4;padding:2px;border-radius: 2px;'>Page #</span> <span id='current_page' style='color: #145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>" + str(__class__.num) + "</span> <span style='color:#145A32;'><< out of >></span> <span style='color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h3>", "utf-8"))
            self.wfile.write(bytes("<pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span>&nbsp;]&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.first)+"'>first</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.middle)+"'>middle</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.max)+"'>last</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            
            self.wfile.write(bytes("<pre>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p255)+"'>2^255</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p254)+"'>2^254</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p253)+"'>2^253</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p252)+"'>2^252</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p251)+"'>2^251</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p250)+"'>2^250</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p249)+"'>2^249</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p248)+"'>2^248</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p247)+"'>2^247</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p246)+"'>2^246</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p245)+"'>2^245</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p244)+"'>2^244</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p243)+"'>2^243</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p242)+"'>2^242</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p241)+"'>2^241</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p240)+"'>2^240</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p239)+"'>2^239</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p238)+"'>2^238</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p237)+"'>2^237</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p236)+"'>2^236</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p235)+"'>2^235</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p234)+"'>2^234</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p233)+"'>2^233</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p232)+"'>2^232</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p231)+"'>2^231</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p230)+"'>2^230</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p229)+"'>2^229</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p228)+"'>2^228</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p227)+"'>2^227</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p226)+"'>2^226</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p225)+"'>2^225</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p224)+"'>2^224</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p223)+"'>2^223</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p222)+"'>2^222</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p221)+"'>2^221</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p220)+"'>2^220</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p219)+"'>2^219</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p218)+"'>2^218</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p217)+"'>2^217</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p216)+"'>2^216</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p215)+"'>2^215</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p214)+"'>2^214</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p213)+"'>2^213</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p212)+"'>2^212</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p211)+"'>2^211</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p210)+"'>2^210</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p209)+"'>2^209</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p208)+"'>2^208</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p207)+"'>2^207</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p206)+"'>2^206</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p205)+"'>2^205</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p204)+"'>2^204</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p203)+"'>2^203</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p202)+"'>2^202</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p201)+"'>2^201</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p200)+"'>2^200</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p199)+"'>2^199</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p198)+"'>2^198</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p197)+"'>2^197</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p196)+"'>2^196</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p195)+"'>2^195</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p194)+"'>2^194</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p193)+"'>2^193</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p192)+"'>2^192</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p191)+"'>2^191</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p190)+"'>2^190</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p189)+"'>2^189</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p188)+"'>2^188</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p187)+"'>2^187</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p186)+"'>2^186</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p185)+"'>2^185</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p184)+"'>2^184</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p183)+"'>2^183</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p182)+"'>2^182</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p181)+"'>2^181</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p180)+"'>2^180</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p179)+"'>2^179</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p178)+"'>2^178</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p177)+"'>2^177</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p176)+"'>2^176</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p175)+"'>2^175</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p174)+"'>2^174</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p173)+"'>2^173</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p172)+"'>2^172</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p171)+"'>2^171</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p170)+"'>2^170</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p169)+"'>2^169</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p168)+"'>2^168</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p167)+"'>2^167</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p166)+"'>2^166</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p165)+"'>2^165</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p164)+"'>2^164</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p163)+"'>2^163</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p162)+"'>2^162</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p161)+"'>2^161</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p160)+"'>2^160</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p159)+"'>2^159</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p158)+"'>2^158</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p157)+"'>2^157</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p156)+"'>2^156</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p155)+"'>2^155</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p154)+"'>2^154</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p153)+"'>2^153</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p152)+"'>2^152</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p151)+"'>2^151</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p150)+"'>2^150</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p149)+"'>2^149</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p148)+"'>2^148</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p147)+"'>2^147</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p146)+"'>2^146</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p145)+"'>2^145</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p144)+"'>2^144</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p143)+"'>2^143</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p142)+"'>2^142</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p141)+"'>2^141</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p140)+"'>2^140</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p139)+"'>2^139</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p138)+"'>2^138</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p137)+"'>2^137</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p136)+"'>2^136</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p135)+"'>2^135</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p134)+"'>2^134</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p133)+"'>2^133</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p132)+"'>2^132</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p131)+"'>2^131</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p130)+"'>2^130</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p129)+"'>2^129</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p128)+"'>2^128</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p127)+"'>2^127</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p126)+"'>2^126</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p125)+"'>2^125</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p124)+"'>2^124</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p123)+"'>2^123</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p122)+"'>2^122</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p121)+"'>2^121</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p120)+"'>2^120</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p119)+"'>2^119</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p118)+"'>2^118</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p117)+"'>2^117</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p116)+"'>2^116</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p115)+"'>2^115</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p114)+"'>2^114</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p113)+"'>2^113</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p112)+"'>2^112</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p111)+"'>2^111</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p110)+"'>2^110</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p109)+"'>2^109</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p108)+"'>2^108</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p107)+"'>2^107</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p106)+"'>2^106</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p105)+"'>2^105</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p104)+"'>2^104</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p103)+"'>2^103</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p102)+"'>2^102</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p101)+"'>2^101</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p100)+"'>2^100</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p99)+"'>2^99</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p98)+"'>2^98</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p97)+"'>2^97</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p96)+"'>2^96</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p95)+"'>2^95</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p94)+"'>2^94</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p93)+"'>2^93</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p92)+"'>2^92</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p91)+"'>2^91</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p90)+"'>2^90</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p89)+"'>2^89</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p88)+"'>2^88</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p87)+"'>2^87</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p86)+"'>2^86</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p85)+"'>2^85</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p84)+"'>2^84</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p83)+"'>2^83</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p82)+"'>2^82</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p81)+"'>2^81</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p82)+"'>2^82</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p81)+"'>2^81</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p80)+"'>2^80</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p79)+"'>2^79</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p78)+"'>2^78</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p77)+"'>2^77</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p76)+"'>2^76</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p75)+"'>2^75</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p74)+"'>2^74</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p73)+"'>2^73</a><br><a style='color:blue;' class='ajax' page='/"+str(__class__.p72)+"'>2^72</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p71)+"'>2^71</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p70)+"'>2^70</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p69)+"'>2^69</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p68)+"'>2^68</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p67)+"'>2^67</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p66)+"'>2^66</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p65)+"'>2^65</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p64)+"'>2^64</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p63)+"'>2^63</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p62)+"'>2^62</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p61)+"'>2^61</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p60)+"'>2^60</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p59)+"'>2^59</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p58)+"'>2^58</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p57)+"'>2^57</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p56)+"'>2^56</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p55)+"'>2^55</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p54)+"'>2^54</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p53)+"'>2^53</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p52)+"'>2^52</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p51)+"'>2^51</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p50)+"'>2^50</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p49)+"'>2^49</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p48)+"'>2^48</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p47)+"'>2^47</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p46)+"'>2^46</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p45)+"'>2^45</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p44)+"'>2^44</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p43)+"'>2^43</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p42)+"'>2^42</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p41)+"'>2^41</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p40)+"'>2^40</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p39)+"'>2^39</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p38)+"'>2^38</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p37)+"'>2^37</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p36)+"'>2^36</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p35)+"'>2^35</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p34)+"'>2^34</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p33)+"'>2^33</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p32)+"'>2^32</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p31)+"'>2^31</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p30)+"'>2^30</a><br>", "utf-8"))
            self.wfile.write(bytes("<a style='color:blue;' class='ajax' page='/"+str(__class__.p29)+"'>2^29</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p28)+"'>2^28</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p27)+"'>2^27</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p26)+"'>2^26</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p25)+"'>2^25</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p24)+"'>2^24</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p23)+"'>2^23</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p22)+"'>2^22</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p21)+"'>2^21</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p20)+"'>2^20</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p19)+"'>2^19</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p18)+"'>2^18</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p17)+"'>2^17</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p16)+"'>2^16</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p15)+"'>2^15</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p14)+"'>2^14</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p13)+"'>2^13</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p12)+"'>2^12</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p11)+"'>2^11</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p10)+"'>2^10</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p9)+"'>2^9</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p8)+"'>2^8</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p7)+"'>2^7</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p6)+"'>2^6</a>", "utf-8"))
            self.wfile.write(bytes("|<a style='color:blue;' class='ajax' page='/"+str(__class__.p5)+"'>2^5</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p4)+"'>2^4</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p3)+"'>2^3</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p2)+"'>2^2</a>|<a style='color:blue;' class='ajax' page='/"+str(__class__.p1)+"'>2^1</a>", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            ###---Loop---******************************************************************
            for i in range(0,128):
                #pubkey = get_pubkey(__class__.startPrivKey)
                pub = ice.point_multiplication(__class__.startPrivKey,G).hex()
                addrU = ice.pubkey_to_address(0, False, bytes(bytearray.fromhex(pub)))
                addrC = ice.pubkey_to_address(0, True, bytes(bytearray.fromhex(pub)))
                addrS = ice.privatekey_to_address(1, True, __class__.startPrivKey) #p2sh
                addrbech32 = ice.privatekey_to_address(2, True, __class__.startPrivKey) #bech32
                addrETH = ice.privatekey_to_ETH_address(__class__.startPrivKey)[2:]
                addresses.append(addrU.strip());
                addresses.append(addrC.strip());
                addresses.append(addrS.strip());
                addresses.append(addrbech32.strip());
                addresses.append(addrETH.strip());
                self.wfile.write(bytes("<div style='background-color:#D7DBDD;text-align:center;padding:4px;margin:4px;width:98%;height:160px;'>", "utf-8"))
                self.wfile.write(bytes("<p style='text-align:left;'><span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+addrU+"'>"+addrU+"</a></span>&nbsp;&nbsp;&nbsp;<span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>C: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+addrC+"'>"+addrC+"</a></span>&nbsp;&nbsp;&nbsp;<span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>3: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+addrS+"'>"+addrS+"</a></span>&nbsp;&nbsp;&nbsp;<span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>BC1: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+addrbech32+"'>"+addrbech32+"</a></span>&nbsp;&nbsp;&nbsp;<span style='color:blue;padding:3px;font-weight:bold;font-size: 12px;'>ETH: <a target='_blank'  href='https://ethplorer.io/address/0x"+addrETH+"'>0x"+addrETH+"</a></span></p>","utf-8"))
                self.wfile.write(bytes("<p style='text-align:left;font-weight:bold;'><span style='color:#34495E;background-color:white;padding:3px;font-size:12px;'><span style='color:brown;'>DEC: </span>"+str(__class__.startPrivKey)+"</span><span style='color:#DE3163;margin-left:12px;background-color:white;padding:3px;font-size:12px;'><span style='color:brown;f'>HEX: </span>"+str(hex(__class__.startPrivKey)[2:].zfill(64))+"</span><span style='color:brown;margin-left:12px;background-color:white;padding:3px;font-size:12px;'>"+str(len(bin(__class__.startPrivKey)[2:]))+"bit</span></p>", "utf-8"))
                self.wfile.write(bytes("<p style='text-align:left;font-weight:bold;'><span style='color:brown;background-color:white;padding:3px;font-size:12px;'>"+str(bin(__class__.startPrivKey)[2:])+"</span>", "utf-8"))
                self.wfile.write(bytes("<p>"+"<span style='color:#21618C;padding:3px;font-weight:bold;font-size: 12px;'>X: "+str(int(pub[2:66],16))+"</span> "+"<span style='color:#239B56;padding:3px;font-weight:bold;font-size: 12px;'>Y: "+str(int(pub[66:],16))+"</span></p>", "utf-8"))
                self.wfile.write(bytes("<p>"+"<span style='color:#21618C;padding:3px;font-weight:bold;font-size: 12px;'>X: "+str(pub[2:66])+"</span> "+"<span style='color:#239B56;padding:3px;font-weight:bold;font-size: 12px;'>Y: "+str(pub[66:])+"</span></p>", "utf-8"))
                self.wfile.write(bytes("</div>", "utf-8"))
                if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                __class__.startPrivKey += 1
            for addr in addresses:
                if addr in __class__.bloom_filter:
                    status = 'Yes'
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"Bitcoin Address: {addr}  Found on Page# {__class__.num} \n")
                if addr in __class__.bloom_filter1:
                    status = 'Yes'
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"ETH Address: 0x{addr}  Found on Page# {__class__.num} \n")
                    if status == "Yes":
                        mixer.init()
                        mixer.music.load("success.mp3")
                        mixer.music.play()
            ###---Loop---******************************************************************
            self.wfile.write(bytes("</pre><pre class='keys'>[&nbsp;<span style='color:blue;' class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span style='color:blue;' class='ajax' page='/"+str(__class__.next)+"'>next</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            self.wfile.write(bytes("</div>", "utf-8"))
            self.wfile.write(bytes("""
            <script>
            $('.ajax').click(function() { 
                var pnum = $(this).attr('page');
                pnum = pnum.substring(1);
                $.get("http://localhost:3334/A"+pnum, function(data, status){
                    $('#main_content').html(data)
                    history.pushState({}, null, "http://localhost:3334/"+pnum); 
                })
            })
            $(function() {
                $('#up').click(function(){
                    $('html,body').animate({scrollTop:0},400);
                });
            })           
            </script>""", "utf-8"))
            self.wfile.write(bytes("<button id='up' style='float:right;margin-top:-1.8%;text-align:center;width:80px;height:30px;'>Go Up</button>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
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
