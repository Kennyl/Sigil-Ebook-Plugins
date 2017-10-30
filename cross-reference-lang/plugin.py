#!/usr/bin/env python
#-*- coding: utf-8 -*-
import copy
from functools import reduce
from lxml import etree, html
import sys

from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit,
                             QLabel, QApplication, QVBoxLayout)

from PyQt5.QtCore import Qt

lineEditPrompt1 = 'Language to be process i.e. "zh" in (chapter1.zh.html)'
defaultInput1 = "zh"
lineEditPrompt2 = 'Language to be reference i.e. "en" to (chapter1.en.html)'
defaultInput2 = "en"

# 🇬🇧
# flag of United Kingdom
# Unicode: U+1F1EC U+1F1E7, UTF-8: F0 9F 87 AC F0 9F 87 A7
# String.fromCharCode(55356,56812,55356,56807);

# 🇭🇰
# flag of Hong Kong SAR China
# Unicode: U+1F1ED U+1F1F0, UTF-8: F0 9F 87 AD F0 9F 87 B0
# String.fromCharCode(55356,56813,55356,56816);

# 🔖
# bookmark
# Unicode: U+1F516, UTF-8: F0 9F 94 96
# String.fromCharCode(55357, 565980);

filelist = "Selected file in Book Browser:\n"


class askSetting(QDialog):

    def __init__(self,
                 app=None,
                 parent=None,
                 items=None):

        super(askSetting, self).__init__(parent)

        self.app = app
        self.items = items

        layout = QVBoxLayout()

        self.lineedits = {}
        global filelist
        layout.addWidget(QLabel(filelist))

        for key in items.keys():
            layout.addWidget(QLabel(key))
            self.lineedits[key] = QLineEdit()
            self.lineedits[key].setText(items[key])
            # enable ime input
            self.lineedits[key].inputMethodQuery(Qt.ImEnabled)
            layout.addWidget(self.lineedits[key])

        self.btn = QPushButton(
            'OK to Change Selected File in Book Browser', self)
        self.btn.clicked.connect(lambda: (self.bye(items)))
        self.btn.setFocusPolicy(Qt.StrongFocus)

        layout.addWidget(self.btn)

        self.setLayout(layout)
        self.setWindowTitle(' Setting ')

    def bye(self, items):
        for key in self.lineedits.keys():
            self.items[key] = self.lineedits[key].text()
        self.close()
        self.app.exit(1)


def run(bk):
    if sys.platform == "darwin":
        print("Plugin using PyQt5, bundled Python may not work")

    items = {lineEditPrompt1: defaultInput1,
             lineEditPrompt2: defaultInput2}
    count = 0
    for (_, b) in bk.selected_iter():
        global filelist
        count += 1
        filelist += "\n" + b
    if count == 0:
        filelist += "Please select file(s) first!!"
        print("Please select file(s) first!!")
        return -1
    filelist += "\n"

    app = QApplication(sys.argv)
    ask = askSetting(app=app, items=items)
    ask.show()
    rtnCode = app.exec_()
    # If press OK button  rtnCode should be 1
    if rtnCode != 1:
        print('User abort by closing Setting dialog')
        return -1

    print(items)
    # selected file in file list
    replace_lang = items[lineEditPrompt1]
    refer_lang = items[lineEditPrompt2]

    # for (file_id, href) in bk.text_iter():
    for (id_type, file_id) in bk.selected_iter():
        href = bk.id_to_href(file_id)
        hrefsplit = href.split(".")
        if hrefsplit[-2] == replace_lang:
            html_original = bk.readfile(file_id)
            doc = html.fromstring(html_original.encode("utf-8"))
            pathsearch = "//*[local-name()='p']"
            elements = doc.xpath(pathsearch)
            pid = 0
            target = (reduce(lambda x, y: x+"."+y, hrefsplit[0:-2]) +
                      "." + refer_lang + "."+hrefsplit[-1])

            for elem in elements:
                # hard code, bad, not consistent syntax in html
                if elem.find('span') is None:
                    if elem.text is None or len(elem.text) == 0:
                        continue

                # pid += 1
                # atag = etree.SubElement(
                #     elem,
                #     "a",
                #     attrib={"id": replace_lang+str(pid),
                #             "style": "float:right;text-decoration:none",
                #             "href": target+"#"+refer_lang+str(pid)})
                # atag.text = '🔖'
                # elem.insert(0, atag)

                pid += 1
                temp = copy.deepcopy(elem)
                temp.tag = "span"
                elem.tag = "p"
                elem.clear()
                atag = etree.SubElement(
                    elem,
                    "a",
                    attrib={"id": replace_lang+str(pid),
                            "style": "float:right;text-decoration:none",
                            "href": target+"#"+refer_lang+str(pid)})
                atag.text = '🔖'
                elem.append(atag)
                elem.append(temp)

            # for elem in elements:
            #     pid += 1
            #     temp = copy.deepcopy(elem)
            #     temp.tag = "a"
            #     temp.set("style", "text-decoration:none")
            #     temp.set("id", replace_lang+str(pid))
            #     temp.set("href", target+"#"+refer_lang+str(pid))
            #     elem.tag = "p"
            #     elem.clear()
            #     elem.append(temp)
            bk.writefile(file_id,
                         etree.tostring(
                             doc,
                             encoding="utf-8",
                             xml_declaration=True).decode('utf8'))
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
