import sys
from choosers import JSMajorityChooser
from combiners import CascadeCombiner, C4OutOf3Combiner
from obfuscators import YUIObfuscator


YUI_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\build\yuicompressor-2.4.8.jar'
JQUERY_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\tests\jquery-1.6.4.js'


def main():
    o = YUIObfuscator(YUI_PATH, randomize=True)
    m = JSMajorityChooser()
    cascade = C4OutOf3Combiner(obfs=[o, o, o, o], maj=m)
    with open(JQUERY_PATH, 'rb') as f:
        prog = f.read()

    print len(o.obfuscate(prog))
    print len(cascade.combine(prog))

    return 0


if __name__ == '__main__':
    sys.exit(main())
