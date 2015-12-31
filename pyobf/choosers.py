import jinja2
from languages import *


tpl_loader = jinja2.FileSystemLoader(searchpath='templates')
tpl_env = jinja2.Environment(loader=tpl_loader)


class BaseChooser(object):
    def choose(self, progs):
        raise NotImplementedError()


class JSChooserMixin:
    @property
    def lang(self):
        return LANG_JS


class CChooserMixin:
    @property
    def lang(self):
        return LANG_C


class MajorityChooser(BaseChooser):
    pass


class JSMajorityChooser(MajorityChooser, JSChooserMixin):
    _TPL_FN = r'js-majority-chooser.tpl'

    def choose(self, progs):
        tpl = tpl_env.get_template(self._TPL_FN)
        return tpl.render(progs=progs)


class DefensiveChooser(BaseChooser):
    pass
