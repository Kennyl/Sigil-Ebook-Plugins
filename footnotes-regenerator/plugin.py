#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import re
from lxml import etree, html

'''

Markdown Extra style change footnote to epub:type=footnote
Example.
Note Reference [^1]

[^2]: Footnote

'''

def runLXML(bk):
    useNumberOrderingInsteadOfIdeograph = True
    noteref_re = r'([^>])(\[\^\d+\])([^:])'
    footnote_re = r'^(\[[\^]\d+\]):'
    #old
    # noteref_re = r'[^>](\[\d+\])'
    # footnote_re = r'^(\[[]\d+\])'
    nref_id = 0
    fn_id = 0
    modified = False
    for (file_id, _) in bk.text_iter():
        if nref_id != fn_id:
            print("\nReference ID desync, restart at %s." % str(fn_id))
            nref_id = fn_id
        html_original = bk.readfile(file_id)
        doc = html.fromstring(html_original.encode("utf-8"))
        doc.attrib['xmlns:epub'] = 'http://www.idpf.org/2007/ops'
        ol = etree.SubElement(doc.xpath("//*[local-name() = 'body']")[0],
                              "ol",
                              attrib={"class": "duokan-footnote-content"})
        pathsearch = "//*[local-name()='p' or local-name()='div' or local-name()='span']"
        elements = doc.xpath(pathsearch)
        for elem in elements:
            innerText = elem.text
            if innerText is None:
                continue
            found_noteref = re.search(noteref_re, innerText)
            while found_noteref is not None:
                modified = True
                nref_id += 1
                innerText = re.sub(noteref_re,
                                   r'\1<a class="duokan-footnote" href="#fn'+str(nref_id)+r'" id="fnref'+str(nref_id)+r'"></a>\3',
                                   innerText,
                                   1)
                # if useNumberOrderingInsteadOfIdeograph:
                #     innerText = re.sub(r'([^>])\[\d+\]',r'\1<a class="duokan-footnote" href="#fn'+str(nref_id)+'" id="fnref'+str(nref_id)+
                #                        '">['+str(nref_id)+']</a>',innerText,1)
                # else:
                #     innerText = re.sub(r'([^>])\[\d+\]',r'\1<a class="duokan-footnote" href="#fn'+str(nref_id)+'" id="fnref'+str(nref_id)+
                #                        '">注</a>',innerText,1)
                found_noteref = re.search(noteref_re,
                                          innerText)

            if elem.text != innerText:
                elem.getparent().replace(elem,etree.XML("<"+elem.tag+">"+innerText+"</"+elem.tag+">"))

            found_footnote = re.search(footnote_re, innerText)
            if found_footnote is not None:
                modified = True
                fn_id += 1
                aside = etree.SubElement(ol,
                                         "aside",
                                         attrib={"epub:type": "footnote"})
                xml = etree.XML('<li class="duokan-footnote-item" id="fn'+str(fn_id)+
                                '">\n<p class="fn"><a href="'+str(id)+'#fnref'+str(fn_id)+
                                '"></a> '+innerText[found_footnote.end():]+
                                '<a href="'+str(id)+'#fnref'+str(fn_id)+'"></a></p>\n</li>')
                # if useNumberOrderingInsteadOfIdeograph:
                #     xml = etree.XML('<li class="duokan-footnote-item" id="fn'+str(fn_id)+'">\n<p class="fn"><a href="'+str(id)+'#fnref'+str(fn_id)+
                #                     '">['+str(fn_id)+']</a> '+innerText[found_footnote.end():]+'&#8203;​​​​​​​​</p>\n</li>')
                # else:
                #     xml = etree.XML('<li class="duokan-footnote-item" id="fn'+str(fn_id)+'">\n<p class="fn"><a href="'+str(id)+'#fnref'+str(fn_id)+
                #                     '">原文</a>：'+innerText[found_footnote.end():]+'&#8203;​​​​​​​​</p>\n</li>')
                aside.append(xml)
                elem.getparent().remove(elem)
