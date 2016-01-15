import copy
import os

from .languages import *
from pyobf.executors import ObfuscatorExecutor, JarProcessCreator,\
    PerlProcessCreator, BareProcessCreator


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
        self.executor = ObfuscatorExecutor(self.jar, self.lang,
                                           JarProcessCreator)

    def obfuscate(self, prog):
        args = []
        if self.randomize:
            args.append('--randomize')
        if self.leak:
            args.append('--leaktype=%s' % (self._VALID_LEAKS_MAP[self.leak], ))
        args.extend(['-o', '%OUT_FILE%', '%IN_FILE%'])
        o_prog = copy.deepcopy(prog)
        o_prog.code = self.executor.execute(prog.code, args)
        return o_prog

    def __repr__(self):
        opts = []
        if self.randomize:
            opts.append('rand=%r' % (self.randomize, ))
        if self.leak is not None:
            opts.append('leak=%r' % (self.leak, ))
        opts = ', '.join(opts)
        if opts:
            opts = ' ' + opts
        return '<%s%s>' % (self.__class__.__name__, opts)


class ClosureObfuscator(BaseObfuscator, JSObfuscatorMixin):
    def __init__(self, jar):
        super(ClosureObfuscator, self).__init__()
        self.jar = jar
        self.executor = ObfuscatorExecutor(self.jar, self.lang,
                                           JarProcessCreator)

    def obfuscate(self, prog):
        args = ['-O', 'SIMPLE_OPTIMIZATIONS',
                '--js', '%IN_FILE%',
                '--js_output_file', '%OUT_FILE%']
        o_prog = copy.deepcopy(prog)
        o_prog.code = self.executor.execute(prog.code, args)
        return o_prog


class PackerObfuscator(BaseObfuscator, JSObfuscatorMixin):
    def __init__(self, script):
        super(PackerObfuscator, self).__init__()
        self.script = script
        self.executor = ObfuscatorExecutor(self.script, self.lang,
                                           PerlProcessCreator)

    def obfuscate(self, prog):
        args = ['-i', '%IN_FILE%',
                '-o', '%OUT_FILE%',
                '-e62']
        o_prog = copy.deepcopy(prog)
        o_prog.code = self.executor.execute(prog.code, args)
        return o_prog


class TigressObfuscator(BaseObfuscator, CObfuscatorMixin):
    def __init__(self, script, args):
        super(TigressObfuscator, self).__init__()
        self.script = script
        self.args = args
        self.executor = ObfuscatorExecutor(self.script, self.lang,
                                           BareProcessCreator)

    def obfuscate(self, prog):
        args = [self.args,
                '--out=$OUT_FILE',
                '$IN_FILE']
        tigress_home = os.path.basename(self.script)
        env = {
            'TIGRESS_HOME': tigress_home,
            'PATH': '%s:%s' % (os.environ['PATH'], tigress_home),
        }
        o_prog = copy.deepcopy(prog)
        o_prog.code = self.executor.execute(prog.code, args, env)
        return o_prog
