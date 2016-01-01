import os
import subprocess
import sys

from languages import *


class BaseObfuscator(object):
    def obfuscate(self, prog):
        raise NotImplementedError()

    def __repr__(self):
        return '<%s>' % (self.__class__.__name__, )


class JSObfuscatorMixin:
    @property
    def lang(self):
        return LANG_JS


class CObfuscatorMixin:
    @property
    def lang(self):
        return LANG_C


def _get_jar_input_output(jar, prog, args):
    env = os.environ
    in_fn, out_fn = 'in.js', 'out.js'
    env['IN_FILE'], env['OUT_FILE'] = in_fn, out_fn
    try:
        with open(in_fn, 'wb') as infile:
            infile.write(prog)
        try:
            p = subprocess.Popen(['java', '-jar', jar] + list(args),
                                 shell=True, env=env, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            assert p.returncode is not None
            if p.returncode != 0:
                sys.stdout.write(stdout)
                sys.stderr.write(stderr)
                assert False
            with open(out_fn, 'rb') as outfile:
                return outfile.read()
        finally:
            os.unlink(out_fn)
    finally:
        os.unlink(in_fn)


class YUIObfuscator(BaseObfuscator, JSObfuscatorMixin):
    _VALID_LEAKS_MAP = {
        'in-code': 'output',
        'run-time': 'backdoor',
        'external': 'context',
        # 'side-channel': None,
    }

    def __init__(self, jar, randomize=False, leak=None):
        super(YUIObfuscator, self).__init__()
        self.jar = jar
        self.randomize = randomize
        self.leak = leak
        if self.leak is not None:
            assert self.leak in self._VALID_LEAKS_MAP

    def obfuscate(self, prog):
        args = []
        if self.randomize:
            args.append('--randomize')
        if self.leak:
            args.append('--leaktype=%s' % (self._VALID_LEAKS_MAP[self.leak], ))
        args.extend(['-o', '%OUT_FILE%', '%IN_FILE%'])
        return _get_jar_input_output(self.jar, prog, args)

    def __repr__(self):
        return '<%s rand=%r, leak=%r>' % (self.__class__.__name__,
                                          self.randomize, self.leak)


class ClosureObfuscator(BaseObfuscator, JSObfuscatorMixin):
    def __init__(self, jar):
        super(ClosureObfuscator, self).__init__()
        self.jar = jar

    def obfuscate(self, prog):
        args = ['-O', 'SIMPLE_OPTIMIZATIONS', '--js', '%IN_FILE%',
                '--js_output_file', '%OUT_FILE%']
        return _get_jar_input_output(self.jar, prog, args)
