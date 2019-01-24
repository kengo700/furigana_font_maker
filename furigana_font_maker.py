#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import sys
import fontforge
import psMat

if __name__ == '__main__':

    src = sys.argv[1]
    dst = sys.argv[2]
    font = fontforge.open(src)

    oyamoji_all = "ABC"
    oyamoji_list = list(oyamoji_all)

    oyamoji_width = 0
    for oyamoji in oyamoji_list:
        oyamoji_width += font[oyamoji].width
        print font[oyamoji].width

    print oyamoji_width
    print oyamoji_width / 2

    font.selection.select("A")
    font.copy()

    font.selection.select(('more', 'unicode'), 0xE000)
    font.paste()

    ascent = font.ascent

    matrix = psMat.compose(psMat.scale(0.5), psMat.translate(0, ascent))
    font[0xE000].transform(matrix)

    matrix = psMat.compose(psMat.scale(0.5), psMat.translate(1000, ascent))
    font[0xE000].addReference("B", matrix)

    font[0xE000].width = 0;

    font.ascent = ascent + ascent * 0.5

    font.generate(dst)
    font.close()