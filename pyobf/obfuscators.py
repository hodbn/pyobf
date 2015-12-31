import os
import subprocess

from languages import *


class BaseObfuscator(object):
    def obfuscate(self, prog):
        raise NotImplementedError()

    def __str__(self):
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
                                 shell=True, env=env)
            p.wait()
            assert p.returncode == 0
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
            self.leak = self._VALID_LEAKS_MAP[leak]

    def obfuscate(self, prog):
        args = []
        if self.randomize:
            args.append('--randomize')
        if self.leak:
            args.append('--leaktype=%s' % (self.leak, ))
        args.extend(['-o', '%OUT_FILE%', '%IN_FILE%'])
        return _get_jar_input_output(self.jar, prog, args)


class ClosureObfuscator(BaseObfuscator, JSObfuscatorMixin):
    def __init__(self, jar):
        super(ClosureObfuscator, self).__init__()
        self.jar = jar

    def obfuscate(self, prog):
        args = ['-O', 'SIMPLE_OPTIMIZATIONS', '--js', '%IN_FILE%',
                '--js_output_file', '%OUT_FILE%']
        return _get_jar_input_output(self.jar, prog, args)
