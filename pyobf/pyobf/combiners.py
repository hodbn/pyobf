from .obfuscators import BaseObfuscator


class BaseCombiner(BaseObfuscator):
    def __init__(self, obfs):
        self.obfs = obfs
        assert len(self.obfs) > 0
        langs = [o.lang for o in self.obfs]
        assert all(langs[0] == l for l in langs)
        self.lang = langs[0]

    def combine(self, prog):
        raise NotImplementedError()

    def obfuscate(self, prog):
        return self.combine(prog)

    def __repr__(self):
        return '<%s obfs=%r>' % (self.__class__.__name__, self.obfs)


class CascadeCombiner(BaseCombiner):
    def combine(self, prog):
        for obf in self.obfs:
            prog = obf.obfuscate(prog)
        return prog


class C3OutOf4Combiner(BaseCombiner):
    def __init__(self, obfs, maj):
        super(C3OutOf4Combiner, self).__init__(obfs)
        assert len(self.obfs) == 4
        self.o1, self.o2, self.o3, self.o4 = self.obfs
        self.maj = maj
        assert self.maj.lang == self.o1.lang

    def combine(self, prog):
        prog_o1 = self.o1.obfuscate(prog)
        prog_o2 = self.o2.obfuscate(prog)
        prog_o3 = self.o3.obfuscate(prog)
        prog_o4 = self.o4.obfuscate(prog)

        prog_o234 = self.maj.choose([prog_o2, prog_o3, prog_o4])
        prog_o134 = self.maj.choose([prog_o1, prog_o3, prog_o4])
        prog_o124 = self.maj.choose([prog_o1, prog_o2, prog_o4])

        prog_final = self.maj.choose([prog_o234, prog_o134, prog_o124])

        return prog_final
