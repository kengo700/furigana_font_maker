#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import sys
import fontforge
import psMat

if __name__ == '__main__':

    src = sys.argv[1]
    dst = sys.argv[2]
    font = fontforge.open(src)

    furigana_scale = 0.5

    print font.fontname
    print font.fullname

    font.fontname = font.fontname + "_furigana"
    font.fullname = font.fullname + " Furigana"
    font.familyname = font.familyname + " Furigana"

    oyamoji_all = "ABC"
    oyamoji_list = list(oyamoji_all)

    oyamoji_width = 0
    for oyamoji in oyamoji_list:
        oyamoji_width += font[oyamoji].width

    oyamoji_center = oyamoji_width / 2

    furigana_all = "A"
    furigana_list = list(furigana_all)

    font.selection.select(furigana_list[0])
    font.copy()

    font.selection.select(('more', 'unicode'), 0xE000)
    font.paste()

    furigana_width = font[furigana_list[0]].width;

    furigana_x = -oyamoji_center - furigana_width/2*furigana_scale

    ascent = font.ascent

    matrix = psMat.compose(psMat.scale(furigana_scale), psMat.translate(furigana_x, ascent))
    font[0xE000].transform(matrix)

    #matrix = psMat.compose(psMat.scale(furigana_scale), psMat.translate(1000, ascent))
    #font[0xE000].addReference("B", matrix)

    font[0xE000].width = 0;

    font.ascent = ascent + ascent * 0.5

    font.generate(dst)
    font.close()