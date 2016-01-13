import copy
import os
import subprocess
import sys
import tempfile

from .languages import *


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


def _create_jar_process(jar, args, env):
    return subprocess.Popen(['java', '-jar', jar] + list(args),
                            shell=True, env=env, cwd=os.path.dirname(jar),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _create_perl_process(script, args, env):
    return subprocess.Popen(['perl', script] + list(args),
                            shell=True, env=env, cwd=os.path.dirname(script),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _get_input_output(proc_creator, exe, code, args):
    env = os.environ
    cwd = os.path.dirname(exe)
    in_fd, in_fn = tempfile.mkstemp(suffix='.js', dir=cwd)
    try:
        os.close(in_fd)
        out_fd, out_fn = tempfile.mkstemp(suffix='.js', dir=cwd)
        os.close(out_fd)
        env['IN_FILE'] = os.path.basename(in_fn)
        env['OUT_FILE'] = os.path.basename(out_fn)
        with open(in_fn, 'wb') as infile:
            infile.write(code)
        try:
            p = proc_creator(exe, args, env)
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


def _get_jar_input_output(jar, code, args):
    return _get_input_output(_create_jar_process, jar, code, args)


def _get_perl_input_output(script, code, args):
    return _get_input_output(_create_perl_process, script, code, args)


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
        o_prog = copy.deepcopy(prog)
        o_prog.code = _get_jar_input_output(self.jar, prog.code, args)
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

    def obfuscate(self, prog):
        args = ['-O', 'SIMPLE_OPTIMIZATIONS',
                '--js', '%IN_FILE%',
                '--js_output_file', '%OUT_FILE%']
        o_prog = copy.deepcopy(prog)
        o_prog.code = _get_jar_input_output(self.jar, prog.code, args)
        return o_prog


class PackerObfuscator(BaseObfuscator, JSObfuscatorMixin):
    def __init__(self, script):
        super(PackerObfuscator, self).__init__()
        self.script = script

    def obfuscate(self, prog):
        args = ['-i', '%IN_FILE%',
                '-o', '%OUT_FILE%',
                '-e62']
        o_prog = copy.deepcopy(prog)
        o_prog.code = _get_perl_input_output(self.script, prog.code, args)
        return o_prog
