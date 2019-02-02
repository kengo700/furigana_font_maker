#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import sys
import fontforge
import psMat
import re
import codecs
import unicodedata
import ConfigParser
import os

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

# 文字列から正規表現にマッチする箇所を抜き出し、前後の記号を削除して返す（マッチするものがない場合はNoneを返す）
def extract_text_within_symbol(text, re_pattern_object, symbol_left, symbol_right):
    re_result = re.search(re_pattern_object,text)
    text_within_symbol = None
    if re_result:
        text_within_symbol = re_result.group()
        text_within_symbol = text_within_symbol.strip(symbol_left)
        text_within_symbol = text_within_symbol.strip(symbol_right)
    return text_within_symbol


def main():
    config_file = sys.argv[1]

    # 設定ファイル読み込み
    #   各変数の意味は、設定ファイルを参照
    config = ConfigParser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
    else:
        sys.stderr.write('%s was not found.' % config_file)
        sys.exit(2)

    src_text = config.get("file","src_text")
    src_font = config.get("file","src_font")
    dst_text = config.get("file","dst_text")
    dst_font = config.get("file","dst_font")

    mode_new_glyph = config.get("mode","new_glyph")

    furigana_scale         = config.getfloat("glyph","furigana_scale")
    all_glyph_ascent_scale = config.getfloat("glyph","all_glyph_ascent_scale")
    furigana_height        = config.getfloat("glyph","furigana_height")
    all_glyph_height       = config.getfloat("glyph","all_glyph_height")
    new_furigana_codepoint = int(config.get("glyph","furigana_codepoint_start"),0)

    symbol_oyamoji_left   = config.get("text","symbol_oyamoji_left").decode('utf-8')
    symbol_oyamoji_right  = config.get("text","symbol_oyamoji_right").decode('utf-8')
    symbol_furigana_left  = config.get("text","symbol_furigana_left").decode('utf-8')
    symbol_furigana_right = config.get("text","symbol_furigana_right").decode('utf-8')


    option_onechar      = False
    option_nofurigana   = False

    # ルビと親文字を一文字ずつ組み合わせて出力する（親文字が二文字以上の場合は、最初の文字以降を無視する）
    if mode_new_glyph == "both_oyamoji_furigana":
        option_onechar = True

    # ルビを振らずに親文字だけを一文字ずつ出力する
    if mode_new_glyph == "only_oyamoji":
        option_onechar = True
        option_nofurigana = True


    # テキスト中に出てきたルビ指定を保存する辞書（同じルビ指定が出たときに使い回せるように）
    dictionary_oyamoji_furigana = {}

    # テキスト中に出てきたルビ指定を保存する辞書（親文字の幅とルビを記録しておき、例えば傍点などを使い回せるように）
    dictionary_width_furigana = {}
    
    # 正規表現の準備
    re_pattern_oyamoji_furigana = symbol_oyamoji_left  + ".*?" + symbol_furigana_right
    re_pattern_oyamoji          = symbol_oyamoji_left  + ".*?" + symbol_oyamoji_right
    re_pattern_furigana         = symbol_furigana_left + ".*?" + symbol_furigana_right
    re_pattern_object_oyamoji_furigana = re.compile(re_pattern_oyamoji_furigana)
    re_pattern_object_oyamoji = re.compile(re_pattern_oyamoji)
    re_pattern_object_furigana = re.compile(re_pattern_furigana)

    # ファイル読み込み
    font = fontforge.open(src_font)
    file_src_text = codecs.open(src_text,'r', "utf_8")
    file_dst_text = codecs.open(dst_text,'w', "utf_8")
    
    # フォント名を修正
    font.fontname = font.fontname + "_furigana"
    font.fullname = font.fullname + " Furigana"
    font.familyname = font.familyname + " Furigana"

    # 全ての文字の高さを調整
    matrix = psMat.translate(0, all_glyph_height)
    font.selection.all()
    font.transform(matrix)

    # ファイルからテキストを一行ずつ読み込み
    for src_text_line in file_src_text:

        # テキスト内のルビの指定がある部分を順次抽出
        while True:
            # テキストからルビの指定がある部分を抽出
            re_result_oyamoji_furigana = re.search(re_pattern_object_oyamoji_furigana,src_text_line)
    
            if re_result_oyamoji_furigana == None:
                # ルビ指定の検索結果がなくなったら、この行に対する処理は終了
                break

            text_oyamoji_furigana = re_result_oyamoji_furigana.group()

            # 親文字部分を抽出
            text_oyamoji = extract_text_within_symbol(text_oyamoji_furigana, re_pattern_object_oyamoji, symbol_oyamoji_left, symbol_oyamoji_right)

            # ルビ部分を抽出
            text_furigana = extract_text_within_symbol(text_oyamoji_furigana, re_pattern_object_furigana, symbol_furigana_left, symbol_furigana_right)

            if(text_oyamoji == None or text_furigana == None):
                # 親文字部分、もしくはルビ部分がNoneの場合（抽出が上手くいかなかった場合）は、この行に対する処理を終了
                #   本来は何らかのエラーメッセージを出すべきなので、要修正
                break

            # 親文字全体の幅を計算（カーニングなどはないものとする）
            oyamoji_width = calc_text_width(text_oyamoji, font)

            # ルビ全体の幅を計算（カーニングなどはないものとする）
            furigana_width = calc_text_width(text_furigana, font) * furigana_scale

            # 親文字の幅とルビの文字を組み合わせた変数を作成
            width_and_furigana = str(furigana_width) + text_furigana

            # このルビ指定が既出であれば、それを使い回す
            if text_oyamoji_furigana in dictionary_oyamoji_furigana:

                # ルビの指定部分を置換し、出力用の文字列を作成する（一カ所ずつ処理するので、replaceの回数を1に）
                temp_furigana_codepoint = dictionary_oyamoji_furigana[text_oyamoji_furigana]
                if option_onechar:
                    # ルビと親文字を一文字にする場合は、親文字を残さない
                    src_text_line = src_text_line.replace(text_oyamoji_furigana,                unichr(temp_furigana_codepoint), 1)
                else:
                    src_text_line = src_text_line.replace(text_oyamoji_furigana, text_oyamoji + unichr(temp_furigana_codepoint), 1)

            # 親文字の幅とルビが既出のものがあれば、それを使い回す
            elif ((option_onechar != True) and (width_and_furigana in dictionary_width_furigana)):

                # ルビの指定部分を置換し、出力用の文字列を作成する（一カ所ずつ処理するので、replaceの回数を1に）
                temp_furigana_codepoint = dictionary_width_furigana[width_and_furigana]
                src_text_line = src_text_line.replace(text_oyamoji_furigana, text_oyamoji + unichr(temp_furigana_codepoint), 1)

            # このルビ指定が初めて出てきたものであれば、新たにルビ文字を作成する
            else:
                # 辞書に登録
                dictionary_oyamoji_furigana[text_oyamoji_furigana] = new_furigana_codepoint
                dictionary_width_furigana[width_and_furigana] = new_furigana_codepoint

                # ルビの各文字の位置を計算
                list_furigana_x = calc_furigana_x(text_furigana, oyamoji_width, furigana_width, furigana_scale, font)

                # ルビの高さを計算
                furigana_y = font.ascent + furigana_height

                if option_onechar:
                    # 親文字をコピペし、私用領域に割り当てる
                    for index, oyamoji in enumerate(list(text_oyamoji)):
                        if index == 0:
                            oyamoji_codepoint = ord(oyamoji)
                            font.selection.select(oyamoji_codepoint)
                            font.copy()

                            font.selection.select(('more', 'unicode'), new_furigana_codepoint)
                            font.paste()

                            matrix = psMat.compose(psMat.scale(1.0), psMat.translate(0.0, 0.0))
                            font[new_furigana_codepoint].transform(matrix)
                    
                        else:
                            # 親文字の二文字目以降は読み捨てる
                            break

                    if option_nofurigana != True:
                        # 親文字にルビを合成し、一文字にする
                        for index, furigana in enumerate(list(text_furigana)):
                            matrix = psMat.compose(psMat.scale(furigana_scale), psMat.translate(oyamoji_width + list_furigana_x[index], furigana_y))
                            furigana_codepoint = ord(furigana)
                            font[new_furigana_codepoint].addReference(font[furigana_codepoint].glyphname , matrix)

                else:
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
                if (option_onechar != True):
                    font[new_furigana_codepoint].width = 0

                # ルビの指定部分を置換し、出力用の文字列を作成する（一カ所ずつ処理するので、replaceの回数を1に）
                if option_onechar:
                    # ルビと親文字を一文字にするので親文字を残さない
                    src_text_line = src_text_line.replace(text_oyamoji_furigana,                unichr(new_furigana_codepoint), 1)
                else:
                    src_text_line = src_text_line.replace(text_oyamoji_furigana, text_oyamoji + unichr(new_furigana_codepoint), 1)

                # ルビ文字を割り当てるコードポイントを次へ
                new_furigana_codepoint += 1

        # ルビ文字を置き換えたテキストを出力
        file_dst_text.write(src_text_line)

    # フォントの高さを修正（ルビ文字が入るように）
    font.ascent = font.ascent * all_glyph_ascent_scale

    # フォント出力
    font.generate(dst_font)

    # 後処理
    font.close()
    file_src_text.close()
    file_dst_text.close()


if __name__ == '__main__':
    main()
