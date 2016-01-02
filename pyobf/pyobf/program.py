from .languages import lang_text


class Program(object):
    def __init__(self, name, lang, fn, test_fn=None):
        self.name = name
        self.lang = lang
        with open(fn, 'rb') as f:
            self.code = f.read()
        if test_fn is not None:
            with open(test_fn, 'rb') as f:
                self.test = f.read()
        else:
            self.test = None

    def __repr__(self):
        return '<Program name=%s, lang=%s>' % (self.name, lang_text(self.lang))