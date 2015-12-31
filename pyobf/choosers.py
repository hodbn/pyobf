class BaseChooser(object):
    def __init__(self, lang):
        self.lang = lang

    def choose(self, progs):
        raise NotImplementedError()


class MajorityChooser(BaseChooser):
    def choose(self, progs):
        raise NotImplementedError()


class DefensiveChooser(BaseChooser):
    def choose(self, progs):
        raise NotImplementedError()
