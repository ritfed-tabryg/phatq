#!/bin/sh

cp -v ../x_u64.sat ../x_u64_cvc4.sat .

/usr/bin/time -p z3 x_u64.sat 2>&1 | tee z3_x_u64.log &
/usr/bin/time -p z3 x_u64_cvc4.sat 2>&1 | tee z3_x_u64_cvc4.log &
/usr/bin/time -p cvc4 --lang smt x_u64.sat 2>&1 | tee cvc4_x_u64.log &
/usr/bin/time -p cvc4 --lang smt x_u64_cvc4.sat 2>&1 | tee cvc4_x_u64_cvc4.log &

wait

