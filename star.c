#include <inttypes.h>
#include <stdio.h>

const uint64_t a = 2008855980444497303;
const uint64_t b = 2325138028067525836;
const uint64_t c = 8407072421076875978;
const uint64_t d = 10219333622835820130;
const uint64_t e = 15784341262116914227;
const uint64_t f = 3555825001007892841;
const uint64_t g = 918594726993000814;
const uint64_t h = 9745709350640736890;
const uint64_t x = 14125482616912420471;

// expects 7-byte string e.g. "~marzod"
uint16_t star(char *name) {
    return (
        name[1] * a + name[2] * b + name[3] * c +
        name[4] * d + name[5] * e + name[6] * f + x
    );
}

int main(int argc, char **argv) {
    if (argc < 2) {
        puts("usage: star ~doznec");
        return 1;
    }

    printf("`@u`%s = %" PRIu16 "\n", argv[1], star(argv[1]));
}
