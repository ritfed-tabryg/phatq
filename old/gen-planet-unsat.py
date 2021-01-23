#!/bin/env python3
from z3 import Solver, BitVec, BitVecVal, LShR, set_param, unsat
# TODO: which of these two syntaxes is correct?
#set_param(parallel_enable=True)
set_param("parallel.enable", True)

prefixes = (
    "dozmarbinwansamlitsighidfidlissogdirwacsabwissib"
    "rigsoldopmodfoglidhopdardorlorhodfolrintogsilmir"
    "holpaslacrovlivdalsatlibtabhanticpidtorbolfosdot"
    "losdilforpilramtirwintadbicdifrocwidbisdasmidlop"
    "rilnardapmolsanlocnovsitnidtipsicropwitnatpanmin"
    "ritpodmottamtolsavposnapnopsomfinfonbanmorworsip"
    "ronnorbotwicsocwatdolmagpicdavbidbaltimtasmallig"
    "sivtagpadsaldivdactansidfabtarmonranniswolmispal"
    "lasdismaprabtobrollatlonnodnavfignomnibpagsopral"
    "bilhaddocridmocpacravripfaltodtiltinhapmicfanpat"
    "taclabmogsimsonpinlomrictapfirhasbosbatpochactid"
    "havsaplindibhosdabbitbarracparloddosbortochilmac"
    "tomdigfilfasmithobharmighinradmashalraglagfadtop"
    "mophabnilnosmilfopfamdatnoldinhatnacrisfotribhoc"
    "nimlarfitwalrapsarnalmoslandondanladdovrivbacpol"
    "laptalpitnambonrostonfodponsovnocsorlavmatmipfip"
)

suffixes = (
    "zodnecbudwessevpersutletfulpensytdurwepserwylsun"
    "rypsyxdyrnuphebpeglupdepdysputlughecryttyvsydnex"
    "lunmeplutseppesdelsulpedtemledtulmetwenbynhexfeb"
    "pyldulhetmevruttylwydtepbesdexsefwycburderneppur"
    "rysrebdennutsubpetrulsynregtydsupsemwynrecmegnet"
    "secmulnymtevwebsummutnyxrextebfushepbenmuswyxsym"
    "selrucdecwexsyrwetdylmynmesdetbetbeltuxtugmyrpel"
    "syptermebsetdutdegtexsurfeltudnuxruxrenwytnubmed"
    "lytdusnebrumtynseglyxpunresredfunrevrefmectedrus"
    "bexlebduxrynnumpyxrygryxfeptyrtustyclegnemfermer"
    "tenlusnussyltecmexpubrymtucfyllepdebbermughuttun"
    "bylsudpemdevlurdefbusbeprunmelpexdytbyttyplevmyl"
    "wedducfurfexnulluclennerlexrupnedlecrydlydfenwel"
    "nydhusrelrudneshesfetdesretdunlernyrsebhulryllud"
    "remlysfynwerrycsugnysnyllyndyndemluxfedsedbecmun"
    "lyrtesmudnytbyrsenwegfyrmurtelreptegpecnelnevfes"
)

for WIDTH in [8, 16, 32, 64]:
    s = Solver()

    x = BitVec('x', WIDTH)
    y = BitVec('y', WIDTH)
    z = BitVec('z', WIDTH)
    b = BitVec('bx', WIDTH)

    print("generating constraints...")

    from itertools import *
    import string

    id = 0
    #for suffix in product(*repeat(string.ascii_lowercase, 3)):
    #for i in range(0, len(prefixes), 3):
    #    prefix = prefixes[i:i+3]
    for j in range(0, 3*2, 3):
        id_b = BitVecVal(id, WIDTH)
        chars = [BitVecVal(ord(char), WIDTH) for char in suffixes[j:j+3]]
        #s.add(sum(map(mul, zip(chars, (x,y,z))) + b % 65536 == id_b)
        s.add(sum(m*x for m,x in zip((x,y,z), chars)) + b % 256 == id_b)

        id += 1


    # we are going to see if there is a linear equation mapping word numbers to star numbers.
    print("solving...")
    if s.check() != unsat:
        print("solved!")
        print("constraints:", s.sexpr())
        print("model:", s.model(), s.model().sexpr())
        sys.exit()

print("unsat")
