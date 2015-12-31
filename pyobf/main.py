import sys
from combiners import CascadeCombiner
from obfuscators import YUIObfuscator


YUI_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\build\yuicompressor-2.4.8.jar'
JQUERY_PATH = r'..\obfuscators\js\yuicompressor-2.4.8-leak\tests\jquery-1.6.4.js'


def main():
    o = YUIObfuscator(YUI_PATH, randomize=True)
    c = CascadeCombiner([o, o, o, o])
    with open(JQUERY_PATH, 'rb') as f:
        prog = f.read()

    print len(o.obfuscate(prog))
    print len(c.combine(prog))

    return 0


if __name__ == '__main__':
    sys.exit(main())
