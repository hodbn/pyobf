import PyV8
import pytest

from languages import *
from obfuscators import YUIObfuscator, ClosureObfuscator
from consts import *
from program import Program


@pytest.fixture(params=[YUIObfuscator(YUI_PATH),
                        YUIObfuscator(YUI_PATH, randomize=True),
                        YUIObfuscator(YUI_PATH, leak='in-code'),
                        YUIObfuscator(YUI_PATH, leak='run-time'),
                        YUIObfuscator(YUI_PATH, leak='external'),
                        ClosureObfuscator(CLOSURE_PATH),
                        ])
def obf(request):
    return request.param


@pytest.fixture(params=[Program('fib', LANG_JS, JS_FIB, JS_TEST_FIB),
                        Program('fact', LANG_JS, JS_FACT, JS_TEST_FACT),
                        ])
def prog(request, ctx):
    p = request.param
    ctx.eval(p.test)
    return p


@pytest.fixture(params=[PyV8.JSContext(),
                        ])
def ctx(request):
    c = request.param
    c.enter()
    with open(JS_TEST_EQ, 'rb') as f:
        c.eval(f.read())

    return c
