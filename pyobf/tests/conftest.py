import PyV8
import pytest

from obfuscators import YUIObfuscator, ClosureObfuscator
from consts import *


@pytest.fixture(params=[YUIObfuscator(YUI_PATH),
                        YUIObfuscator(YUI_PATH, randomize=True),
                        YUIObfuscator(YUI_PATH, leak='in-code'),
                        YUIObfuscator(YUI_PATH, leak='run-time'),
                        YUIObfuscator(YUI_PATH, leak='external'),
                        ClosureObfuscator(CLOSURE_PATH),
                        ])
def obf(request):
    return request.param


@pytest.fixture(params=[(JS_FIB, JS_TEST_FIB),
                        (JS_FACT, JS_TEST_FACT),
                        ])
def prog(request, ctx):
    p_fn, t_fn = request.param
    with open(p_fn, 'rb') as f:
        p = f.read()
    with open(t_fn, 'rb') as f:
        ctx.eval(f.read())
    return p


@pytest.fixture(params=[PyV8.JSContext(),
                        ])
def ctx(request):
    c = request.param
    c.enter()
    with open(JS_TEST_EQ, 'rb') as f:
        c.eval(f.read())

    return c
