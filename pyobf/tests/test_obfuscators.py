def test_yui_normal(obf, prog, ctx):
    p_obf = obf.obfuscate(prog)

    ctx.eval(prog)
    ctx.eval('val1 = test_fib()')
    ctx.eval(p_obf)
    ctx.eval('val2 = test_fib()')
    assert ctx.eval('test_equals(val1, val2)')
