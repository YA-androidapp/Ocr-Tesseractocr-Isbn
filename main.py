#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
#
# Required:
#  $ sudo apt install -y libtesseract-dev tesseract-ocr && pip install pillow pyocr

from PIL import Image, ImageDraw, ImageFilter  # , ImageOps
import pyocr
import pyocr.builders
import re
import sys


ISBN_PREFIX = '978'

INPUT_FILENAME = 'input.jpg'
OUTPUT_FILENAME = 'result_{:0=3}.jpg'


def init():
    available_tools = pyocr.get_available_tools()
    if len(available_tools) == 0:
        print('aptでtesseract-ocrをインストールしてください')
        sys.exit(1)
    else:
        for available_tool in available_tools:
            print('available_tool: %s' % available_tools)

    available_tool = available_tools[0]
    print('available_tool: \'%s\'を使用します' % available_tool)

    available_languages = available_tool.get_available_languages()
    if len(available_languages) == 0:
        print('利用できる言語がありません')
        sys.exit(1)
    else:
        for available_language in available_languages:
            print('available_language: %s' % available_language)

    available_language = available_languages[0]
    print('available_languages: \'%s\'を使用します' % (available_language))

    return available_tool, available_language


def preproc(filename):
    img = Image.open(filename)

    imgs = []

    # 画像処理
    for i in range(20):
        imgs.append(img.copy().rotate(i - 10))

    print(len(imgs))

    # for

    # img = img.convert('L') # グレースケール
    # img = img.quantize(16) # 減色
    # img = img.convert('RGB') # 減色した場合は変換してRGBに戻す

    # img = img.filter(ImageFilter.SHARPEN) # 鮮鋭化

    # img = img.filter(ImageFilter.GaussianBlur(1)) # ガウシアンフィルタ

    # img = img.filter(ImageFilter.MedianFilter(1)) # メディアンフィルタ

    # img = ImageOps.equalize(img) # 平均化

    # img = img.point(lambda x: 0 if x < 100 else x) # 二値化
    # img = img.point(lambda x: 0 if x < 100 else 255 if x > 185 else 200)

    # 画像処理

    return imgs


def main(tool, lang, img, i):
    isbns = []

    result_img = img.copy()

    result_text = tool.image_to_string(
        img,
        lang=lang,
        builder=pyocr.builders.DigitLineBoxBuilder(tesseract_layout=6)
    )

    draw = ImageDraw.Draw(result_img)

    for item in result_text:
        content = re.sub(r'[^0-9]+', '', str(item.content))
        if content.find(ISBN_PREFIX) > -1 and len(content) >= 13:
            print('{}: content: {}, position: {}'.format(i, item.content, item.position))

            isbn = content[content.find(ISBN_PREFIX):]
            if len(isbn) > 13:
                isbn = isbn[0:13]
            # print('isbn: {}'.format(isbn))

            clr = (255, 255, 255)
            if checkdigit(isbn):
                clr = (255, 0, 0)
                isbns.append(isbn)

            # print('clr: {}'.format(clr))

            position = ()
            for r in item.position:
                position = position + r

            draw.rectangle(position, outline=clr)  # カラーの時
            # draw.rectangle(position) # グレースケールの時

            draw.text((item.position)[0], text=isbn, fill=clr)  # カラーの時
            # draw.text((item.position)[0], text=isbn) # グレースケールの時

    result_img.save(OUTPUT_FILENAME.format(i))
    result_img = None

    return isbns


def checkdigit(code):
    s = str(code)[:12]
    a = b = 0

    for i in range(0, len(s), 2):
        a += int(s[i])

    for i in range(1, len(s), 2):
        b += int(s[i])

    d = 10 - ((a + (b * 3)) % 10)
    d = 0 if d == 10 else d

    return d == int(str(code)[12:])


if __name__ == '__main__':
    tool, lang = init()
    imgs = preproc(INPUT_FILENAME)

    result = []
    i = 0
    for img in imgs:
        result.extend(main(tool, lang, img, i))
        i += 1

    result = list(set(result))  # 重複除去
    print(','.join(result))
