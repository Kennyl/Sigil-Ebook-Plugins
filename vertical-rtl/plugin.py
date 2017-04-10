#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import sys
from lxml import etree, html


def run(bk):
    count = 0
    print('start')
    for (id, href) in bk.text_iter():
        modified = True
        html_original = bk.readfile(id)
        doc = html.fromstring(html_original.encode("utf-8"))
        for link in doc.xpath("//*[local-name() = 'link']"):
            if link['href'] == "../Styles/t2bv2l.css":
                modified= False
                break

        if modified:
            count += 1
            head = doc.xpath("//*[local-name() = 'head']")[0]
            link = etree.SubElement(head, "link", attrib={'href': "../Styles/t2bv2l.css",
                                                          'rel': "stylesheet",
                                                          'type': "text/css"
                                                         })
            print("Modified File : ", id)
            bk.writefile(id, etree.tostring(doc, encoding="utf-8", xml_declaration=True).decode('utf8'))

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
