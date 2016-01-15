import os
import subprocess
import sys
import tempfile
from pyobf.languages import lang_ext


class BaseProcessCreator(object):
    @classmethod
    def create_process(cls, exe, args, env):
        raise NotImplementedError()


class JarProcessCreator(BaseProcessCreator):
    JAVA_EXE = r'java'

    @classmethod
    def create_process(cls, exe, args, env):
        return subprocess.Popen([cls.JAVA_EXE, '-jar', exe] + list(args),
                                shell=True, env=env, cwd=os.path.dirname(exe),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class PerlProcessCreator(BaseProcessCreator):
    PERL_EXE = r'perl'

    @classmethod
    def create_process(cls, exe, args, env):
        return subprocess.Popen([cls.PERL_EXE, exe] + list(args), shell=True,
                                env=env, cwd=os.path.dirname(exe),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class BareProcessCreator(BaseProcessCreator):
    @classmethod
    def create_process(cls, exe, args, env):
        return subprocess.Popen([exe] + list(args), shell=True, env=env,
                                cwd=os.path.dirname(exe),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class ObfuscatorExecutor(object):
    def __init__(self, exe, lang, proc_creator):
        self.exe = exe
        self.lang = lang
        self.proc_creator = proc_creator

    def execute(self, code, args, env=None):
        new_env = os.environ.copy()
        if env is not None:
            new_env.update(env)
        env = new_env
        cwd = os.path.dirname(self.exe)
        suffix = '.%s' % (lang_ext(self.lang), )
        in_fd, in_fn = tempfile.mkstemp(suffix=suffix, dir=cwd)
        try:
            os.close(in_fd)
            out_fd, out_fn = tempfile.mkstemp(suffix=suffix, dir=cwd)
            os.close(out_fd)
            env['IN_FILE'] = os.path.basename(in_fn)
            env['OUT_FILE'] = os.path.basename(out_fn)
            with open(in_fn, 'wb') as infile:
                infile.write(code)
            try:
                p = self.proc_creator.create_process(self.exe, args, env)
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
