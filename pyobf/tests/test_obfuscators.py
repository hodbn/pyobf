def test_obfuscator(obf, prog, ctx):
    p_obf = obf.obfuscate(prog)

    ctx.eval(prog.code)
    ctx.eval('val1 = run_test()')
    ctx.eval(p_obf.code)
    ctx.eval('val2 = run_test()')
    assert ctx.eval('test_equals(val1, val2)')
