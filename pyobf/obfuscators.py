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


class YUIObfuscator(BaseObfuscator, JSObfuscatorMixin):
    def __init__(self, jar, randomize=False):
        super(YUIObfuscator, self).__init__()
        self.jar = jar
        self.randomize = randomize

    def _run_jar(self, *args):
        p = subprocess.Popen(['java', '-jar', self.jar] + list(args),
                             shell=True)
        p.wait()
        return p.returncode == 0

    def obfuscate(self, prog):
        in_fn = 'in.js'
        out_fn = 'out.js'
        try:
            with open(in_fn, 'wb') as infile:
                infile.write(prog)
            try:
                args = []
                if self.randomize:
                    args.append('--randomize')
                args.extend(['-o', out_fn, infile.name])
                if not self._run_jar(*args):
                    return None
                with open(out_fn, 'rb') as outfile:
                    return outfile.read()
            finally:
                os.unlink(out_fn)
        finally:
            os.unlink(in_fn)
