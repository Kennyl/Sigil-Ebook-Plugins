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
    previewConstant = 10
    lastid = 0
    fnid = 0
    fnid1 = 0
    modified = False
    for (id, href) in bk.text_iter():
        if fnid != fnid1:
            print("\nReference ID desync, restart at %s." % str(fnid1))
            fnid = fnid1
        html_original = bk.readfile(id)
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
                fnid += 1
                innerText = re.sub(noteref_re,
                                   r'\1<a class="duokan-footnote" href="#fn'+str(fnid)+r'" id="fnref'+str(fnid)+r'"></a>\3',
                                   innerText,
                                   1)
                # if useNumberOrderingInsteadOfIdeograph:
                #     innerText = re.sub(r'([^>])\[\d+\]',r'\1<a class="duokan-footnote" href="#fn'+str(fnid)+'" id="fnref'+str(fnid)+
                #                        '">['+str(fnid)+']</a>',innerText,1)
                # else:
                #     innerText = re.sub(r'([^>])\[\d+\]',r'\1<a class="duokan-footnote" href="#fn'+str(fnid)+'" id="fnref'+str(fnid)+
                #                        '">注</a>',innerText,1)
                found_noteref = re.search(noteref_re,
                                          innerText)

            if elem.text != innerText:
                elem.getparent().replace(elem,etree.XML("<"+elem.tag+">"+innerText+"</"+elem.tag+">"))

            found_footnote = re.search(footnote_re, innerText)
            if found_footnote is not None:
                modified = True
                fnid1 += 1
                aside = etree.SubElement(ol,
                                         "aside",
                                         attrib={"epub:type": "footnote"})
                xml = etree.XML('<li class="duokan-footnote-item" id="fn'+str(fnid1)+
                                '">\n<p class="fn"><a href="'+str(id)+'#fnref'+str(fnid1)+
                                '"></a> '+innerText[found_footnote.end():]+
                                '<a href="'+str(id)+'#fnref'+str(fnid1)+'"></a></p>\n</li>')
                # if useNumberOrderingInsteadOfIdeograph:
                #     xml = etree.XML('<li class="duokan-footnote-item" id="fn'+str(fnid1)+'">\n<p class="fn"><a href="'+str(id)+'#fnref'+str(fnid1)+
                #                     '">['+str(fnid1)+']</a> '+innerText[found_footnote.end():]+'&#8203;​​​​​​​​</p>\n</li>')
                # else:
                #     xml = etree.XML('<li class="duokan-footnote-item" id="fn'+str(fnid1)+'">\n<p class="fn"><a href="'+str(id)+'#fnref'+str(fnid1)+
                #                     '">原文</a>：'+innerText[found_footnote.end():]+'&#8203;​​​​​​​​</p>\n</li>')
                aside.append(xml)
                elem.getparent().remove(elem)
#add back epub:type avoid mulitple namespace in XML create
        for a in  elem.xpath("//*[contains(@class, 'duokan-footnote')]"):
            a.attrib['epub:type']= "noteref"

        if modified:
            # head = doc.xpath("//*[local-name() = 'head']")[0]
            head = doc.xpath("//*[local-name() = 'head']")[0]
            link = etree.SubElement(head,
                                    "link",
                                    attrib={'href': "../Styles/footnote.css",
                                            'rel': "stylesheet",
                                            'type': "text/css"
                                           })
            # head.append(link)
            bk.writefile(id,
                         etree.tostring(
                             doc,
                             encoding="utf-8",
                             xml_declaration=True).decode('utf8'))
        modified = False
        lastid = id
#css
    if fnid > 0:
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


