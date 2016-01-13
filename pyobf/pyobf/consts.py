import os


_base = os.path.dirname(__file__)
_js_obf = os.path.join(_base, r'..\..\obfuscators\js')
_tests = os.path.join(_base, r'tests')

YUI_PATH = os.path.join(_js_obf, r'yuicompressor-2.4.8-leak\build' +
                                 '\yuicompressor-2.4.8.jar')
CLOSURE_PATH = os.path.join(_js_obf, r'closure\compiler.jar')
PACKER_PATH = os.path.join(_js_obf, r'packer\jsPacker.pl')

JS_FIB = os.path.join(_tests, r'fib.js')
JS_FACT = os.path.join(_tests, r'fact.js')
JS_JQUERY = os.path.join(_tests, r'jquery-1.6.4.js')
JS_ANGULAR = os.path.join(_tests, r'angular-1.4.5.js')
JS_DOJO = os.path.join(_tests, r'dojo.js.uncompressed.js')
JS_HIGHLIGHT = os.path.join(_tests, r'highlight.js')
JS_RAPHAEL = os.path.join(_tests, r'raphael.js')
JS_SWIG = os.path.join(_tests, r'swig.js')
JS_CHART = os.path.join(_tests, r'Chart.js')
JS_COOKIES = os.path.join(_tests, r'cookies.js')
JS_JCAROUSEL = os.path.join(_tests, r'jquery.jcarousel.js')
JS_BACKBONE = os.path.join(_tests, r'backbone.js')
JS_EPOCH = os.path.join(_tests, r'epoch.js')
JS_PHYSICSJS = os.path.join(_tests, r'physicsjs.js')
JS_VIDEOJS = os.path.join(_tests, r'video.js')


del _base
del os
