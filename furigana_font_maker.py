#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import sys
import fontforge
import psMat
import re
import codecs
import unicodedata

# 文字列の各文字のフォントの幅の合計を計算（カーニングなどはないものとする）
def calc_text_width(text, font):
    text_list = list(text)

    width = 0
    for glyph in text_list:
        glyph_codepoint = ord(glyph)
        width += font[glyph_codepoint].width

    return width

# ルビの各文字の位置を計算（親文字の文字列の中央に、カーニングなしで並べる）
def calc_furigana_x(text_furigana, oyamoji_width, furigana_width, furigana_scale, font):

    list_furigana_x = []
    temp_x = 0
    furigana_list = list(text_furigana)
    for index, furigana in enumerate(furigana_list):
        list_furigana_x.append( -(oyamoji_width / 2) - (furigana_width / 2) + temp_x)
        furigana_codepoint = ord(furigana)
        temp_x += font[furigana_codepoint].width * furigana_scale

    return list_furigana_x

# 文字列から正規表現にマッチする箇所を抜き出し、前後の記号を削除して返す（マッチするものがない場合は""を返す）
def extract_text_within_symbol(text, re_pattern_object, symbol_left, symbol_right):
    re_result = re.search(re_pattern_object,text)
    text_within_symbol = ""
    if re_result:
        text_within_symbol = re_result.group()
        text_within_symbol = text_within_symbol.strip(symbol_left)
        text_within_symbol = text_within_symbol.strip(symbol_right)
    return text_within_symbol

def main():
    src_text = sys.argv[1]
    src_font = sys.argv[2]
    dst_font = sys.argv[3]

    font = fontforge.open(src_font)
    file_src_text = codecs.open(src_text,'r', "utf_8")

    furigana_scale = 0.5
    ascent_scale = 1.6

    new_furigana_codepoint = 0xE000

    symbol_oyamoji_left   = u"｜"
    symbol_oyamoji_right  = u"《"
    symbol_furigana_left  = u"《"
    symbol_furigana_right = u"》"
    
    # 正規表現の準備
    re_pattern_oyamoji_furigana = symbol_oyamoji_left  + u".*?" + symbol_furigana_right
    re_pattern_oyamoji          = symbol_oyamoji_left  + u".*?" + symbol_oyamoji_right
    re_pattern_furigana         = symbol_furigana_left + u".*?" + symbol_furigana_right
    re_pattern_object_oyamoji_furigana = re.compile(re_pattern_oyamoji_furigana)
    re_pattern_object_oyamoji = re.compile(re_pattern_oyamoji)
    re_pattern_object_furigana = re.compile(re_pattern_furigana)
   
    # ファイルからテキストを読み込み
    src_text_line = file_src_text.readline().rstrip()

    # テキストから親文字とルビの指定がある部分を抽出
    re_result_oyamoji_furigana = re.search(re_pattern_object_oyamoji_furigana,src_text_line)
    
    f_test = codecs.open("test.txt", 'w', "utf_8")

    if re_result_oyamoji_furigana:
        text_oyamoji_furigana = re_result_oyamoji_furigana.group()
        f_test.write(text_oyamoji_furigana + "\r\n")

        # 親文字部分を抽出
        text_oyamoji = extract_text_within_symbol(text_oyamoji_furigana, re_pattern_object_oyamoji, symbol_oyamoji_left, symbol_oyamoji_right)

        # ルビ部分を抽出
        text_furigana = extract_text_within_symbol(text_oyamoji_furigana, re_pattern_object_furigana, symbol_furigana_left, symbol_furigana_right)


    font.fontname = font.fontname + "_furigana"
    font.fullname = font.fullname + " Furigana"
    font.familyname = font.familyname + " Furigana"

    # 親文字全体の幅を計算（カーニングなどはないものとする）
    oyamoji_width = calc_text_width(text_oyamoji, font)

    # ルビ全体の幅を計算（カーニングなどはないものとする）
    furigana_width = calc_text_width(text_furigana, font) * furigana_scale

    # ルビの各文字の位置を計算
    list_furigana_x = calc_furigana_x(text_furigana, oyamoji_width, furigana_width, furigana_scale, font)

    # ルビの高さを計算（今は親文字のすぐ上に）
    furigana_y = font.ascent

    # ルビの新たな文字を合成し、私用領域に割り当てる
    for index, furigana in enumerate(list(text_furigana)):
        if index == 0:
            # ルビの一文字目だけは、コピペして位置とサイズを変更（全ての文字が参照だと、上手くいかないっぽいので）
            furigana_codepoint = ord(furigana)
            font.selection.select(furigana_codepoint)
            font.copy()

            font.selection.select(('more', 'unicode'), new_furigana_codepoint)
            font.paste()

            matrix = psMat.compose(psMat.scale(furigana_scale), psMat.translate(list_furigana_x[0], furigana_y))
            font[new_furigana_codepoint].transform(matrix)

        else:
            # ルビの二文字目以降は、文字の位置とサイズを設定して参照を追加
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
    file_src_text.close()

    f_test.close()

if __name__ == '__main__':
    main()
