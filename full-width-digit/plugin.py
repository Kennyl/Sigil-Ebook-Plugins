#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys


def run(bk):
    print('start')
    for (id, href) in bk.text_iter():
        html = bk.readfile(id)
        old_html = html
        html = re.sub("0", "\N{FULLWIDTH DIGIT ZERO}", html)
        html = re.sub("1", "\N{FULLWIDTH DIGIT ONE}", html)
        html = re.sub("2", "\N{FULLWIDTH DIGIT TWO}", html)
        html = re.sub("3", "\N{FULLWIDTH DIGIT THREE}", html)
        html = re.sub("4", "\N{FULLWIDTH DIGIT FOUR}", html)
        html = re.sub("5", "\N{FULLWIDTH DIGIT FIVE}", html)
        html = re.sub("6", "\N{FULLWIDTH DIGIT SIX}", html)
        html = re.sub("7", "\N{FULLWIDTH DIGIT SEVEN}", html)
        html = re.sub("8", "\N{FULLWIDTH DIGIT EIGHT}", html)
        html = re.sub("9", "\N{FULLWIDTH DIGIT NINE}", html)
        if html != old_html:
            print("Modifed ", id)
            bk.writefile(id, html)
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
