#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import sys
import fontforge

if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    font = fontforge.open(src)
    font.generate(dst)
    font.close()