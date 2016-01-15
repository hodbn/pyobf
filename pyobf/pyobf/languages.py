(
    LANG_C,
    LANG_JS,
) = range(2)
_text = {
    LANG_C: 'C',
    LANG_JS: 'JS',
}
_ext = {
    LANG_C: 'c',
    LANG_JS: 'js',
}


def lang_text(lang):
    return _text[lang]


def lang_ext(lang):
    return _ext[lang]
