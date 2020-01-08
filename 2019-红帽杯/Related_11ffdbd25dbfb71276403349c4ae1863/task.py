#!/usr/bin/env python2
from Crypto.Util import number
from secret import flag

assert len(flag) < 48


class PRNG(object):
    def __init__(self, key):
        super(PRNG, self).__init__()
        self.key = key
        self.e = 17
        self.N = number.getPrime(1024) * number.getPrime(1024)
        print self.N
        self.state = []

    def pad(self, msg, length):
        l = len(msg)
        return msg + chr(length - l) * (length - l)

    def enc(self, m):
        return pow(m, self.e, self.N)

    def gen(self, l):
        if len(self.key) != 48:
            self.key = self.pad(self.key, 48)
        if len(self.state) != 3:
            m = number.bytes_to_long(self.key)
            self.state = [ ( m >> (128*i) ) & (2**128 - 1) for i in range(3) ]
            print sum(self.state)
        O = []
        for _ in range(l):
            s0, s1, s2 = self.state
            s3 = (65537*s0 - 66666*s1 + 12345*s2) % self.N
            self.state = [s1, s2, s3]
            O.append( self.enc(s0) )
        return O



challenge = PRNG(flag)
print challenge.gen(4)

# 16084923760264169099484353317952979348361855860935256157402027983349457021767614332173154044206967015252105109115289920685657394517879177103414348487477378025259589760996270909325371731433876289897874303733424115117776042592359041482059737708721396118254756778152435821692154824236881182156000806958403005506732891823555324800528934757672719379501318525189471726279397236710401497352477683714139039769105043411654493442696289499967521222951945823233371845110807469944602345293068346574630273539870116158817556523565199093874587097230314166365220290730937380983228599414137341498205967870181640370981402627360812251649
# 280513550110197745829890567436265496990
# [10607235400098586699994392584841806592000660816191315008947917773605476365884572056544621466807636237415893192966935651590312237598366247520986667580174438232591692369894702423377081613821241343307094343575042030793564118302488401888197517625333923710172738913771484628557310164974384462856047065486913046647133386246976457961265115349103039946802386897315176633274295410371986422039106745216230401123542863714301114753239888820442112538285194875243192862692290859625788686421276234445677411280606266052059579743874849594812733193363406594409214632722438592376518310171297234081555028727538951934761726878443311071990L, 2665348075952836665455323350891842781938471372943896177948046901127648217780657532963063228780230203325378931053293617434754585479452556620021360669764370971665619743473463613391689402725053682169256850873752706252379747752552015341379702582040497607180172854652311649467878714425698676142212588380080361100526614423533767196749274741380258842904968147508033091819979042560336703564128279527380969385330845759998657540777339113519036552454829323666242269607225156846084705957131127720351868483375138773025602253783595007177712673092409157674720974653789039702431795168654387038080256838321255342848782705785524911705L, 4881225713895414151830685259288740981424662400248897086365166643853409947818654509692299250960938511400178276416929668757746679501254041354795468626916196040017280791985239849062273782179873724736552198083211250561192059448730545500442981534768431023858984817288359193663144417753847196868565476919041282010484259630583394963580424358743754334956833598351424515229883148081492471874232555456362089023976929766530371320876651940855297249474438564801349160584279330339012464716197806221216765180154233949297999618011342678854874769762792918534509941727751433687189532019000334342211838299512315478903418642056097679717L, 12534425973458061280573013378054836248888335198966169076118474130362704619767247747943108676623695140384169222126709673116428645230760767457471129655666350250668322899568073246541508846438634287249068036901665547893655280767196856844375628177381351311387888843222307448227990714678010579304867547658489581752103225573979257011139236972130825730306713287107974773306076630024338081124142200612113688850435053038506912906079973403207309246156198371852177700671999937121772761984895354214794816482109585409321157303512805923676416467315573673701738450569247679912197730245013539724493780184952584813891739837153776754362L]