#add back epub:type avoid mulitple namespace in XML create
        for a in  elem.xpath("//*[contains(@class, 'duokan-footnote')]"):
            a.attrib['epub:type']= "noteref"

        if modified:
            # head = doc.xpath("//*[local-name() = 'head']")[0]
            head = doc.xpath("//*[local-name() = 'head']")[0]
            etree.SubElement(head,
                             "link",
                             attrib={'href': "../Styles/footnote.css",
                                     'rel': "stylesheet",
                                     'type': "text/css"
                                    })
            bk.writefile(file_id,
                         etree.tostring(
                             doc,
                             encoding="utf-8",
                             xml_declaration=True).decode('utf8'))
        modified = False
#css
    if nref_id > 0:
        if useNumberOrderingInsteadOfIdeograph:
            cssdata = '''
body{
    counter-reset:footref-index;
}
a.duokan-footnote::before{
    content: "(";
}
a.duokan-footnote::after{
    counter-increment: footref-index;
    content: counter(footref-index) ")";
}
a.duokan-footnote {
    line-height: 1;
    vertical-align: super;
    text-decoration: none;
    height: auto;
    font-size: 0.5em;
    border: 0;
    background: black;
    color: white;
    border-radius: 50%;
    -moz-border-radius: 50%;
    -webkit-border-radius: 50%;
}

ol {
    list-style: none;
}
li {
    text-decoration: none;
}
.duokan-footnote-content{
    counter-reset:footnote-index;
}
.duokan-footnote-item {
    margin: 0 0.6em;
    line-height: 130%;
    text-indent: 2em;
    font-weight: bold;
    font-size: 0.95em;
    text-align: justify;
}
.duokan-footnote-item a:first-of-type{
    text-decoration: none;
    background: black;
    color: white;
    border-radius: 50%;
    -moz-border-radius: 50%;
    -webkit-border-radius: 50%;
}
.duokan-footnote-item a:first-of-type::before{
    content: "[";
}
.duokan-footnote-item a:first-of-type::after{
    counter-increment: footnote-index;
    content: counter(footnote-index) "]";
}
.duokan-footnote-item a:last-of-type::before{
    content: "";
}
.duokan-footnote-item a:last-of-type::after{
    content: "\N{LEFTWARDS ARROW WITH HOOK}";
}
.fn {
    text-indent: 0;
}'''
        else:
            cssdata = '''
a.duokan-footnote::before{
    content: "";
}
a.duokan-footnote::after{
    content: "注 ";
}
a.duokan-footnote {
    line-height: 1;
    vertical-align: super;
    text-decoration: none;
    height: auto;
    border: 0;
    font-size: 0.5em;
    background: black;
    color: white;
    border-radius: 50%;
    -moz-border-radius: 50%;
    -webkit-border-radius: 50%;
}

ol {
    list-style: none;
}
li {
    text-decoration: none;
}
.duokan-footnote-item {
    margin: 0 0.6em;
    line-height: 130%;
    text-indent: 2em;
    font-weight: bold;
    font-size: 0.95em;
    text-align: justify;
}
.duokan-footnote-item a:first-of-type{
    text-decoration: none;
    background: black;
    color: white;
    border-radius: 50%;
    -moz-border-radius: 50%;
    -webkit-border-radius: 50%;
}
.duokan-footnote-item a:first-of-type::before{
    content: "";
}
.duokan-footnote-item a:first-of-type::after{
    content: "釋：";
}

.duokan-footnote-item a:last-of-type::before{
    content: "";
}
.duokan-footnote-item a:last-of-type::after{
    content:  "\N{LEFTWARDS ARROW WITH HOOK}";
}
.fn {
    text-indent: 0;
}'''
        basename = "footnote.css"
        uid = "footnotecss"
        mime = "text/css"
        bk.addfile(uid, basename, cssdata, mime)
    return 0

def run(bk):
    return runLXML(bk)


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
