#!/usr/bin/env python
#-*- coding: utf-8 -*-
# from __future__ import unicode_literals, division, absolute_import, print_function
import sys

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel,
    QInputDialog, QApplication, QHBoxLayout, QVBoxLayout, QCheckBox)


class askSetting(QWidget):

   def makeFunc1(self, x):
     return lambda:self.btnstate(x)


   def __init__(self, parent = None, items = {"Default": True, "Text": ""}):
      super(askSetting, self).__init__(parent)

      layout = QVBoxLayout()
      self.buttons = {}
      self.lineedits = {}
      self.items = items

      for key in items.keys():
        if type(items[key])==bool :
            self.buttons[key] = QCheckBox(key)
            self.buttons[key].setChecked(items[key])
            self.buttons[key].stateChanged.connect(self.makeFunc1(key))
            layout.addWidget(self.buttons[key])
        else:
         # I Default it is string
            layoutX = QHBoxLayout()
            layoutX.addWidget(QLabel(key))
            self.lineedits[key] = QLineEdit()
            self.lineedits[key].setText(items[key])
            layoutX.addWidget(self.lineedits[key])
            layout.addLayout(layoutX)


      self.btn = QPushButton('OK', self)
      self.btn.clicked.connect(lambda:(self.bye(items)))

      layout.addWidget(self.btn)

      self.setLayout(layout)
      self.setWindowTitle("Setting")


   def bye(self, items):
       for key in self.lineedits.keys():
           self.items[key] = self.lineedits[key].text()
       self.close()

   def edited(self, key):
       self.items[key] = self.lineedits[key].getText()

   def btnstate(self,key):
       self.items[key] = self.buttons[key].isChecked()

def run(bk):
    if sys.platform == "darwin":
        print("Don't use bundle python or it may not work")

    items = {"TextBox1": "",
             "CheckBox1": True,
             "CheckBox2": False,
             "TextBox2": "2"}
    app = QApplication(sys.argv)
    ask = askSetting(None,items=items)
    ask.show()
    app.exec_()

    print(items)
    abc = bk.selected_iter()
    if abc is None:
        print("None")
    else:
        print("Found Selected %s" % (abc) )

    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
