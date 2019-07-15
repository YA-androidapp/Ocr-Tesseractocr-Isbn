#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
#
# Required:
#  $ sudo apt install -y libtesseract-dev tesseract-ocr && pip install pillow pyocr

from PIL import Image, ImageDraw
import sys
import pyocr
import pyocr.builders


INPUT_FILENAME = 'input.jpg'
OUTPUT_FILENAME = 'result.jpg'


def init():
    available_tools = pyocr.get_available_tools()
    if len(available_tools) == 0:
        print("aptでtesseract-ocrをインストールしてください")
        sys.exit(1)
    else:
        for available_tool in available_tools:
            print("available_tool: %s" % available_tools)

    available_tool = available_tools[0]
    print("available_tool: '%s'を使用します" % available_tool)

    available_languages = available_tool.get_available_languages()
    if len(available_languages) == 0:
        print("利用できる言語がありません")
        sys.exit(1)
    else:
        for available_language in available_languages:
            print("available_language: %s" % available_language)

    available_language = available_languages[0]
    print("available_languages: '%s'を使用します" % (available_language))

    return available_tool, available_language


def preproc(filename):
    img = Image.open(filename)

    # 画像処理

    # 画像処理

    img_filtered = img

    return img_filtered


def main(tool, lang, img):
    result_img = img.copy()

    result_text = tool.image_to_string(
        img,
        lang=lang,
        builder=pyocr.builders.DigitLineBoxBuilder(tesseract_layout=6)
    )

    draw = ImageDraw.Draw(result_img)

    for item in result_text:
        print("content: {}, position: {}".format(item.content, item.position))

        position = ()
        for r in item.position:
            position = position + r

        draw.rectangle(position, outline=(255, 0, 0))

        draw.text((item.position)[0], text=item.content, fill=(255,0,0))

    result_img.save(OUTPUT_FILENAME)

    return result_text


if __name__ == "__main__":
    tool, lang = init()
    img = preproc(INPUT_FILENAME)
    main(tool, lang, img)
