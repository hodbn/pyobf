import sys
import time
from choosers import JSMajorityChooser
from combiners import C4OutOf3Combiner, CascadeCombiner
from obfuscators import YUIObfuscator, ClosureObfuscator


YUI_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\build\yuicompressor-2.4.8.jar'
CLOSURE_PATH = r'..\obfuscators\js\closure\compiler.jar'
JQUERY_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\tests\jquery-1.6.4.js'


def profile_obfuscator(o, p):
    print '%s:' % (o, ),
    s = time.time()
    out = o.obfuscate(p)
    e = time.time()
    print 'size=%d,time=%3.3f' % (len(out), e - s)
profile_combiner = profile_obfuscator


def main():
    with open(JQUERY_PATH, 'rb') as f:
        jquery = f.read()

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
    profile_obfuscator(o_norm, jquery)
    profile_obfuscator(o_rand, jquery)
    profile_obfuscator(o_closure, jquery)

    # profile malicious obfuscators
    profile_obfuscator(o_leak_in_code, jquery)
    profile_obfuscator(o_leak_run_time, jquery)
    profile_obfuscator(o_leak_external, jquery)

    # profile cascade combiners
    profile_combiner(c_norm_rand_closure, jquery)
    profile_combiner(c_norm_rand_closure_in_code, jquery)
    return
    m = JSMajorityChooser()
    cascade = C4OutOf3Combiner(obfs=[o, o, o, o], maj=m)

    print len(o.obfuscate(jquery))
    print len(cascade.combine(jquery))

    return 0


if __name__ == '__main__':
    sys.exit(main())
