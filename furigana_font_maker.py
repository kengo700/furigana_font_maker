#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import sys
import fontforge
import psMat

if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    font = fontforge.open(src)

    font.selection.select("A")
    font.copy()

    font.selection.select(('more', 'unicode'), 0xE000)
    font.paste()

    matrix = psMat.compose(psMat.scale(0.5), psMat.translate(0,1000))
    font[0xE000].addReference("B", matrix)

    font.generate(dst)
    font.close()