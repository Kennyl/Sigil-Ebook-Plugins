#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import, print_function
import sys
import re
import sigil_bs4

def fixSelfCloseTags(html):
    return html.replace("></link>","/>").replace("<br></br>","<br/>").replace("></img>","/>")

def run(bk):
    lastid = 0
    fnid = 0
    fnid1 = 0
    modified = False
# all xhtml/html files - moves found notes to end of file, insert a link in the text and link to css in the files with notes
    for (id, href) in bk.text_iter():
        if fnid != fnid1:
            print("\nReference ID desync, restart at %s." % str(fnid1))
            fnid = fnid1
        html = bk.readfile(id)
        html = html.replace("<br/>","")
        soup = sigil_bs4.BeautifulSoup(html, "lxml")
        ol = sigil_bs4.Tag(name="ol")
        ol['class'] = "sigil-footnote-content"
        # br tag  will cause p tag cannot be found
        for elem in soup.findAll(['p','div'], text=re.compile('.+(\[\d+\])')):
            modified = True
            fnid = fnid + 1
            text =  elem.string
            elem.clear()
            match = re.search(r'(\[\d+\])', text)
            while match is not None:
                start, end = match.start(), match.end()
                elem.append(text[:start])
                a = sigil_bs4.Tag(name="a")
                a["class"] = "sigil-footnote"
                a["epub:type"]= "noteref"
                a["href"]=str(id)+'#fn'+str(fnid)
                a["id"] = "fnref"+str(fnid)
                a.string = "["+str(fnid)+"]"
                elem.append(a)
                preview = 0
                if start > 10:
                    preview = start - 10
                print("\n", id, href, str(fnid), ':', text[preview:start])
                text = text[end:]
                match = re.search(r'(\[\d+\])', text)
                if match is None:
                    elem.append(text)
                else:
                    fnid = fnid + 1

        for elem in soup.findAll(['p','div'], text=re.compile('^\[\d+\]')):
            modified = True
            fnid1 = fnid1 + 1
            print("\n", id, href, '', str(fnid1), ':', elem.string)
            text =  elem.string
            e = elem.extract()
            e.clear()
            match = re.search(r'(\[\d+\])', text)
            aside = sigil_bs4.Tag(name="aside")
            aside["epub:type"] = "footnote"
            li = sigil_bs4.Tag(name="li")
            li['class'] = "sigil-footnote-item"
            li['id'] = 'fn'+str(fnid1)
            a = sigil_bs4.Tag(name="a")
            a['href'] = str(id)+'#fnref'+str(fnid1)
            a.string = '['+str(fnid1)+']'
            e.append(a)
            e.append(text[match.end():])
            li.append(e)
            aside.append(li)
            ol.append(aside)
        if modified:
            soup.html.attrs['xmlns:epub'] = 'http://www.idpf.org/2007/ops'
            link = sigil_bs4.Tag(name="link")
            link['href'] = "../Styles/footnote.css"
            link['rel'] = "stylesheet"
            link['type'] = "text/css"
            soup.html.head.append(link)
            soup.html.body.append(ol)
            # dunno why sigil cannot have valid close tag
            html = fixSelfCloseTags(str(soup))
            bk.writefile(id,html)
        modified = False
        lastid = id
#css
    if fnid > 0:
        cssdata = '''.sigil-footnote-item {
    margin: 0 0.6em;
    line-height: 130%;
    text-indent: 2em;
    font-weight: bold;
    font-size: 0.95em;
    text-align: justify;
}
.fn {
    text-indent: 0;
}
a.sigil-footnote {
    line-height: 1;
    vertical-align: super;
    text-decoration: none;
    height: auto;
    border: 0;
}
ol {
    list-style: none;
}
li {
    text-decoration: none;
}'''
        basename = "footnote.css"
        uid = "footnotecss"
        mime = "text/css"
        bk.addfile(uid, basename, cssdata, mime)
    return 0

def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
