import os


_base = os.path.dirname(__file__)
_js_obf = os.path.join(_base, r'..\..\obfuscators\js')
_tests = os.path.join(_base, r'tests')

YUI_PATH = os.path.join(_js_obf, r'yuicompressor-2.4.8-leak\build\yuicompressor-2.4.8.jar')
CLOSURE_PATH = os.path.join(_js_obf, r'closure\compiler.jar')

JS_FIB = os.path.join(_tests, r'fib.js')
JS_FACT = os.path.join(_tests, r'fact.js')
JS_JQUERY = os.path.join(_js_obf, r'yuicompressor-2.4.8-leak\tests\jquery-1.6.4.js')


del _base
del os
