#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys
import sigil_bs4


def fixSelfCloseTags(html):
    return html.replace("></input>"," />").replace("></img>"," />").replace("></meta>"," />").replace("></link>"," />").replace("<br></br>","<br />").replace("></img>"," />")


def run(bk):
    count = 0
    print('start')
    for (id, href) in bk.text_iter():
        modified = False
        html = bk.readfile(id)
        html = html.replace("<br/>","")
        soup = sigil_bs4.BeautifulSoup(html)
        print("id ", id)
        try:
            modified = 'sigil-t2bv2l' not in soup.body['class'].split()
        except KeyError:
            soup.body['class'] = ""
            modified = True
        if modified:
            count = 1
            link = sigil_bs4.Tag(name="link")
            link['href'] = "../Styles/t2bv2l.css"
            link['rel'] = "stylesheet"
            link['type'] = "text/css"
            soup.html.head.append(link)
            # soup.body['class'] = soup.body['class'] + " sigil-t2bv2l"
            # dunno why sigil cannot have valid close tag
            html = fixSelfCloseTags(str(soup))
            print(id)
            bk.writefile(id, html)

# css
        if count > 0:
            cssdata = '''
html{
    direction:rtl;
}
body {
    direction:ltr;
    line-break: normal;
    -epub-line-break: normal;
    -webkit-line-break: normal;
    writing-mode: tb-rl;
    -epub-writing-mode: vertical-rl;
    -webkit-writing-mode: vertical-rl;
    -ms-writing-mode: vertical-rl;
    text-orientation: mixed;
    -webkit-text-orientation: mixed;
    -epub-text-orientation: mixed;
}'''
            basename = "t2bv2l.css"
            uid = "t2bv2lcss"
            mime = "text/css"
            bk.addfile(uid, basename, cssdata, mime)
    print('end')
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
