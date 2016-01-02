import os


_base = os.path.dirname(__file__)
JS_TEST_EQ = os.path.join(_base, r'test_equals.js')

JS_TEST_FIB = os.path.join(_base, r'test_fib.js')
JS_TEST_FACT = os.path.join(_base, r'test_fact.js')


del _base
del os