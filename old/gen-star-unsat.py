#!/bin/env python3
from z3 import Solver, BitVec, BitVecVal, set_param
# TODO: which of these two syntaxes is correct?
#set_param(parallel_enable=True)
set_param("parallel.enable", True)

prefixes = (
    b"dozmarbinwansamlitsighidfidlissogdirwacsabwissib"
    b"rigsoldopmodfoglidhopdardorlorhodfolrintogsilmir"
    b"holpaslacrovlivdalsatlibtabhanticpidtorbolfosdot"
    b"losdilforpilramtirwintadbicdifrocwidbisdasmidlop"
    b"rilnardapmolsanlocnovsitnidtipsicropwitnatpanmin"
    b"ritpodmottamtolsavposnapnopsomfinfonbanmorworsip"
    b"ronnorbotwicsocwatdolmagpicdavbidbaltimtasmallig"
    b"sivtagpadsaldivdactansidfabtarmonranniswolmispal"
    b"lasdismaprabtobrollatlonnodnavfignomnibpagsopral"
    b"bilhaddocridmocpacravripfaltodtiltinhapmicfanpat"
    b"taclabmogsimsonpinlomrictapfirhasbosbatpochactid"
    b"havsaplindibhosdabbitbarracparloddosbortochilmac"
    b"tomdigfilfasmithobharmighinradmashalraglagfadtop"
    b"mophabnilnosmilfopfamdatnoldinhatnacrisfotribhoc"
    b"nimlarfitwalrapsarnalmoslandondanladdovrivbacpol"
    b"laptalpitnambonrostonfodponsovnocsorlavmatmipfip"
)

suffixes = (
    b"zodnecbudwessevpersutletfulpensytdurwepserwylsun"
    b"rypsyxdyrnuphebpeglupdepdysputlughecryttyvsydnex"
    b"lunmeplutseppesdelsulpedtemledtulmetwenbynhexfeb"
    b"pyldulhetmevruttylwydtepbesdexsefwycburderneppur"
    b"rysrebdennutsubpetrulsynregtydsupsemwynrecmegnet"
    b"secmulnymtevwebsummutnyxrextebfushepbenmuswyxsym"
    b"selrucdecwexsyrwetdylmynmesdetbetbeltuxtugmyrpel"
    b"syptermebsetdutdegtexsurfeltudnuxruxrenwytnubmed"
    b"lytdusnebrumtynseglyxpunresredfunrevrefmectedrus"
    b"bexlebduxrynnumpyxrygryxfeptyrtustyclegnemfermer"
    b"tenlusnussyltecmexpubrymtucfyllepdebbermughuttun"
    b"bylsudpemdevlurdefbusbeprunmelpexdytbyttyplevmyl"
    b"wedducfurfexnulluclennerlexrupnedlecrydlydfenwel"
    b"nydhusrelrudneshesfetdesretdunlernyrsebhulryllud"
    b"remlysfynwerrycsugnysnyllyndyndemluxfedsedbecmun"
    b"lyrtesmudnytbyrsenwegfyrmurtelreptegpecnelnevfes"
)

s = Solver()

x = BitVec('x', 64)
y = BitVec('y', 64)

print("generating constraints...")

id = 0
for i in range(0, len(prefixes), 3):
    prefix = prefixes[i:i+3]
    for j in range(0, len(suffixes), 3):
        suffix = suffixes[j:j+3]
        word = (prefix+suffix).rjust(8, b'\0')  # exactly 8 bytes

        # TODO: sort type conversions for smaller numbers (u16)? would it just slow it down?
        id_bits = BitVecVal(id, 64)
        word_bits = BitVecVal(int.from_bytes(word, byteorder="little"), 64)
        #word_bits = id_bits - 10
        s.add((word_bits * x + y) % 65536 == id_bits)

        id += 1

print(s.sexpr())

# we are going to see if there is a linear equation mapping word numbers to star numbers.
print("solving...")
print("check:", s.check())
print("model:", s.model().sexpr())
