#!/usr/bin/env python
import gmpy2
n = 966808932627497190635859236054960349099463975227350564265384373280336699853387254070662881265937565163000758606154308757944030571837175048514574473061401566330836334647176655282619268592560172726526643074499534129878217409046045533656897050117438496357231575999185527675071002803951800635220029015932007465117818739948903750200830856115668691007706836952244842719419452946259275251773298338162389930518838272704908887016474007051397194588396039111216708866214614779627566959335170676055025850932631053641576566165694121420546081043285806783239296799795655191121966377590175780618944910532816988143056757054052679968538901460893571204904394975714081055455240523895653305315517745729334114549756695334171142876080477105070409544777981602152762154610738540163796164295222810243309051503090866674634440359226192530724635477051576515179864461174911975667162597286769079380660782647952944808596310476973939156187472076952935728249061137481887589103973591082872988641958270285169650803792395556363304056290077801453980822097583574309682935697260204862756923865556397686696854239564541407185709940107806536773160263764483443859425726953142964148216209968437587044617613518058779287167853349364533716458676066734216877566181514607693882375533
p = 31093551302922880999883020803665536616272147022877428745314830867519351013248914244880101094365815998050115415308439610066700139164376274980650005150267949853671653233491784289493988946869396093730966325659249796545878080119206283512342980854475734097108975670778836003822789405498941374798016753689377992355122774401780930185598458240894362246194248623911382284169677595864501475308194644140602272961699230282993020507668939980205079239221924230430230318076991507619960330144745307022538024878444458717587446601559546292026245318907293584609320115374632235270795633933755350928537598242214216674496409625928797450473
q = 31093551302922880999883020803665536616272147022877428745314830867519351013248914244880101094365815998050115415308439610066700139164376274980650005150267949853671653233491784289493988946869396093730966325659249796545878080119206283512342980854475734097108975670778836003822789405498941374798016753689377992355122774401780930185598458240894362246194248623911382284169677595864501475308194644140602272961699230282993020507668939980205079239221924230430230318076991507619960330144745307022538024878444458717587446601559546292026245318907293584609320115374632235270795633933755350928537598242214216674496409625928997877221
e = 65537
c = 4358930716870674037221294954990256976127837498632782405926543237648348488202197299071034993102740961537044116306592993097510118103482077045070833809447253574312938341147811984859083673340135238957393842225551730399442391814665402997409105337683561359777434952743651340747638996726944041389454189517534597148203211277250748613023506804560614852075946744634395040927673501849056316035725876327300521963716840462227151921190095670236624051265023248582870751028616352962089291688023212642021242321013327752135458749182579732621375391221209242118366785227716665188442978061948063186317930057611280197149445900394021224173437608030611776061788993125143507939645841691617175110531258032955419588817733884465897620291246413565219066332879296230147671868274509687577406965784242458583724361043786488756723655898389814457335895199199400073835290719538541292146037101193259457600706003068629724781609635387686836222506151191500259467414494759164360324954586698536318237025291857482207675708992483992599821901201183150965171982008035737378518347997205169112768597731951432393011337267382655378403211569592542381267706984334887838614513103636078561179830289718587181126305323126943847721498175451692567065276196281626998119175002712012345218105
d = gmpy2.invert(e, (p - 1) * (q - 1))
print d
m = gmpy2.powmod(c, d, n)
print '{:x}'.format(m).decode('hex')
