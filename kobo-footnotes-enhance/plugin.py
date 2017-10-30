#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import re
from lxml import etree, html
# '''
# this plugin will link (校記1）<-> section ■校記 of 1
# and （注釋2）<-> section ■注釋 of 2
# '''


def run(bk):
    modified = False
# all xhtml/html files - moves found notes to end of file, insert a link
# in the text and link to css in the files with notes
    step = 1  # 1 for footnote #2 For 校記 #3 for noteref
    for (file_id, href) in bk.text_iter():
        step = 1
        modified = False
        print("id ", file_id, "href ", href)
        if href == "Text/nav.xhtml" or href == "Text/000-cover.xhtml":
            continue
        content = bk.readfile(file_id)
        doc = html.fromstring(content.encode('utf-8'))
        doc.attrib['xmlns:epub'] = 'http://www.idpf.org/2007/ops'
        pathsearch = "//*[local-name()='p' or local-name()='div' or local-name()='span']"
        elements = doc.xpath(pathsearch)
        for e in elements:
            innerText = e.text
            if innerText is None or innerText == "":
                continue
            if e.text == "■校記" or e.text == "■校注":
                step = 2
            if e.text == "■注釋" or e.text == "■註釋":
                step = 3
            if step == 1:
                original = innerText
                innerText = re.sub(
                    r'（校記(\d+)）',
                    r'<a class="duokan-footnote footnote2" href="#fx\1"  id="fxref\1">\1</a>',
                    innerText)
                innerText = re.sub(
                    r'（校注(\d+)）',
                    r'<a class="duokan-footnote footnote2" href="#fx\1"  id="fxref\1">\1</a>',
                    innerText)
                innerText = re.sub(
                    r'（注釋(\d+)）',
                    r'<a class="duokan-footnote footnote1" href="#fn\1"  id="fnref\1">\1</a>',
                    innerText)
                innerText = re.sub(
                    r'（註釋(\d+)）',
                    r'<a class="duokan-footnote footnote1" href="#fn\1"  id="fnref\1">\1</a>',
                    innerText)
                if original != innerText:
                    modified = True
                    # print(innerText)
                    e.getparent().replace(e, etree.XML("<" + e.tag + ">" + innerText + "</" + e.tag + ">"))
            if step == 2:
                match = re.search("^(\d+)", innerText)
                if match is not None:
                    innerText = re.sub(
                        r'^(\d+)',
                        r'<a class="duokan-footnote-item footnote-item2" href="#fxref\1"  id="fx\1">\1</a>',
                        innerText)
                    # print("校記", innerText)
                    e.getparent().replace(e, etree.XML("<" + e.tag + ">" + innerText + "</" + e.tag + ">"))
            if step == 3:
                match = re.search("^(\d+)", innerText)
                if match is not None:
                    innerText = re.sub(
                        r'^(\d+)',
                        r'<a class="duokan-footnote-item footnote-item1" href="#fnref\1"  id="fn\1">\1</a>',
                        innerText)
                    # print("注釋 ", innerText)
                    e.getparent().replace(e, etree.XML("<" + e.tag + ">" + innerText + "</" + e.tag + ">"))
        # for a in doc.xpath("//*[contains(@class, 'duokan-footnote footnote1')]"):
        #     a.attrib['epub:type'] = "noteref"
        # for a in doc.xpath("//*[contains(@class, 'duokan-footnote-item footnote-item1')]"):
        #     a.getparent().attrib['epub:type'] = "footnote"
        if modified:
            head = doc.xpath("//*[local-name() = 'head']")[0]
            link = etree.Element("link")
            link.attrib['href'] = "../Styles/kobo-enhance-footnote.css"
            link.attrib['rel'] = "stylesheet"
            link.attrib['type'] = "text/css"
            head.append(link)
            bk.writefile(file_id, etree.tostring(
                doc, xml_declaration=True, encoding="utf-8"))

    cssdata = '''
a.duokan-footnote-item{
text-decoration: none;
background: black;
color: white;
border-radius: 75%;
-moz-border-radius: 75%;
-webkit-border-radius: 75%;
}

a.duokan-footnote {
line-height: 1;
vertical-align: super;
text-decoration: none;
font-size: 0.5em;
height: auto;
border: 0;
background: black;
color: white;
border-radius: 75%;
-moz-border-radius: 75%;
-webkit-border-radius: 75%;
}
a.footnote1::before{
content: "(";
}
a.footnote1::after{
content: ")";
}
a.footnote2::before{
content: "(校";
}
a.footnote2::after{
content: ")";
}

a.footnote-item1::before{
content: "(";
}
a.footnote-item1::after{
content: ")";
}
a.footnote-item2::before{
content: "(";
}
a.footnote-item2::after{
content: ")";
}
'''
    cssfilename = "kobo-enhance-footnote.css"
    uid = "koboenhancefootnotecss"
    mime = "text/css"
    bk.addfile(uid, cssfilename, cssdata, mime)
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
