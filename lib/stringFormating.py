# -*- coding: utf-8 -*- 

def accents2ascii(text):
    dic={ u"á": "a", u"é": "e", u"í": "i", u"ó": "o", u"ú": "u", u"ľ": "l", u"š": "s", u"č": "c", u"ť": "t", u"ž": "z", u"ý": "y", u"ď": "d", u"ň": "n", u"ô": "o", u"ŕ": "r", u"ĺ": "l", u"ä": "a", u"ü": "u", u"ö": "o", u"Á": "A", u"É": "E", u"Í": "I", u"Ó": "O", u"Ú": "U", u"Ľ": "L", u"Š": "S", u"Č": "C", u"Ť": "T", u"Ž": "Z", u"Ý": "Y", u"Ď": "D", u"Ň": "N", u"Ô": "O", u"Ŕ": "R", u"Ĺ": "L", u"Ӓ": "A", u"Ö": "O", u"Ü": "U",  u"\xb4":""}
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text