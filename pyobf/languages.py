(
    LANG_C,
    LANG_JS,
) = range(2)
_text = {
    LANG_C: 'C',
    LANG_JS: 'JS',
}


def lang_text(lang):
    return _text[lang]
