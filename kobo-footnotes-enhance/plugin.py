#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import, print_function
import sys
import re
from lxml import etree, html
import os


'''
this plugin will link (校記1）<-> section ■校記 of 1
and （注釋2）<-> section ■注釋 of 2
'''


def run(bk):
    modified = False
# all xhtml/html files - moves found notes to end of file, insert a link in the text and link to css in the files with notes
    step = 1 # 1 for footnote #2 For 校記 #3 for noteref
    for (id, href) in bk.text_iter():
        step = 1
        modified = False
        print("id ", id, "href ", href)
        if href == "Text/nav.xhtml" or href == "Text/000-cover.xhtml":
            continue
        content = bk.readfile(id)
        doc = html.fromstring(content.encode('utf-8'))
        pathsearch = "//*[local-name()='p' or local-name()='div' or local-name()='span']"
        elements = doc.xpath(pathsearch)
        for e in elements:
            innerText = e.text
            if innerText is None or innerText == "":
                continue
            if e.text == "■校記":
                step = 2
            if e.text == "■注釋":
                step = 3
            if step == 1:
                original = innerText
                innerText = re.sub(r'([^>])（校記(\d+)）',r'\1<a class="duokan-footnote" href="#fx\2"  id="fxref\2">（校記\2）</a>',innerText)
                innerText = re.sub(r'([^>])（注釋(\d+)）',r'\1<a class="duokan-footnote" href="#fn\2"  id="fnref\2">（注釋\2）</a>',innerText)
                if original  != innerText:
                    modified = True
                    # print(innerText)
                    e.getparent().replace(e, etree.XML("<"+e.tag+">"+innerText+"</"+e.tag+">"))
            if step == 2:
                match = re.search("^(\d+)", innerText)
                if match is not None:
                    innerText = re.sub(r'^(\d+)',r'<a class="duokan-footnote" href="#fxref\1"  id="fx\1">\1</a>',innerText)
                    # print("校記", innerText)
                    e.getparent().replace(e, etree.XML("<"+e.tag+">"+innerText+"</"+e.tag+">"))
            if step == 3:
                match = re.search("^(\d+)", innerText)
                if match is not None:
                    innerText = re.sub(r'^(\d+)',r'<a class="duokan-footnote" href="#fnref\1"  id="fn\1">\1</a>',innerText)
                    # print("注釋 ", innerText)
                    e.getparent().replace(e, etree.XML("<"+e.tag+">"+innerText+"</"+e.tag+">"))
        if modified:
            bk.writefile(id, etree.tostring(doc, xml_declaration=True, encoding="utf-8"))
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
