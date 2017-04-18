#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys
import sigil_bs4

conversionDict={"0": "\N{FULLWIDTH DIGIT ZERO}",
                "1": "\N{FULLWIDTH DIGIT ONE}",
                "2": "\N{FULLWIDTH DIGIT TWO}",
                "3": "\N{FULLWIDTH DIGIT THREE}",
                "4": "\N{FULLWIDTH DIGIT FOUR}",
                "5": "\N{FULLWIDTH DIGIT FIVE}",
                "6": "\N{FULLWIDTH DIGIT SIX}",
                "7": "\N{FULLWIDTH DIGIT SEVEN}",
                "8": "\N{FULLWIDTH DIGIT EIGHT}",
                "9": "\N{FULLWIDTH DIGIT NINE}"}


def fixSelfCloseTags(html):
    return html.replace("></input>"," />").replace("></img>"," />").replace("></meta>"," />").replace("></link>"," />").replace("<br></br>","<br />").replace("></img>"," />")


def run(bk):
    print('start')
    for (file_id, _) in bk.text_iter():
        modified = False
        html = bk.readfile(file_id)
        soup = sigil_bs4.BeautifulSoup(html)
        # br tag  will cause p tag cannot be found
        for elem in soup.findAll(['p','div','span'], text=re.compile('(\d+)')):
            modified = True
            text = elem.string
            for key in conversionDict:
                text = re.sub(key, conversionDict[key], text)
            elem.string.replace_with(text)
            # print(elem.string)
        if modified:
            print("Modifed File -> ", id)
            bk.writefile(file_id, fixSelfCloseTags(str(soup)))
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
