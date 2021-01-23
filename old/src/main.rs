#![feature(array_chunks)]

use std::{
    sync::{
        atomic::{AtomicU64, Ordering::Relaxed},
        mpsc::{self, RecvTimeoutError},
        Arc,
    },
    thread,
    time::Duration,
};
use xxhash_rust::xxh3::xxh3_64_with_seed;

const PREFIXES: &[u8; 256*3] = b"dozmarbinwansamlitsighidfidlissogdirwacsabwissibrigsoldopmodfoglidhopdardorlorhodfolrintogsilmirholpaslacrovlivdalsatlibtabhanticpidtorbolfosdotlosdilforpilramtirwintadbicdifrocwidbisdasmidloprilnardapmolsanlocnovsitnidtipsicropwitnatpanminritpodmottamtolsavposnapnopsomfinfonbanmorworsipronnorbotwicsocwatdolmagpicdavbidbaltimtasmalligsivtagpadsaldivdactansidfabtarmonranniswolmispallasdismaprabtobrollatlonnodnavfignomnibpagsopralbilhaddocridmocpacravripfaltodtiltinhapmicfanpattaclabmogsimsonpinlomrictapfirhasbosbatpochactidhavsaplindibhosdabbitbarracparloddosbortochilmactomdigfilfasmithobharmighinradmashalraglagfadtopmophabnilnosmilfopfamdatnoldinhatnacrisfotribhocnimlarfitwalrapsarnalmoslandondanladdovrivbacpollaptalpitnambonrostonfodponsovnocsorlavmatmipfip";
const SUFFIXES: &[u8; 256*3] = b"zodnecbudwessevpersutletfulpensytdurwepserwylsunrypsyxdyrnuphebpeglupdepdysputlughecryttyvsydnexlunmeplutseppesdelsulpedtemledtulmetwenbynhexfebpyldulhetmevruttylwydtepbesdexsefwycburderneppurrysrebdennutsubpetrulsynregtydsupsemwynrecmegnetsecmulnymtevwebsummutnyxrextebfushepbenmuswyxsymselrucdecwexsyrwetdylmynmesdetbetbeltuxtugmyrpelsyptermebsetdutdegtexsurfeltudnuxruxrenwytnubmedlytdusnebrumtynseglyxpunresredfunrevrefmectedrusbexlebduxrynnumpyxrygryxfeptyrtustyclegnemfermertenlusnussyltecmexpubrymtucfyllepdebbermughuttunbylsudpemdevlurdefbusbeprunmelpexdytbyttyplevmylwedducfurfexnulluclennerlexrupnedlecrydlydfenwelnydhusrelrudneshesfetdesretdunlernyrsebhulrylludremlysfynwerrycsugnysnyllyndyndemluxfedsedbecmunlyrtesmudnytbyrsenwegfyrmurtelreptegpecnelnevfes";

const UNITS: &[(u64, &str)] = &[
    (1<<40, "T"), // tera-
    (1<<30, "G"), // giga-
    (1<<20, "M"), // mega-
    (1<<10, "K"), // kilo-
];

fn brute_force_syllable(seed: Arc<AtomicU64>, step: u64) -> u64 {
    // only bother refcounts once
    let seed = seed.as_ref();

    // 2 NUL bytes, 3 prefix bytes, 3 suffix bytes
    let mut buf = [0u8; 8];

    // TODO: up to 256 is galaxies (i.e. `@p`0 is not ~dozzod),
    // so be sure to set edit distance between ~doz*** and *** to 0
    // number that should represent syllable (e.g. ~marzod = 256)
    let mut num = 0u64;

    'reseed: loop {
        for prefix in PREFIXES.array_chunks::<3>() {
            buf[2..5].copy_from_slice(prefix);
            for suffix in SUFFIXES.array_chunks::<3>() {
                buf[5..8].copy_from_slice(suffix);
                // TODO: xxhash-rust docs mention something about precomputing a seed?
                // how are seeds different from xxhash secrets?

                // it is overwhelmingly likely (255/256) the seed will need to
                // be incremented, so do it atomically here & undo if seed=num
                if xxh3_64_with_seed(&buf, seed.fetch_add(step, Relaxed)) != num {
                    num = 0;
                    continue 'reseed;
                } else {
                    seed.fetch_sub(step, Relaxed);
                }
                num += 1;
            }
        }
        
        return seed.load(Relaxed) - step;
    }
}

fn main() {
    // TODO: SIMD generation? threads may not be optimal
    // xxHash may take up available SIMD parallelism. idk
    // but would a bunch of e.g. FNV in parallel be better?

    eprint!("starting threads...");

    let (tx, rx) = mpsc::channel();

    // say there are 8 cores.
    // thread 0 will check 0, 8, 16...
    // thread 1 will check 1, 9, 18...
    // and so on, with all numbers reached
    let cpus = num_cpus::get() as u64;
    let current_seeds: Vec<Arc<AtomicU64>> = (0..cpus)
        .map(|offset| {
            let seed = Arc::new(AtomicU64::new(offset));

            let tx = tx.clone();
            let seed2 = seed.clone();
            thread::spawn(move || tx.send(
                brute_force_syllable(seed2, cpus)
            ).unwrap());

            seed
        })
        .collect();

    eprint!("\rsearching seed space...");

    let mut last_seed = 0;
    loop {
        match rx.recv_timeout(Duration::from_secs(1)) {
            Ok(seed) => {
                println!("\nfound seed {}", seed);
                return;
            }
            Err(RecvTimeoutError::Timeout) => {
                let current_seed = current_seeds.iter()
                    // downshift seeds so sum doesn't overflow with many cores
                    .map(|a| a.load(Relaxed) >> 16).sum::<u64>() / cpus;

                // total progress is average of each core's
                // new max seed is also downshifted
                let progress = current_seed as f64 / (u64::MAX >> 16) as f64;

                let per_second = (current_seed - last_seed) << 16;
                let (divisor, prefix) = UNITS.iter().copied().find(|(div, _)| per_second >= *div).unwrap_or((1, ""));

                eprint!(
                    "\rsearching seed space... {:.3}% complete ({:03.3} {}seeds/s)",
                    progress * 100.0, per_second as f64 / divisor as f64, prefix,
                    
                );
                
                last_seed = current_seed;
            }
            Err(RecvTimeoutError::Disconnected) => panic!(
                "channels disconnected unexpectedly (current progress: {:?})",
                current_seeds
                    .iter()
                    .map(|a| a.load(Relaxed))
                    .collect::<Vec<_>>()
            ),
        }
    }
}
