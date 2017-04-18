#!/usr/bin/env python
#-*- coding: utf-8 -*-
# from __future__ import unicode_literals, division, absolute_import, print_function
import sys

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel,
                             QApplication, QHBoxLayout, QVBoxLayout,
                             QCheckBox)
from PyQt5.QtCore import Qt


class askSetting(QWidget):


   def __init__(self,
                items,
                app = None,
                parent = None
                ):

      super(askSetting, self).__init__(parent)

      self.app = app
      self.items = items

      layout = QVBoxLayout()

      self.buttons = {}
      self.lineedits = {}

      for key in items.keys():
        if type(items[key]) == bool :
            self.buttons[key] = QCheckBox(key)
            self.buttons[key].setChecked(items[key])
            self.buttons[key].setFocusPolicy(Qt.StrongFocus)
            layout.addWidget(self.buttons[key])
        else:
         # I Default it is string
            layoutX = QHBoxLayout()
            layoutX.addWidget(QLabel(key))
            self.lineedits[key] = QLineEdit()
            self.lineedits[key].setText(items[key])
            #enable ime input
            self.lineedits[key].inputMethodQuery(Qt.ImEnabled)
            layoutX.addWidget(self.lineedits[key])
            layout.addLayout(layoutX)

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
        print("Don't use bundle python or it may not work")

    items = {"TextBox1": "",
             "CheckBox1": True,
             "CheckBox2": False,
             "TextBox2": "2"}
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
