#!/usr/bin/env python
#-*- coding: utf-8 -*-
# from __future__ import unicode_literals, division, absolute_import, print_function
import sys
import re
import html

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel,
                             QApplication, QHBoxLayout, QVBoxLayout,
                             QCheckBox)

from PyQt5.QtCore import Qt

lineEditPrompt = "String to Find (seperated in Spacebar)"
defaultInput =  "幹 乾 干 髮 里 裡 衝 沖 制 製 準"
regexpCondition = r'.{0,3}'

class askSetting(QWidget):


   def __init__(self,
                app = None,
                parent = None,
                items = None):

      super(askSetting, self).__init__(parent)

      self.app = app
      self.items = items

      layout = QVBoxLayout()

    #   self.buttons = {}
      self.lineedits = {}

      for key in items.keys():
        layout.addWidget(QLabel(key))
        self.lineedits[key] = QLineEdit()
        self.lineedits[key].setText(items[key])
        # enable ime input
        self.lineedits[key].inputMethodQuery(Qt.ImEnabled)
        layout.addWidget(self.lineedits[key])

      self.btn = QPushButton('OK', self)
      self.btn.clicked.connect(lambda:(self.bye(items)))
      self.btn.setFocusPolicy(Qt.StrongFocus)

      layout.addWidget(self.btn)

      self.setLayout(layout)
      self.setWindowTitle(' Setting ')


   def bye(self, items):
       for key in self.lineedits.keys():
           self.items[key] = self.lineedits[key].text()
    #    for key in self.buttons.keys():
    #        self.items[key] = self.buttons[key].isChecked()
       self.close()
       self.app.exit(1)

   # def btnstate(self,key):
   #     self.items[key] = self.buttons[key].isChecked()

def run(bk):
    if sys.platform == "darwin":
        print("Plugin using PyQt5, bundled Python may not work")

    items = {lineEditPrompt: defaultInput}

    app = QApplication(sys.argv)
    ask = askSetting(app=app, items=items)
    ask.show()
    rtnCode = app.exec_()
    #If press OK button  rtnCode should be 1
    if rtnCode != 1 :
        print('User abort by closing Setting dialog')
        return -1

    print(items)
    #selected file in file list
    searching_words = items[lineEditPrompt].split(' ')
    result_dicts = {}
    for word in searching_words:
        result_dicts[word] = {}
    # debug print
    # print('href\tword\trow\tcolumn\tpattern')
    for (file_id, href) in bk.text_iter():
        if href.startswith("Text/_eyeball-replace-assistant"):
            continue
        html_original = bk.readfile(file_id)
        for word in searching_words:
            for match in re.finditer(regexpCondition + word + regexpCondition,
                                     html_original,
                                     re.DOTALL):
                if match.group(0) in result_dicts[word]:
                    result_dicts[word][match.group(0)].append(href)
                else:
                    result_dicts[word][match.group(0)] = [href]
                row = html_original[:match.start()].count('\n') + 1
                column = (match.start()
                          - html_original[:match.start()].rfind('\n'))
                pattern = html.escape(match.group(0))
                # debug print
                # print('%s\t%s\t%s\t%s\t%s' % (href, word, row, column, match.group(0)))
                message = ('Col:%04s , %s -> %s'
                           % (column, word, pattern))
                bk.add_result(bk.TYPE_INFO,
                              bk.href_to_basename(href),
                              row,
                              message)
                # bk.add_extended_result(bk.TYPE_INFO, bk.href_to_basename(href), row, column, message)
                # extended result will not scroll to row use add_result instead.
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
