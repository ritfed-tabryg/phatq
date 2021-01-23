#!/bin/env python3
import operator
from itertools import product
from functools import reduce

import z3
from z3 import Solver, BitVec, BitVecVal, set_param, unsat
# TODO: which of these two syntaxes is correct?
#set_param(parallel_enable=True)
#set_param("parallel.enable", True)

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

individual_ops = (
    operator.add,
    operator.mul,
    #operator.sub,
    operator.or_,
    operator.and_,
    operator.xor,
    operator.truediv,  #operator.floordiv,
    #inv(operator.div),
    operator.mod,
    # lt, gt, etc.
    operator.rshift,
    operator.lshift,
    #rev(operator.rshift),
    #rev(operator.lshift),
    z3.UDiv,
    z3.URem,
    # TODO signed stuff
    z3.LShR,
    z3.RotateLeft,
    z3.RotateRight,
)

sum_ops = (
    #operator.add,  # add already exhaustively checked
    #TODO operator.mul,
    #operator.sub,
    operator.or_,
    operator.and_,
    operator.xor,
    operator.truediv,  #operator.floordiv,
    #inv(operator.div),
    operator.mod,
    # lt, gt, etc.
    operator.rshift,
    operator.lshift,
    #rev(operator.rshift),
    #rev(operator.lshift),
    z3.UDiv,
    z3.URem,
    # TODO signed stuff
    z3.LShR,
    z3.RotateLeft,
    z3.RotateRight,
)

#suffixes = "".join(sorted(suffixes[j:j+3] for j in range(0, len(suffixes), 3)))

for width, sum, ops in product([8, 16, 32, 64], sum_ops, product(individual_ops, repeat=3)):
    s = Solver()

    x = BitVec('x', width)
    y = BitVec('y', width)
    z = BitVec('z', width)
    b = BitVec('bx', width)

    print("generating constraints...", width, sum, ops)

    id = 0
    #for i in range(0, len(prefixes), 3):
    #    prefix = prefixes[i:i+3]
    for j in range(0, len(suffixes), 3):
        id_b = BitVecVal(id, width)
        chars = [BitVecVal(ord(char), width) for char in suffixes[j:j+3]]
        chars_transformed = (o(c,x) for o,c,x in zip(ops, chars, (x,y,z)))
        s.add(reduce(sum, chars_transformed) + b % 256 == id_b)

        id += 1


    # we are going to see if there is a linear equation mapping word numbers to star numbers.
    print("solving...")
    if s.check() != unsat:
        print("solved!")
        print("constraints:", s.sexpr())
        print("model:", s.model(), s.model().sexpr())
        sys.exit()

print("unsat")
