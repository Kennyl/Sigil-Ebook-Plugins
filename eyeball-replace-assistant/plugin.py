#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
outputAsFilePrompt = "Output As File"
outputAsFile = True


class askSetting(QWidget):


   def __init__(self,
                items,
                app = None,
                parent = None,
                ):

      super(askSetting, self).__init__(parent)

      self.app = app
      self.items = items

      layout = QVBoxLayout()

      self.buttons = {}
      self.lineedits = {}

      for key in items.keys():
        if type(items[key]) is bool:
            self.buttons[key] = QCheckBox(key)
            self.buttons[key].setChecked(items[key])
            self.buttons[key].setFocusPolicy(Qt.StrongFocus)
            layout.addWidget(self.buttons[key])
        else:
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
       for key in self.buttons.keys():
           self.items[key] = self.buttons[key].isChecked()
       self.close()
       self.app.exit(1)

   # def btnstate(self,key):
   #     self.items[key] = self.buttons[key].isChecked()

def run(bk):
    if sys.platform == "darwin":
        print("Plugin using PyQt5, bundled Python may not work")

    items = {lineEditPrompt: defaultInput,
             outputAsFilePrompt: outputAsFile}

    app = QApplication(sys.argv)
    ask = askSetting(items=items, app=app)
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
    word_dicts = {}
    for word in searching_words:
        result_dicts[word] = {}
    tsv = 'HRef\tWord\tRow\tColumn\tPattern\n'
    print('HRef\tWord\tRow\tColumn\tPattern')
    for (file_id, href) in bk.text_iter():
        if href.startswith("Text/_eyeball-replace-assistant"):
            continue
        html_original = bk.readfile(file_id)
        for word in searching_words:
            for match in re.finditer(regexpCondition + word + regexpCondition,
                                     html_original,
                                     re.DOTALL):
                # print(match.group(1))
                occurrence = word_dicts.setdefault(word, 0) + 1
                word_dicts[word] = occurrence
                if match.group(0) in result_dicts[word]:
                    result_dicts[word][match.group(0)].append(href)
                else:
                    result_dicts[word][match.group(0)] = [href]
                row = html_original[:match.start()].count('\n')+1
                column = match.start() - html_original[:match.start()].rfind('\n')
                pattern = match.group(0)
                print('%s\t%s\t%s\t%s\t%s'
                      % (href, word, row, column, pattern))
                tsv += ('%s\t%s\t%s\t%s\t%s\n'
                        % (href, word, row, column, pattern))

    print('\n\n===================================================\n')
    print("File saved as Text/_eyeball-replace-assistant*.html")
    print('===================================================\n\n')
    breakdown_text = ""
    for word in sorted(result_dicts):
        if (len(result_dicts[word]) > 0) :
            print("%s Distinct (%s) Total (%s) " % (word, len(result_dicts[word]), word_dicts[word]))
            print('===================================================')
            breakdown_text += '\n===================================================\n'
            breakdown_text += "%s Distinct (%s) Total (%s) " % (word, len(result_dicts[word]), word_dicts[word])
            breakdown_text += '\n===================================================\n'
            for pattern in sorted(result_dicts[word]):
                # line = "Found %s as pattern %s in %s ." % (pattern, word, result_dicts[word][pattern])
                line = pattern
                breakdown_text += pattern + '\n'
                print(line)
                # breakdown_text += line + "\n"
            print('===================================================')
        else:
            breakdown_text += '\n===================================================\n'
            breakdown_text += "%s Not Found " % word
            breakdown_text += '\n===================================================\n'
            print("%s Not Found " % word)
            print('===================================================')


    print('\n            Done. Copy as you need\n')
    print('===================================================\n\n')
    breakdown_text += '\n===================================================\n'
    text = ""
    if breakdown_text != "":
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

        text += '\n\n===================================================\n\n'
        body = ('<abbr title="Tab Seperated Version">TSV</abbr>'
        '(Tab Seperated Version) as text file '
        '<a href="Misc/_eyeball-replace-assistant.tsv.txt"> '
        'Misc/_eyeball-replace-assistant.tsv.txt</a> <br/><hr/>')
        body += ('Breakdown'
        '<a href="Misc/_eyeball-replace-assistant.txt">'
        'Misc/_eyeball-replace-assistant.txt</a> <br/><hr/>')
        for href in sorted(reversed_dicts):
            body += '<br/><hr/><a href="%s">%s</a><br/><hr/>\n' % (href, href)
            for word in sorted(reversed_dicts[href]):
                pattern = reversed_dicts[href][word]
                text += ('In %s has word %s in following pattern(s):  %s .'
                         % (href, word, pattern))
                body += (r'<br/>Word %s in following pattern(s):  %s .\n'
                        % (word, html.escape(r''.join(pattern))))
            body += "<br/><hr/>\n"

        if outputAsFile:
            print('File Output\n===================================')
            print('Text/_eyeball-replace-assistant*.html')
            print('Misc/_eyeball-replace-assistant*.tsv.txt')
            print('Misc/_eyeball-replace-assistant*.txt')
            print('===================================')
            # bk.addotherfile('eyeball-replace-assistant.txt',text)
            bk.addotherfile('_eyeball-replace-assistant.html',
                            '<html><body>'+body+'</body></html>')
            bk.addotherfile('_eyeball-replace-assistant.tsv.txt',
                            tsv)
            bk.addotherfile('_eyeball-replace-assistant.txt',
                            breakdown_text)
#varible (text) hasn't used
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
