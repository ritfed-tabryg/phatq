#!/usr/bin/env python3

import asyncio, itertools, os
from contextlib import AsyncExitStack

preamble = r"""
(set-option :produce-models true)
(set-logic ALL)  ; TODO: do string processing in python & make all QF_BV

(define-const prefixes String "dozmarbinwansamlitsighidfidlissogdirwacsabwissibrigsoldopmodfoglidhopdardorlorhodfolrintogsilmirholpaslacrovlivdalsatlibtabhanticpidtorbolfosdotlosdilforpilramtirwintadbicdifrocwidbisdasmidloprilnardapmolsanlocnovsitnidtipsicropwitnatpanminritpodmottamtolsavposnapnopsomfinfonbanmorworsipronnorbotwicsocwatdolmagpicdavbidbaltimtasmalligsivtagpadsaldivdactansidfabtarmonranniswolmispallasdismaprabtobrollatlonnodnavfignomnibpagsopralbilhaddocridmocpacravripfaltodtiltinhapmicfanpattaclabmogsimsonpinlomrictapfirhasbosbatpochactidhavsaplindibhosdabbitbarracparloddosbortochilmactomdigfilfasmithobharmighinradmashalraglagfadtopmophabnilnosmilfopfamdatnoldinhatnacrisfotribhocnimlarfitwalrapsarnalmoslandondanladdovrivbacpollaptalpitnambonrostonfodponsovnocsorlavmatmipfip")
(define-const suffixes String "zodnecbudwessevpersutletfulpensytdurwepserwylsunrypsyxdyrnuphebpeglupdepdysputlughecryttyvsydnexlunmeplutseppesdelsulpedtemledtulmetwenbynhexfebpyldulhetmevruttylwydtepbesdexsefwycburderneppurrysrebdennutsubpetrulsynregtydsupsemwynrecmegnetsecmulnymtevwebsummutnyxrextebfushepbenmuswyxsymselrucdecwexsyrwetdylmynmesdetbetbeltuxtugmyrpelsyptermebsetdutdegtexsurfeltudnuxruxrenwytnubmedlytdusnebrumtynseglyxpunresredfunrevrefmectedrusbexlebduxrynnumpyxrygryxfeptyrtustyclegnemfermertenlusnussyltecmexpubrymtucfyllepdebbermughuttunbylsudpemdevlurdefbusbeprunmelpexdytbyttyplevmylwedducfurfexnulluclennerlexrupnedlecrydlydfenwelnydhusrelrudneshesfetdesretdunlernyrsebhulrylludremlysfynwerrycsugnysnyllyndyndemluxfedsedbecmunlyrtesmudnytbyrsenwegfyrmurtelreptegpecnelnevfes")

(define-fun syllable ((table String) (pos Int)) String
    (str.substr table (* pos 3) 3)
)

(define-fun star ((id (_ BitVec 16))) String
    (str.++
        (syllable prefixes (bv2nat ((_ extract 15 8) id)))
        (syllable suffixes (bv2nat ((_ extract 7 0) id)))
    )
)

(define-const ascii_table String "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

; warning: calling with strings >8 chars gives nonsense
(define-fun-rec str_as_u64 ((s String)) (_ BitVec 64)
    (ite (= (str.len s) 0) #x0000000000000000 (bvadd
        ;(concat #x00000000000000 (seq.nth s 0))  ; Z3 only
        ((_ int2bv 64) (str.indexof ascii_table (str.at s 0) 0))
        (bvshl (str_as_u64 (str.substr s 1 (- (str.len s) 1))) #x0000000000000008)
    ))
)

; TODO: declare consts with sequences and/or recursively
(declare-const a (_ BitVec 64))
(declare-const b (_ BitVec 64))
(declare-const c (_ BitVec 64))
(declare-const d (_ BitVec 64))
(declare-const e (_ BitVec 64))
(declare-const f (_ BitVec 64))
(declare-const g (_ BitVec 64))
(declare-const h (_ BitVec 64))
(declare-const x (_ BitVec 64))
"""

