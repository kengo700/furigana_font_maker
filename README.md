# Furigana Font Maker

ゲームの字幕にルビ（ふりがな）を表示するために、フォントにルビを埋め込むプログラムです。ルビを表示する機能がない海外ゲームでも、ルビを表示できる可能性があります。

現在開発中のベータ版です。

## コンセプト

ルビを指定したテキストとオリジナルのフォントを読み込み、ルビを埋め込んだ文字を生成してUnicodeの[私用領域][1]に割り当てます。この文字をテキストの文字と置き換えることで、ゲーム内でルビ表示を表示します。

＜コンセプト図＞


## 活用例

ゲームの字幕にルビを振ることで、表現の幅が広がります。

＜図＞

ゲームの固有名詞の原文を表示することで、「日本語化されると英語Wikiを検索できない」問題を解決します。

＜図＞


# 環境

* [FontForge][2]
* Python2


# 使い方

## インストール

このページの右上の「Clone or download」ボタンから「Download ZIP」でダウンロードし、解凍

[FontForge][2]をダウンロードしてインストール（必要なPythonはFontForgeに含まれています）


## テキストとフォントの準備

ゲームのテキストで、親文字（ルビを振りたい文字）とルビを下記のように指定し、UTF-8で保存

    ｜親文字《ルビ》

使用したいTTF形式のフォントを準備し、ファイル名を確認しておく

## ルビ用フォント＆テキストの生成

ダウンロードした「furigana_font_maker」フォルダ内の「furigana_font_maker.bat」をメモ帳で開き、下記の部分を書き換えて保存

    set SRC_TEXT=読み込みたいテキストのファイル名
    set SRC_FONT=読み込みたいフォントのファイル名
    set DST_TEXT=作成するテキストのファイル名
    set DST_FONT=作成するフォントのファイル名

FontForgeのインストール先をデフォルトから変えている場合は、下記も修正

    set FF=C:\Program Files (x86)\FontForgeBuilds

修正した「furigana_font_maker.bat」をダブルクリックし、ルビ用フォント＆テキストの生成処理を実行する

## 生成したフォント＆テキストの確認

生成したフォントをFontForgeで開き、「表示」メニューの「移動」から「u+e000」へ移動すると、ルビ文字が生成されているはず

生成したテキストをメモ帳などで開くと、親文字の後ろに記号が表示されているはず（現在のフォントによって表示は異なる）
　

# 参考文献

* アイデア
    * 恐らくゲーム翻訳家の武藤陽生さんが考案者。フォントに手動でルビを埋め込み、「The Vanishing of Ethan Carter」に実装されている
        * http://gametranslation.blog.fc2.com/blog-entry-29.html
        * https://twitter.com/Minstrel_Bird/status/995850877972889602
    * 私のアイデアメモ
        * https://twitter.com/kengo700/status/934231043820761088
        * https://twitter.com/kengo700/status/934242914510635008
* FontForgeのPythonプログラミング
    * [Writing python scripts to change fonts in FontForge](https://fontforge.github.io/en-US/documentation/scripting/python/)
    * [Writing python scripts to change fonts in FontForge](https://fontforge.github.io/python.html)
    * [Writing python scripts to change fonts in FontForge](http://dmtr.org/ff.php)
    * [FontForge の Python bindings を使えるようにする - にせねこメモ](chrome://bookmarks/?id=13202#1)
    * [amiri/tools at master · alif-type/amiri](https://github.com/alif-type/amiri/tree/master/tools)
    * [Generate Script fo Koruri/VlKoruri.](https://gist.github.com/lindwurm/b24657c335bb11a520c4/9461c1690188ddd2b6d721467653e6e0072689b8)
    * [第332回　Webフォントをつくろう：Ubuntu Weekly Recipe｜gihyo.jp … 技術評論社](http://gihyo.jp/admin/serial/01/ubuntu-recipe/0332?page=2)
    * [fontforge でフォントのサブセットを生成する - Möbius Flyer](https://blog.alprosys.com/2016/03/28/genwebfonts/)
    * [fontforge.font Python Example](https://www.programcreek.com/python/example/106105/fontforge.font)
    * [fontforge.open Python Example](https://www.programcreek.com/python/example/106104/fontforge.open)
    * [Kennyl/python-fontforge-script: Python Script for Font Manipulation using FontForge Module](https://github.com/Kennyl/python-fontforge-script)
    * [Creating Fonts with Inkscape and FontForge | Part#10 : neography](https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/)
* FontForgeによる複合グリフの生成
    * [Building accented glyphs](https://fontforge.github.io/editexample4.html#accents)
    * [FontForge -- An outline font editor](https://fontforge.github.io/overview.html#References)
    * [Design With FontForge: Diacritics and Accents](http://designwithfontforge.com/en-US/Diacritics_and_Accents.html)
    * [Create Composite Glyphs - Font Forum](https://forum.high-logic.com/viewtopic.php?t=173)
    * [Developer - Custom accent-placers](http://fontforge.10959.n7.nabble.com/Custom-accent-placers-td5400.html)
    * [Developer - handling anchor points](http://fontforge.10959.n7.nabble.com/handling-anchor-points-td1221.html)
    * [fontforge - Making a Glyph of more than one unicode character - Stack Overflow](https://stackoverflow.com/questions/45699560/making-a-glyph-of-more-than-one-unicode-character)
* ルビ
    * [Furigana - Wikipedia](https://en.wikipedia.org/wiki/Furigana)
    * [ルビの組版 その1 - JAGAT](https://www.jagat.or.jp/past_archives/content/view/3827.html)
    * [ルビにもルールがある　～文字組版の基本（後半）～](http://www.tairapromote.com/2016/10/10/ruby_rule/)
* ルビの書式
    * [青空文庫作業マニュアル【入力編】](https://www.aozora.gr.jp/aozora-manual/index-input.html#markup)
    * [小説家になろう - ルビを振る｜マニュアル](https://syosetu.com/man/ruby/)
    * [ルビや傍点を付ける（カクヨム記法を使う） - カクヨムヘルプセンター](https://kakuyomu.jp/help/entry/notation)
    * [ルビを振る - 吉里吉里講座](http://novel.yukigesho.com/kirikiri/a014.htm)
* 正規表現
    * [分かりやすいpythonの正規表現の例 - Qiita](https://qiita.com/luohao0404/items/7135b2b96f9b0b196bf3)
    * [正規表現サンプル(かっこで囲まれた文字を検索する)](http://hodade.com/seiki/page.php?s_kakko)
* 合字（Ligature）
    * [【完全版】Ligature Symbols フォントセットの自作方法 - くらげだらけ](http://kudakurage.hatenadiary.com/entry/20120720/1342749116)
    * [ligature(合字）アイコンを作る - Qiita](https://qiita.com/itoz/items/778cff14344da6f1743a)
    * [Fontforge Scripting how to add ligatures for a glyph - Stack Overflow](https://stackoverflow.com/questions/10902593/fontforge-scripting-how-to-add-ligatures-for-a-glyph)
    * [Manipulating OpenType Lookups](https://fontforge.github.io/lookups.html)
* その他
    * [The FreeType Project](https://www.freetype.org/)
    * [Programming library for editing ttf fonts - Stack Overflow](https://stackoverflow.com/questions/7686360/programming-library-for-editing-ttf-fonts)

[1]:https://ja.wikipedia.org/wiki/%E7%A7%81%E7%94%A8%E9%9D%A2
[2]:https://fontforge.github.io/