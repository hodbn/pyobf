import sys
import time
from choosers import JSMajorityChooser
from combiners import C4OutOf3Combiner
from obfuscators import YUIObfuscator


YUI_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\build\yuicompressor-2.4.8.jar'
JQUERY_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\tests\jquery-1.6.4.js'


def profile_obfuscator(n, o, p):
    print '%s:' % (n, ),
    s = time.time()
    out = o.obfuscate(p)
    e = time.time()
    print 'size=%d,time=%3.3f' % (len(out), e - s)


def main():
    with open(JQUERY_PATH, 'rb') as f:
        jquery = f.read()

    o_normal = YUIObfuscator(YUI_PATH)
    o_rand = YUIObfuscator(YUI_PATH, randomize=True)
    o_leak_in_code = YUIObfuscator(YUI_PATH, leak='in-code')
    o_leak_run_time = YUIObfuscator(YUI_PATH, leak='run-time')
    o_leak_external = YUIObfuscator(YUI_PATH, leak='external')

    # profile normal obfuscator
    profile_obfuscator('Normal YUI', o_normal, jquery)
    profile_obfuscator('Normal YUI (Randomized)', o_rand, jquery)
    profile_obfuscator('Malicious YUI (In-code)', o_leak_in_code, jquery)
    profile_obfuscator('Malicious YUI (Run-time)', o_leak_run_time, jquery)
    profile_obfuscator('Malicious YUI (External)', o_leak_external, jquery)
    return
    m = JSMajorityChooser()
    cascade = C4OutOf3Combiner(obfs=[o, o, o, o], maj=m)

    print len(o.obfuscate(jquery))
    print len(cascade.combine(jquery))

    return 0


if __name__ == '__main__':
    sys.exit(main())
