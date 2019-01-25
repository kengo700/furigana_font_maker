#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import sys
import fontforge
import psMat
import re
import codecs
import unicodedata

if __name__ == '__main__':

    src_text = sys.argv[1]
    src_font = sys.argv[2]
    dst_font = sys.argv[3]

    font = fontforge.open(src_font)
    #text = open(src_text)

    furigana_scale = 0.5
    ascent_scale = 1.6

    new_furigana_codepoint = 0xE000

    re_pattern_oyamoji_furigana = u"｜.*?》"
    re_pattern_oyamoji = u"｜.*?《"
    re_pattern_furigana = u"《.*?》"

    text = u"テスト｜親文字《ふりがな》テストテスト"

    re_pattern_object_oyamoji_furigana = re.compile(re_pattern_oyamoji_furigana)
    re_pattern_object_oyamoji = re.compile(re_pattern_oyamoji)
    re_pattern_object_furigana = re.compile(re_pattern_furigana)


    re_result_oyamoji_furigana = re.search(re_pattern_object_oyamoji_furigana,text)
    
    f_test = codecs.open("test.txt", 'w', "utf_8")

    if re_result_oyamoji_furigana:
        print re_result_oyamoji_furigana.span()
        text_oyamoji_furigana = re_result_oyamoji_furigana.group()
        f_test.write(text_oyamoji_furigana + "\r\n")

        # 親文字部分を抽出
        re_result_oyamoji = re.search(re_pattern_object_oyamoji,text_oyamoji_furigana)
        if re_result_oyamoji:
            text_oyamoji = re_result_oyamoji.group()
            text_oyamoji = text_oyamoji.strip(u"｜")
            text_oyamoji = text_oyamoji.strip(u"《")
            f_test.write(text_oyamoji + "\r\n")

        # ルビ部分を抽出
        re_result_furigana = re.search(re_pattern_object_furigana,text_oyamoji_furigana)
        if re_result_furigana:
            text_furigana = re_result_furigana.group()
            text_furigana = text_furigana.strip(u"《")
            text_furigana = text_furigana.strip(u"》")
            f_test.write(text_furigana )


    font.fontname = font.fontname + "_furigana"
    font.fullname = font.fullname + " Furigana"
    font.familyname = font.familyname + " Furigana"

    # 親文字全体の幅を計算（カーニングなどはないものとする）
    oyamoji_list = list(text_oyamoji)

    oyamoji_width = 0
    for oyamoji in oyamoji_list:
        oyamoji_codepoint = ord(oyamoji)
        oyamoji_width += font[oyamoji_codepoint].width


    # ルビ全体の幅を計算（カーニングなどはないものとする）
    furigana_list = list(text_furigana)

    furigana_width = 0
    for furigana in furigana_list:
        furigana_codepoint = ord(furigana)
        furigana_width += font[furigana_codepoint].width * furigana_scale

    # ルビの各文字の位置を計算
    list_furigana_x = []
    temp_x = 0
    for index, furigana in enumerate(furigana_list):
        list_furigana_x.append( -(oyamoji_width / 2) - (furigana_width / 2) + temp_x)
        furigana_codepoint = ord(furigana)
        temp_x += font[furigana_codepoint].width * furigana_scale

    # ルビの高さを計算（今は親文字のすぐ上に）
    furigana_y = font.ascent

    # ルビの一文字目をコピペし、位置とサイズを変更
    furigana_0_codepoint = ord(furigana_list[0])
    font.selection.select(furigana_0_codepoint)
    font.copy()

    font.selection.select(('more', 'unicode'), new_furigana_codepoint)
    font.paste()

    matrix = psMat.compose(psMat.scale(furigana_scale), psMat.translate(list_furigana_x[0], furigana_y))
    font[new_furigana_codepoint].transform(matrix)

    # ルビの二文字目移行の文字の位置とサイズを設定し、参照を追加
    for index, furigana in enumerate(furigana_list):
        if index == 0:
            continue
        matrix = psMat.compose(psMat.scale(furigana_scale), psMat.translate(list_furigana_x[index], furigana_y))
        furigana_codepoint = ord(furigana)
        font[new_furigana_codepoint].addReference(font[furigana_codepoint].glyphname , matrix)

    # ルビ文字の幅をゼロに（親文字の後ろにつけるので）
    font[new_furigana_codepoint].width = 0;

    # フォントの高さを修正（ルビ文字が入るように）
    font.ascent = font.ascent * ascent_scale

    # フォント出力
    font.generate(dst_font)

    font.close()
    #text.close()

    f_test.close()