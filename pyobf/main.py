import sys
import time

from pyobf.choosers import JSMajorityChooser
from pyobf.combiners import C3OutOf4Combiner, CascadeCombiner
from pyobf.consts import *
from pyobf.languages import *
from pyobf.obfuscators import YUIObfuscator, ClosureObfuscator
from pyobf.program import Program


REPEAT = 10


def _avg(l):
    assert len(l) > 0
    return float(sum(l)) / len(l)


def profile_obfuscator(o, p):
    times = []
    lens = []
    for _ in xrange(REPEAT):
        s = time.time()
        out = o.obfuscate(p)
        e = time.time()
        times.append(e - s)
        lens.append(len(out.code))
    return _avg(lens), (_avg(lens) / float(len(p.code))) * 100., _avg(times)


def profile_obfuscators(obfs, progs):
    for o in obfs:
        for p in progs:
            print '%s on %s:' % (o, p),
            s, p, t = profile_obfuscator(o, p)
            print 'size = %3.3f, pct = %3.2f%%, time = %3.3f' % (s, p, t)


profile_combiners = profile_obfuscators


def main():
    progs = [
        Program('jquery', LANG_JS, JS_JQUERY),
        # Program('fact', LANG_JS, JS_FACT),
        Program('angular', LANG_JS, JS_ANGULAR),
        # Program('fib', LANG_JS, JS_FIB),
        Program('dojo', LANG_JS, JS_DOJO),
        # Program('popcorn', LANG_JS, JS_POPCORN),
        Program('swig', LANG_JS, JS_SWIG),
        Program('chart', LANG_JS, JS_CHART),
        Program('cookies', LANG_JS, JS_COOKIES),
        # Program('modernizr', LANG_JS, JS_MODERNIZR),
        Program('jcarousel', LANG_JS, JS_JCAROUSEL),
        # Program('hammer', LANG_JS, JS_HAMMER),
        Program('backbone', LANG_JS, JS_BACKBONE),
        Program('epoch', LANG_JS, JS_EPOCH),
        Program('physicsjs', LANG_JS, JS_PHYSICSJS),
        # Program('soundjs', LANG_JS, JS_SOUNDJS),
        Program('videojs', LANG_JS, JS_VIDEOJS),
        Program('raphael', LANG_JS, JS_RAPHAEL),
        Program('highlight', LANG_JS, JS_HIGHLIGHT),
        # Program('jqueryui', LANG_JS, JS_JQUERY_UI),
        # Program('mootools', LANG_JS, JS_MOOTOOLS),
        # Program('underscore', LANG_JS, JS_UNDERSCORE),
    ]

    o_norm = YUIObfuscator(YUI_PATH)
    o_rand = YUIObfuscator(YUI_PATH, randomize=True)
    o_closure = ClosureObfuscator(CLOSURE_PATH)

    """
    o_leak_in_code = YUIObfuscator(YUI_PATH, leak='in-code')
    o_leak_run_time = YUIObfuscator(YUI_PATH, leak='run-time')
    o_leak_external = YUIObfuscator(YUI_PATH, leak='external')
    """

    c_norm_rand_closure = CascadeCombiner(obfs=[o_norm, o_rand, o_closure])
    c_norm_rand_closure_norm = CascadeCombiner(obfs=[o_norm, o_rand, o_closure,
                                                     o_norm])

    # profile normal obfuscators
    profile_obfuscators([o_norm, o_rand, o_closure],
                        progs)

    # profile malicious obfuscators
    """
    profile_obfuscators([o_leak_in_code, o_leak_run_time, o_leak_external],
                        progs)
    """

    # profile cascade combiners
    profile_combiners([c_norm_rand_closure, c_norm_rand_closure_norm], progs)

    # profile 3-out-of-4 combiners
    m = JSMajorityChooser()
    f_norm_rand_closure_norm = C3OutOf4Combiner(
        obfs=[o_norm, o_rand, o_closure, o_norm], maj=m)
    f_closure_rand_closure_norm = C3OutOf4Combiner(
        obfs=[o_closure, o_rand, o_closure, o_norm], maj=m)
    profile_combiners([f_norm_rand_closure_norm, f_closure_rand_closure_norm],
                      progs)

    return 0


if __name__ == '__main__':
    sys.exit(main())
