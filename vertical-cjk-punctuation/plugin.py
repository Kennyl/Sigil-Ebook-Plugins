#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys
import sigil_bs4


conversionDict={
                "\N{FULLWIDTH HYPHEN-MINUS}": "\N{FULLWIDTH VERTICAL LINE}",
                "\N{BOX DRAWINGS LIGHT HORIZONTAL}": "\N{BOX DRAWINGS LIGHT VERTICAL}",
                "\N{HORIZONTAL ELLIPSIS}": "\N{VERTICAL ELLIPSIS}",
                "\N{MIDLINE HORIZONTAL ELLIPSIS}": "\N{VERTICAL ELLIPSIS}",
                }


def fixSelfCloseTags(html):
    return html.replace("></input>"," />").replace("></img>"," />").replace("></meta>"," />").replace("></link>"," />").replace("<br></br>","<br />").replace("></img>"," />")


def run(bk):
    print('start')
    for (id, href) in bk.text_iter():
        modified = False
        html = bk.readfile(id)
        # html = html.replace("<br/>","")
        soup = sigil_bs4.BeautifulSoup(html)
        # br tag  will cause p tag cannot be found
        for elem in soup.findAll(['p','div','span'], text=re.compile("["+"".join(conversionDict.keys())+"]")):
            modified = True
            text = elem.string
            for key in conversionDict:
                text = re.sub("["+key+"]", conversionDict[key], text)
            elem.string.replace_with(text)
            # print(elem.string)
        if modified:
            print("Modifed File -> ", id)
            bk.writefile(id, fixSelfCloseTags(str(soup)))
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
