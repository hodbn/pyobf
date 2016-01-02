import copy
import json
import os
import jinja2

from .languages import *


tpl_loader = jinja2.FileSystemLoader(searchpath=os.path.join(
    os.path.dirname(__file__), 'templates'))
tpl_env = jinja2.Environment(loader=tpl_loader)


def _unsafeescapejs(val):
    return json.dumps(str(val))
tpl_env.filters['unsafeescapejs'] = _unsafeescapejs


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
        assert len(progs) > 1
        progs_name = progs[0].name
        tpl = tpl_env.get_template(self._TPL_FN)
        o_prog = copy.deepcopy(progs[0])
        o_prog.code = tpl.render(progs=progs, prog_name=progs_name)
        return o_prog


class DefensiveChooser(BaseChooser):
    pass
