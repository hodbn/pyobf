import sys
import time

from pyobf.choosers import JSMajorityChooser
from pyobf.combiners import C3OutOf4Combiner, CascadeCombiner
from pyobf.consts import *
from pyobf.languages import *
from pyobf.obfuscators import YUIObfuscator, ClosureObfuscator
from pyobf.program import Program


def profile_obfuscator(o, p):
    print '%s:' % (o, ),
    s = time.time()
    out = o.obfuscate(p)
    e = time.time()
    print 'size=%d,time=%3.3f' % (len(out.code), e - s)
profile_combiner = profile_obfuscator


def main():
    jquery = Program('jquery', LANG_JS, JS_JQUERY)
    fact = Program('fact', LANG_JS, JS_FACT)

    o_norm = YUIObfuscator(YUI_PATH)
    o_rand = YUIObfuscator(YUI_PATH, randomize=True)
    o_closure = ClosureObfuscator(CLOSURE_PATH)

    o_leak_in_code = YUIObfuscator(YUI_PATH, leak='in-code')
    o_leak_run_time = YUIObfuscator(YUI_PATH, leak='run-time')
    o_leak_external = YUIObfuscator(YUI_PATH, leak='external')

    c_norm_rand_closure = CascadeCombiner(obfs=[o_norm, o_rand, o_closure])
    c_norm_rand_closure_in_code = CascadeCombiner(obfs=[o_norm, o_rand,
                                                        o_closure,
                                                        o_leak_in_code])

    # profile normal obfuscators
    # profile_obfuscator(o_norm, jquery)
    # profile_obfuscator(o_rand, jquery)
    # profile_obfuscator(o_closure, jquery)

    # profile malicious obfuscators
    # profile_obfuscator(o_leak_in_code, jquery)
    # profile_obfuscator(o_leak_run_time, jquery)
    # profile_obfuscator(o_leak_external, jquery)

    # profile cascade combiners
    # profile_combiner(c_norm_rand_closure, jquery)
    # profile_combiner(c_norm_rand_closure_in_code, jquery)

    # profile 3-out-of-4 combiners
    m = JSMajorityChooser()
    f_norm_rand_closure_run_time = C3OutOf4Combiner(
        obfs=[o_norm, o_rand, o_closure, o_leak_run_time], maj=m)
    f_norm_rand_closure_in_code = C3OutOf4Combiner(
        obfs=[o_norm, o_rand, o_closure, o_leak_in_code], maj=m)
    # profile_combiner(f_norm_rand_closure_run_time, jquery)
    # profile_combiner(f_norm_rand_closure_in_code, jquery)
    profile_combiner(f_norm_rand_closure_in_code, fact)

    return 0


if __name__ == '__main__':
    sys.exit(main())
