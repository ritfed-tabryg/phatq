#!/bin/env python3
from itertools import product
from functools import reduce
import operator
import string
import sys

from z3 import Solver, BitVec, BitVecVal, set_param, unsat
import z3

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

# TODO: multiprocessing for all cores?
for width in [16, 32, 64]:
    print(f"generating {width}-bit wordlist...")

    words = [(BitVecVal(i, width), s) for i, s in enumerate(
        [BitVecVal(ord(x), width) for x in a] for a in map("".join, product(*(
            (a[i:i+3] for i in range(0, len(a), 3)) for a in (prefixes, suffixes)
        )))
    )]

    for sum, ops in product(sum_ops, product(individual_ops, repeat=len(words[0][1]))):
        print(f"generating constraints... {width} {sum}{ops}")

        s = Solver()

        variables = [BitVec(name, width) for _, name in zip(words[0][1], string.ascii_lowercase[:23])]
        x = BitVec('x', width)


        for id, word in words:
            s.add(reduce(sum, (o(c, x) for o, c, x in zip(ops, word, variables))) + x % 65536 == id)

        # we are going to see if there is a linear equation mapping word numbers to star numbers.
        print("solving...")
        if s.check() != unsat:
            print("solved!")
            print("constraints:", s.sexpr())
            print("model:", s.model(), s.model().sexpr())
            sys.exit()

print("unsat")
