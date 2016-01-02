from ..choosers import JSMajorityChooser
from ..combiners import CascadeCombiner, C3OutOf4Combiner
from ..obfuscators import YUIObfuscator, ClosureObfuscator
from ..consts import *


def test_cascade_combiner(prog, ctx):
    comb = CascadeCombiner([
        YUIObfuscator(YUI_PATH, randomize=True),
        YUIObfuscator(YUI_PATH, randomize=True),
        YUIObfuscator(YUI_PATH, leak='in-code'),
        ClosureObfuscator(CLOSURE_PATH),
    ])
    p_obf = comb.combine(prog)

    ctx.eval(prog.code)
    ctx.eval('val1 = run_test()')
    ctx.eval(p_obf.code)
    ctx.eval('val2 = run_test()')
    assert ctx.eval('test_equals(val1, val2)')


def test_3outof4_combiner(prog, ctx):
    comb = C3OutOf4Combiner([
        YUIObfuscator(YUI_PATH, randomize=True),
        YUIObfuscator(YUI_PATH, randomize=True),
        YUIObfuscator(YUI_PATH, leak='in-code'),
        ClosureObfuscator(CLOSURE_PATH),
    ], maj=JSMajorityChooser())
    p_obf = comb.combine(prog)

    ctx.eval(prog.code)
    ctx.eval('val1 = run_test()')
    ctx.eval(p_obf.code)
    ctx.eval('val2 = run_test()')
    assert ctx.eval('test_equals(val1, val2)')
