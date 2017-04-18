#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
from lxml import etree, html


def run(bk):
    count = 0
    print('start')
    for (file_id, _) in bk.text_iter():
        modified = True
        html_original = bk.readfile(file_id)
        doc = html.fromstring(html_original.encode("utf-8"))
        for link in doc.xpath("//*[local-name() = 'link']"):
            if link.attrib['href'] == "../Styles/t2bv2l.css":
                modified = False
                break

        if modified:
            count += 1
            head = doc.xpath("//*[local-name() = 'head']")[0]
            link = etree.SubElement(head,
                                    "link",
                                    attrib={'href': "../Styles/t2bv2l.css",
                                            'rel': "stylesheet",
                                            'type': "text/css"
                                           })
            print("Modified File : ", file_id)
            bk.writefile(file_id,
                         etree.tostring(
                             doc,
                             encoding="utf-8",
                             xml_declaration=True).decode('utf8'))

# css
    if count > 0:
        cssdata = '''
html{
    direction:rtl;
    -ms-writing-mode: tb-rl;
    -epub-writing-mode: vertical-rl;
    -webkit-writing-mode: vertical-rl;
    writing-mode: vertical-rl;
}
body {
    direction:ltr;
    word-break: normal;
    text-align: justify;
    text-justify: inter-ideograph;
    vertical-align: baseline;
    word-wrap: break-word;
    line-break: normal;
    -epub-line-break: normal;
    -webkit-line-break: normal;
    text-orientation: upright;
    -webkit-text-orientation: upright;
    -epub-text-orientation: upright;
}
.tcy {
  -epub-text-combine: horizontal;
  -webkit-text-combine: horizontal;
  -ms-text-combine-horizontal: all;
  text-combine-horizontal: all;
  text-combine-upright: all;
}
.upright {
  -epub-text-orientation: rotate-right;
  -epub-text-orientation: upright;
  -webkit-text-orientation: upright;
  -epub-text-combine: horizontal;
  -webkit-text-combine: horizontal;
  -ms-text-combine-horizontal: all;
  text-combine-horizontal: all;
  text-combine-upright: all;
}'''
        basename = "t2bv2l.css"
        uid = "t2bv2lcss"
        mime = "text/css"
        bk.addfile(uid, basename, cssdata, mime)


    bk.setspine_ppd('rtl')
    xml = bk.getmetadataxml()

    if '<meta name="primary-writing-mode" content="vertical-rl"/>' not in xml:
        xml = xml.replace('</metadata>',
                '<meta name="primary-writing-mode" content="vertical-rl"/>\n</metadata>')
        bk.setmetadataxml(xml)

    print('end')
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