# #old logic using BeautifulSoup
# def runBS(bk):
#     useNumberOrderingInsteadOfIdeograph = False
#     previewConstant = 10
#     lastid = 0
#     fnid = 0
#     fnid1 = 0
#     modified = False
# # all xhtml/html files - moves found notes to end of file, insert a link in the text and link to css in the files with notes
#     for (id, href) in bk.text_iter():
#         if fnid != fnid1:
#             print("\nReference ID desync, restart at %s." % str(fnid1))
#             fnid = fnid1
#         html = bk.readfile(id)
#         html = html.replace("<br/>","")
#         soup = sigil_bs4.BeautifulSoup(html, "lxml")
#         ol = sigil_bs4.Tag(name="ol")
#         ol['class'] = "duokan-footnote-content"
#         # br tag  will cause p tag cannot be found
#         for elem in soup.findAll(['p', 'div', 'span'], text=re.compile('.+(\[\d+\])')):
#             modified = True
#             fnid = fnid + 1
#             text =  elem.string
#             elem.clear()
#             match = re.search(r'(\[\d+\])', text)
#             while match is not None:
#                 start, end = match.start(), match.end()
#                 elem.append(text[:start])
#                 a = sigil_bs4.Tag(name="a")
#                 a["class"] = "duokan-footnote"
#                 a["epub:type"]= "noteref"
#                 a["href"]='#fn'+str(fnid)
#                 a["id"] = "fnref"+str(fnid)
#                 if useNumberOrderingInsteadOfIdeograph:
#                     a.string = "["+str(fnid)+"]"
#                 else:
#                     a.string = "注"
#                 elem.append(a)
#                 preview = 0
#                 if start > previewConstant:
#                     preview = start - previewConstant
#                 print("\n", id, href, str(fnid), ':', text[preview:start])
#                 text = text[end:]
#                 match = re.search(r'(\[\d+\])', text)
#                 if match is None:
#                     elem.append(text)
#                 else:
#                     fnid = fnid + 1
#
#         for elem in soup.findAll(['p', 'div', 'span'], text=re.compile('^\[\d+\]')):
#             modified = True
#             fnid1 = fnid1 + 1
#             print("\n", id, href, '', str(fnid1), ':', elem.string)
#             text =  elem.string
#             e = elem.extract()
#             e.clear()
#             match = re.search(r'(\[\d+\])', text)
#             aside = sigil_bs4.Tag(name="aside")
#             aside["epub:type"] = "footnote"
#             li = sigil_bs4.Tag(name="li")
#             li['class'] = "duokan-footnote-item"
#             li['id'] = 'fn'+str(fnid1)
#             a = sigil_bs4.Tag(name="a")
#             a['href'] = str(id)+'#fnref'+str(fnid1)
#             if useNumberOrderingInsteadOfIdeograph:
#                 a.string = '['+str(fnid1)+']'
#                 e.append(a)
#                 e.append(text[match.end():])
#             else:
#                 a.string = "原文"
#                 e.append(a)
#                 e.append("：" + text[match.end():])
#             li.append(e)
#             aside.append(li)
#             ol.append(aside)
#         if modified:
#             soup.html.attrs['xmlns:epub'] = 'http://www.idpf.org/2007/ops'
#             link = sigil_bs4.Tag(name="link")
#             link['href'] = "../Styles/footnote.css"
#             link['rel'] = "stylesheet"
#             link['type'] = "text/css"
#             soup.html.head.append(link)
#             soup.html.body.append(ol)
#             # dunno why sigil cannot have valid close tag
#             html = fixSelfCloseTags(str(soup))
#             bk.writefile(id,html)
#         modified = False
#         lastid = id
# #css
#     if fnid > 0:
#         cssdata = '''.duokan-footnote-item {
#     margin: 0 0.6em;
#     line-height: 130%;
#     text-indent: 2em;
#     font-weight: bold;
#     font-size: 0.95em;
#     text-align: justify;
# }
# .duokan-footnote-item a{
#     text-decoration: none;
#     background: black;
#     color: white;
#     border-radius: 50%;
#     -moz-border-radius: 50%;
#     -webkit-border-radius: 50%;
# }
# .fn {
#     text-indent: 0;
# }
# a.duokan-footnote {
#     line-height: 1;
#     vertical-align: super;
#     text-decoration: none;
#     height: auto;
#     border: 0;
#     background: black;
#     color: white;
#     border-radius: 50%;
#     -moz-border-radius: 50%;
#     -webkit-border-radius: 50%;
# }
# ol {
#     list-style: none;
# }
# li {
#     text-decoration: none;
# }'''
#         basename = "footnote.css"
#         uid = "footnotecss"
#         mime = "text/css"
#         bk.addfile(uid, basename, cssdata, mime)
#     return 0


def run(bk):
    return runLXML(bk)


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
