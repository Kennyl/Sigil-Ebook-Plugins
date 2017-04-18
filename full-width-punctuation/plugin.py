#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys
import sigil_bs4

# change ;:,?!. to full width
conversionDict={
                ";": "\N{FULLWIDTH SEMICOLON}",
                ":": "\N{FULLWIDTH COLON}",
                ",": "\N{FULLWIDTH COMMA}",
                "?": "\N{FULLWIDTH QUESTION MARK}",
                "!": "\N{FULLWIDTH EXCLAMATION MARK}",
                ".": "\N{FULLWIDTH FULL STOP}"
                }


def fixSelfCloseTags(html):
    return html.replace("></input>"," />").replace("></img>"," />").replace("></meta>"," />").replace("></link>"," />").replace("<br></br>","<br />").replace("></img>"," />")


def run(bk):
    print('start')
    for (file_id, _) in bk.text_iter():
        modified = False
        html = bk.readfile(file_id)
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
            bk.writefile(file_id, fixSelfCloseTags(str(soup)))
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
