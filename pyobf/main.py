import sys
import time
from choosers import JSMajorityChooser
from combiners import C3OutOf4Combiner, CascadeCombiner
from languages import *
from obfuscators import YUIObfuscator, ClosureObfuscator
from program import Program


YUI_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\build\yuicompressor-2.4.8.jar'
CLOSURE_PATH = r'..\obfuscators\js\closure\compiler.jar'
JQUERY_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\tests\jquery-1.6.4.js'


def profile_obfuscator(o, p):
    print '%s:' % (o, ),
    s = time.time()
    out = o.obfuscate(p)
    e = time.time()
    print 'size=%d,time=%3.3f' % (len(out.code), e - s)


def profile_combiner(c, p):
    print '%s:' % (c, ),
    s = time.time()
    out = c.combine(p)
    e = time.time()
    print 'size=%d,time=%3.3f' % (len(out.code), e - s)


def main():
    JS_FACT = 'tests\\fact.js'
    JS_TEST_FACT = 'tests\\test_fact.js'
    prog = Program('fact', LANG_JS, JS_FACT, JS_TEST_FACT)
    comb = C3OutOf4Combiner([
                                YUIObfuscator(YUI_PATH, randomize=True),
                                YUIObfuscator(YUI_PATH, randomize=True),
                                YUIObfuscator(YUI_PATH, leak='in-code'),
                                ClosureObfuscator(CLOSURE_PATH),
                            ], maj=JSMajorityChooser())
    p_obf = comb.combine(prog)

    import PyV8
    ctx = PyV8.JSContext()
    ctx.enter()
    JS_TEST_EQ = 'tests\\test_equals.js'
    with open(JS_TEST_EQ, 'rb') as f:
        ctx.eval(f.read())
    ctx.eval(prog.test)
    ctx.eval(prog.code)
    ctx.eval('val1 = run_test()')
    ctx.eval(p_obf.code)
    ctx.eval('val2 = run_test()')
    assert ctx.eval('test_equals(val1, val2)')

    return
    jquery = Program('jquery', LANG_JS, JQUERY_PATH)

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

    # profile 3-out-of-4 combiners
    return
    m = JSMajorityChooser()

    return 0


if __name__ == '__main__':
    sys.exit(main())
