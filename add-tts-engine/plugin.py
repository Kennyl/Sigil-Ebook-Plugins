#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
from lxml import etree, html

from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit,
                             QLabel, QApplication, QVBoxLayout)

from PyQt5.QtCore import Qt


lineEditPrompt1 = 'Language to be process. ie. "zh-HK" is Yue.'
defaultInput1 = "zh-HK"
lineEditPrompt2 = 'TTS innerText of Tag. ie. body for Body Tag'
defaultInput2 = "body"
lineEditPrompt3 = 'TTS icon add to Tag Name. ie. h1 for Heading1'
defaultInput3 = "h1"

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


def runLXML(bk):
    if sys.platform == "darwin":
        print("Plugin using PyQt5, bundled Python may not work")

    items = {lineEditPrompt1: defaultInput1,
             lineEditPrompt2: defaultInput2,
             lineEditPrompt3: defaultInput3}

    count = 0
    for (_, file_id) in bk.selected_iter():
        global filelist
        count += 1
        filelist += "\n" + file_id
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

    tts_lang = items[lineEditPrompt1]
    tts_content_tagname = items[lineEditPrompt2]
    tts_icon_in_tagname = items[lineEditPrompt3]

    modified = False

    for (_, file_id) in bk.selected_iter():
        html_original = bk.readfile(file_id)
        doc = html.fromstring(html_original.encode("utf-8"))
        head = doc.xpath("//*[local-name() = 'head']")[0]
        etree.SubElement(head,
                         "script",
                         attrib={'src': "../Misc/tts."+tts_lang+".js",
                                 'type': "text/javascript"
                                 })
        bk.writefile(file_id,
                     etree.tostring(
                         doc,
                         encoding="utf-8",
                         xml_declaration=True).decode('utf8'))
        modified = True
# js
    if modified:
        jsdata = "\n"
        jsdata += "var tts_content_tag_name = '"+tts_content_tagname+"';\n"
        jsdata += "var tts_lang = '"+tts_lang+"';\n"
        jsdata += "var tts_icon_in_tagname = '"+tts_icon_in_tagname+"';\n"
        jsdata += '''
var tts_pitch = 0.7;
var tts_rate = 1.1;

var tts = function() {
    a = document.createElement('a');
    a.id = 'tts';
    a.innerText = '  ' + String.fromCharCode(55357, 56803);
    document.getElementsByTagName(tts_icon_in_tagname)[0].appendChild(a);
    document.getElementById('tts').addEventListener('click', speak);
}
function p(){
    speechSynthesis.pause();
    document.getElementById('tts').removeEventListener('click', p);
    document.getElementById('tts').addEventListener('click', r);
}
function r(){
    speechSynthesis.resume();
    document.getElementById('tts').removeEventListener('click', r);
    document.getElementById('tts').addEventListener('click', p);
}
function speak(text, callback) {
    tags = document.getElementsByTagName(tts_content_tag_name)
    var i = 0;
    text = tags[i].innerText;
    for(i=1; i<tags.length; i++){
      text += tags[i].innerText;
    };
    matches = text.match(/.{1,30000}/mg);
    matches.forEach(function(e){
      var t = new SpeechSynthesisUtterance(e);
      t.lang = tts_lang;
      t.pitch = tts_pitch;
      t.rate = tts_rate;
      msg = t;
      msg.onstart = function (event) {
        //console.log("started");
        emoji = String.fromCharCode(9199);
        document.getElementById('tts').innerHTML = '  ' + emoji;

      };
      msg.onend = function(event) {
        //console.log('Finished in ' + event.elapsedTime + ' seconds.');
        emoji = String.fromCharCode(9209)'
        document.getElementById('tts').innerHTML = '  ' + emoji;
      };
      speechSynthesis.speak(t);
    });
  emoji = String.fromCharCode(9199);
  document.getElementById('tts').innerHTML = '  ' + emoji;
  document.getElementById('tts').removeEventListener('click', speak);
  document.getElementById('tts').addEventListener('click', p);
}

document.addEventListener("DOMContentLoaded", tts);
'''
        basename = "tts."+tts_lang+".js"
        uid = "tts."+tts_lang
        mime = "text/javascript"
        bk.addfile(uid, basename, jsdata, mime)
    return 0


def run(bk):
    return runLXML(bk)


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
