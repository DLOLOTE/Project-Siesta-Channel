from .tr_en import EN
from .tr_hi import HI
from .tr_tr import TR

LANGS = {"en": EN, "hi": HI, "tr": TR}
L: EN = EN

def set_lang(code: str):
    global L
    L = LANGS.get(code, EN)