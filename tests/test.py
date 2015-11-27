import os
import sys
import subprocess

PROJECT_DIR = r'..\yuicompressor-2.4.8'
TESTS_DIR = r'tests'

JQUERY_MIN_FN = r'jquery-1.6.4.js.min'
JQUERY_FN = r'jquery-1.6.4.js'
JQUERY_PATH = os.path.join(TESTS_DIR, JQUERY_FN)
JQUERY_MIN_PATH = os.path.join(TESTS_DIR, JQUERY_MIN_FN)

FA_MIN_FN = r'_function_add.js.min'
FA_FN = r'_function_add.js'
FA_PATH = os.path.join(TESTS_DIR, FA_FN)
FA_MIN_PATH = os.path.join(TESTS_DIR, FA_MIN_FN)


KEY_PATH = os.path.join(TESTS_DIR, 'key.bin')
COMPRESSOR_PATH = os.path.join(PROJECT_DIR, r'build\yuicompressor-2.4.8.jar')
EXTRACTOR_PATH = os.path.join(PROJECT_DIR, r'leakextractor\build\leakextractor-0.0.1.jar')


def test_normal():
    output_fn = JQUERY_MIN_PATH
    input_fn = os.path.join(PROJECT_DIR, JQUERY_PATH)
    test_fn = os.path.join(PROJECT_DIR, JQUERY_MIN_PATH)
    
    p = subprocess.Popen(['java', '-jar', COMPRESSOR_PATH, '-o', output_fn, input_fn], shell=True)
    p.wait()
    
    return open(test_fn, 'rb').read() == open(output_fn, 'rb').read()
    
    
def test_normal_randomize():
    output_fn = JQUERY_MIN_PATH + '.rnd'
    input_fn = os.path.join(PROJECT_DIR, JQUERY_PATH)
    test_fn = os.path.join(PROJECT_DIR, JQUERY_MIN_PATH)
    
    p = subprocess.Popen(['java', '-jar', COMPRESSOR_PATH, '--randomize', '-o', output_fn, input_fn], shell=True)
    p.wait()
    
    return open(test_fn, 'rb').read() != open(output_fn, 'rb').read()

    
def test_output_leak():
    output_fn = JQUERY_MIN_PATH + '.out.src'
    leak_fn = JQUERY_MIN_PATH + '.out.leak'
    input_fn = os.path.join(PROJECT_DIR, JQUERY_PATH)
    
    if os.path.isfile(leak_fn):
        os.remove(leak_fn)
    p = subprocess.Popen(['java', '-jar', COMPRESSOR_PATH, '--leaktype', 'output', '--leakkey', KEY_PATH, '-o', leak_fn, input_fn], shell=True)
    p.wait()
    
    if os.path.isfile(output_fn):
        os.remove(output_fn)
    p = subprocess.Popen(['java', '-jar', EXTRACTOR_PATH, '--leaktype', 'output', '--leakkey', KEY_PATH, '-o', output_fn, leak_fn], shell=True)
    p.wait()
    
    return open(JQUERY_PATH, 'rb').read() == open(output_fn, 'rb').read()


def test_context_leak():
    output_fn = JQUERY_MIN_PATH + '.ctx.src'
    ctx_fn = JQUERY_MIN_PATH + '.ctx.leak'
    obj_fn = JQUERY_MIN_PATH + '.ctx.obj'
    input_fn = os.path.join(PROJECT_DIR, JQUERY_PATH)
    
    if os.path.isfile(ctx_fn):
        os.remove(ctx_fn)
    p = subprocess.Popen(['java', '-jar', COMPRESSOR_PATH, '--leaktype', 'context', '--leakkey', KEY_PATH, '-o', ctx_fn, input_fn], shell=True)
    p.wait()
    
    from splinter.browser import Browser
    browser = Browser()
    browser.visit('file://' + os.path.realpath('test-ctx.html'))
    try:
        leak_json = browser.find_by_css('#leakObj')[0].value
    finally:
        browser.quit()
    
    if os.path.isfile(output_fn):
        os.remove(output_fn)
    open(obj_fn, 'wb').write(leak_json)
    p = subprocess.Popen(['java', '-jar', EXTRACTOR_PATH, '--leaktype', 'context', '--leakkey', KEY_PATH, '-o', output_fn, obj_fn], shell=True)
    p.wait()
    
    return open(JQUERY_PATH, 'rb').read() == open(output_fn, 'rb').read()
    
def test_backdoor_leak():
    output_fn = FA_MIN_PATH + '.back.src'
    back_fn = FA_MIN_PATH + '.back.leak'
    obj_fn = FA_MIN_PATH + '.back.obj'
    input_fn = os.path.join(PROJECT_DIR, FA_PATH)
    
    if os.path.isfile(back_fn):
        os.remove(back_fn)
    p = subprocess.Popen(['java', '-jar', COMPRESSOR_PATH, '--leaktype', 'backdoor', '--leakkey', KEY_PATH, '-o', back_fn, input_fn], shell=True)
    p.wait()
    
    from splinter.browser import Browser
    browser = Browser()
    browser.visit('file://' + os.path.realpath('test-back.html'))
    try:
        leak_json = browser.find_by_css('#leakObj')[0].value
    finally:
        browser.quit()
    
    if os.path.isfile(output_fn):
        os.remove(output_fn)
    open(obj_fn, 'wb').write(leak_json)
    p = subprocess.Popen(['java', '-jar', EXTRACTOR_PATH, '--leaktype', 'backdoor', '--leakkey', KEY_PATH, '-o', output_fn, obj_fn], shell=True)
    p.wait()
    
    return open(FA_PATH, 'rb').read() == open(output_fn, 'rb').read()


def main():
    if not os.path.isdir(TESTS_DIR):
        os.mkdir(TESTS_DIR)

    import shutil
    shutil.copyfile(os.path.join(PROJECT_DIR, JQUERY_PATH), JQUERY_PATH)
    shutil.copyfile(os.path.join(PROJECT_DIR, FA_PATH), FA_PATH)
    
    if test_normal():
        print '[PASSED]',
    else:
        print '[FAILED]',
    print 'Normal test'
    
    if test_normal_randomize():
        print '[PASSED]',
    else:
        print '[FAILED]',
    print 'Normal randomized test'
    
    if test_backdoor_leak():
        print '[PASSED]',
    else:
        print '[FAILED]',
    print 'Backdoor leak test'
    
    if test_output_leak():
        print '[PASSED]',
    else:
        print '[FAILED]',
    print 'Output leak test'
    
    if test_context_leak():
        print '[PASSED]',
    else:
        print '[FAILED]',
    print 'Context leak test'


if __name__ == '__main__':
    sys.exit(main())
