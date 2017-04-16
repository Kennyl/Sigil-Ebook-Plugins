#!/usr/bin/env python
#-*- coding: utf-8 -*-
# from __future__ import unicode_literals, division, absolute_import, print_function
import sys
import re
import html

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel,
    QInputDialog, QApplication, QHBoxLayout, QVBoxLayout, QCheckBox)

import PyQt5.QtCore

lineEditPrompt = "String to Find (seperated in Spacebar)"
defaultInput =  "幹 乾 干 髮 里 裡 衝 沖 制 製 準"

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
        layout.addWidget(self.lineedits[key])

      self.btn = QPushButton('OK', self)
      self.btn.clicked.connect(lambda:(self.bye(items)))

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
        print("Don't use bundle python or it may not work")

    items = {lineEditPrompt:defaultInput}

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

    for (file_id, href) in bk.text_iter():
        if href.startswith("Text/_eyeball-replace-assistant"):
            continue
        html_original = bk.readfile(file_id)
        for word in searching_words:
            match = re.search('(.?.?.?'+word+'.?.?.?)', html_original)
            if match is not None:
                # print(match.group(1))
                if match.group(1) in result_dicts[word]:
                    result_dicts[word][match.group(1)].append(href)
                else:
                    result_dicts[word][match.group(1)] = [href]

    print('\n\n===================================================\n')
    print("File saved as Text/_eyeball-replace-assistant*.htm")
    print('===================================================\n\n')
    text = ""
    for word in sorted(result_dicts):
        for pattern in sorted(result_dicts[word]):
            line = "Found %s as pattern %s in %s ." % (pattern, word, result_dicts[word][pattern])
            print(line)
            text += line + "\n"
    print('\n\n===================================================\n\n')

    if text != "":
        #revesed list
        reversed_dicts = {}
        for word in result_dicts:
            for pattern in result_dicts[word]:
                for href in result_dicts[word][pattern]:
                    if href not in reversed_dicts:
                        reversed_dicts[href]={word:[pattern]}
                    else:
                        if word not in reversed_dicts:
                            reversed_dicts[href][word]=[pattern]
                        else:
                            reversed_dicts[href][word].append(pattern)
                # if word not in reversed_dicts
                #     reversed_dicts[word] =
                # href = result_dicts[word][pattern]
                # dict1 = reversed_dicts.setdefault(href, {word:[pattern]})
                # dict2 = dict1.setdefault(word,[])
                # dict2.append(pattern)

        text += '\n\n===================================================\n\n'
        body = ""

        for href in sorted(reversed_dicts):
            for word in sorted(reversed_dicts[href]):
                pattern = reversed_dicts[href][word]
                text += 'In %s has word %s in pattern %s .' % (href, word, pattern)
                line = r'<br/> In <a href="%s">%s</a> has word %s in pattern %s .' % (href, href, word, html.escape(r''.join(pattern)))
                body += line + "\n"
            body += "<hr/>\n"

        # bk.addotherfile('eyeball-replace-assistant.txt',text)
        bk.addotherfile('_eyeball-replace-assistant.html', '<html><body>'+body+'</body></html>')

    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
