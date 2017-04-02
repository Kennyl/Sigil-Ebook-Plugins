#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys


def run(bk):
    print('start')
    for (id, href) in bk.text_iter():
        modified = False
        html = bk.readfile(id)
		html = html.replace("<br/>","")
        soup = gumbo_bs4.parse(html)
        ol = sigil_bs4.Tag(name="ol")
        ol['class'] = "sigil-footnote-content"
        # br tag  will cause p tag cannot be found
        for elem in soup.findAll(['p','div','span'], text=re.compile('(\d+)')):
            modified = True
            text = elem.string
            text = re.sub("0", "\N{FULLWIDTH DIGIT ZERO}", text)
            text = re.sub("1", "\N{FULLWIDTH DIGIT ONE}", text)
            text = re.sub("2", "\N{FULLWIDTH DIGIT TWO}", text)
            text = re.sub("3", "\N{FULLWIDTH DIGIT THREE}", text)
            text = re.sub("4", "\N{FULLWIDTH DIGIT FOUR}", text)
            text = re.sub("5", "\N{FULLWIDTH DIGIT FIVE}", text)
            text = re.sub("6", "\N{FULLWIDTH DIGIT SIX}", text)
            text = re.sub("7", "\N{FULLWIDTH DIGIT SEVEN}", text)
            text = re.sub("8", "\N{FULLWIDTH DIGIT EIGHT}", text)
            text = re.sub("9", "\N{FULLWIDTH DIGIT NINE}", text)
        if modified:
            print("Modifed File -> ", id)
            bk.writefile(id, html)
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