template = r"""
(define-fun hash ((name (_ BitVec 64))) (_ BitVec 16)
    ((_ extract 15 0) ({0} ({0} ({0} ({0} ({0} ({0} ({0} ({0}
        ({1} a (concat #x00000000000000 ((_ extract 7 0) name)))
        ({2} b (concat #x00000000000000 ((_ extract 15 8) name))))
        ({3} c (concat #x00000000000000 ((_ extract 23 16) name))))
        ({4} d (concat #x00000000000000 ((_ extract 31 24) name))))
        ({5} e (concat #x00000000000000 ((_ extract 39 32) name))))
        ({6} f (concat #x00000000000000 ((_ extract 47 40) name))))
        ({7} g (concat #x00000000000000 ((_ extract 55 48) name))))
        ({8} h (concat #x00000000000000 ((_ extract 63 56) name))))
        x
    ))
)

(define-fun hash_works ((i (_ BitVec 16))) Bool
    (= (hash (str_as_u64 (star i))) i)
)

(define-fun-rec validate ((i (_ BitVec 16))) Bool
    (ite (= i #x0000)
        (hash_works i)
        (and
            (hash_works i)
            (validate (bvsub i #x0001))
        )
    )
)

(assert (validate #x000f))
"""

ops = [
    "bvand",
    "bvor",
    "bvxor",
    "bvnand",
    "bvnor",
    "bvxnor",
    "bvadd",
    "bvsub",
    "bvmul",
    "bvudiv",
    "bvsdiv",
    "bvurem",
    "bvsrem",
    "bvsmod",
    "bvshl",
    "bvlshr",
    "bvashr",
]


class Solver:
    def __init__(self, iter):
        self.solver = None
        self.index = None
        self.iter = iter

    async def __aenter__(self):
        await self.spawn()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.kill()

    async def spawn(self):
        if not self.solver:
            self.solver = await asyncio.create_subprocess_exec(
                #"z3", "-in",
                "cvc4", "--incremental", "--lang", "smt",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                #stderr=asyncio.subprocess.DEVNULL,
            )
            self.solver.stdin.transport.set_write_buffer_limits(0)
            self.solver.stdin.write(preamble.encode())
            await self.solver.stdin.drain()

    async def kill(self):
        if self.solver:
            try:
                self.solver.terminate()
            except ProcessLookupError:
                pass
            await self.solver.communicate()
            self.solver = None

    async def check(self, stmt):
        self.solver.stdin.write(b"(push)\n")
        self.solver.stdin.write(stmt)
        self.solver.stdin.write(b"(check-sat)\n")
        await self.solver.stdin.drain()

        while True:
            line = await self.solver.stdout.readline()
            if line == b"unsat\n":
                self.solver.stdin.write(b"(pop)\n")
                return None
            elif line == b"sat\n" or line == b"unknown\n":
                return (
                    (await self.solver.communicate(b"(get-value (a b c d e f g h x))"))[0]
                    .decode()
                    .rstrip("\n")
                )
            elif line == b"":
                raise EOFError
            else:
                try:
                    print("unrecognized line:", line.decode().rstrip("\n"))
                except UnicodeDecodeError:
                    pass

    async def retry_on_eof(self, f):
        while True:
            try:
                return await f()
            except EOFError:
                await self.kill()
                await self.spawn()

    async def run(self):
        assert self.solver is not None

        while True:
            try:
                self.index, permutation = next(self.iter)
            except StopIteration:
                return None
            assertions = template.format(*permutation).encode()
            model = await self.retry_on_eof(lambda: self.check(assertions))
            if model:
                return model


def load_checkpoints():
    try:
        with open("checkpoints") as f:
            return set(int(line) for line in f)
    except (FileNotFoundError, ValueError):
        return set((0,))


def save_checkpoints(solvers):
    with open("checkpoints.new", "w") as f:
        for s in solvers:
            if s.index:
                print(s.index, file=f)

    os.replace("checkpoints.new", "checkpoints")


def permutations(checkpoints):
    # note: we reverse order to test most significant bits first
    for i, p in enumerate(x[::-1] for x in itertools.product(ops, repeat=9)):
        if i in checkpoints or i >= max(checkpoints):
            print(f"trying {p[0]}({', '.join(p[1:])}) (#{i})")
            yield i, p


async def main():
    p = permutations(load_checkpoints())
    cores = int(os.getenv("CORES", "0")) or len(os.sched_getaffinity(0))
    async with AsyncExitStack() as stack:
        solvers = [await stack.enter_async_context(Solver(p)) for _ in range(cores)]
        stack.callback(lambda: save_checkpoints(solvers))

        pending = [asyncio.create_task(s.run()) for s in solvers]
        stack.callback(lambda: [coro.cancel() for coro in pending])

        # done, pending = await asyncio.wait([s.run() for s in solvers], return_when=asyncio.FIRST_COMPLETED)
        for coro in asyncio.as_completed(pending):
            model = await coro
            if model:
                print("model:", model)
                break
        else:
            print("no model found")


try:
    os.nice(15)
except AttributeError:
    # on non-unix platforms os.nice() will not exist
    pass

asyncio.run(main())
