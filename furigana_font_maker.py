#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import sys
import fontforge
import psMat
import re
import codecs

if __name__ == '__main__':


    pattern = u"｜.*?》"
    text = u"テスト｜親文字《ふりがな》テストテスト"
    repatter = re.compile(pattern)
    result = re.search(repatter,text)
    
    f_test = codecs.open("test.txt", 'w', "utf_8")

    if result:
        print result.span()
        f_test.write(result.group())

    f_test.close()

    exit()


    src_text = sys.argv[1]
    src_font = sys.argv[2]
    dst_font = sys.argv[3]

    font = fontforge.open(src_font)
    text = open(src_text)

    furigana_scale = 0.5
    ascent_scale = 1.6

    oyamoji_all = text.readline().rstrip()
    furigana_all = text.readline().rstrip()

    print oyamoji_all
    print furigana_all

    furigana_unicode = 0xE000

    print font.fontname
    print font.fullname

    font.fontname = font.fontname + "_furigana"
    font.fullname = font.fullname + " Furigana"
    font.familyname = font.familyname + " Furigana"

    # 親文字全体の幅を計算（カーニングなどはないものとする）
    oyamoji_list = list(oyamoji_all)

    oyamoji_width = 0
    for oyamoji in oyamoji_list:
        oyamoji_width += font[oyamoji].width

   # ルビ全体の幅を計算（カーニングなどはないものとする）
    furigana_list = list(furigana_all)

    furigana_width = 0
    for furigana in furigana_list:
        furigana_width += font[furigana].width * furigana_scale

    # ルビの各文字の位置を計算
    list_furigana_x = []
    temp_x = 0
    for index, furigana in enumerate(furigana_list):
        list_furigana_x.append( -(oyamoji_width / 2) - (furigana_width / 2) + temp_x)
        temp_x += font[furigana].width * furigana_scale

    # ルビの高さを計算（今は親文字のすぐ上に）
    furigana_y = font.ascent

    # ルビの一文字目をコピペし、位置とサイズを変更
    font.selection.select(furigana_list[0])
    font.copy()

    font.selection.select(('more', 'unicode'), furigana_unicode)
    font.paste()

    matrix = psMat.compose(psMat.scale(furigana_scale), psMat.translate(list_furigana_x[0], furigana_y))
    font[furigana_unicode].transform(matrix)

    # ルビの二文字目移行の文字の位置とサイズを設定し、参照を追加
    for index, furigana in enumerate(furigana_list):
        if index == 0:
            continue
        matrix = psMat.compose(psMat.scale(furigana_scale), psMat.translate(list_furigana_x[index], furigana_y))
        font[furigana_unicode].addReference(furigana, matrix)

    # ルビ文字の幅をゼロに（親文字の後ろにつけるので）
    font[furigana_unicode].width = 0;

    # フォントの高さを修正（ルビ文字が入るように）
    font.ascent = font.ascent * ascent_scale

    # フォント出力
    font.generate(dst_font)

    font.close()
    text.close()