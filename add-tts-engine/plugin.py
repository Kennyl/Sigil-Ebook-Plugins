#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
from lxml import etree, html

from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit,
                             QLabel, QApplication, QVBoxLayout)

from PyQt5.QtCore import Qt


lineEditPrompt1 = 'Language to be process. ie. "zh-HK" is Yue.'
defaultInput1 = "zh-HK"
lineEditPrompt2 = 'TTS innerText of Tag. ie. p for Paragraph Tag'
defaultInput2 = "p"
lineEditPrompt3 = 'TTS icon add to Tag Name. ie. h1 for Heading1'
defaultInput3 = "h1"
lineEditPrompt4 = 'Text Style when Tag is speaking. ie. style="text-decoration:underline"'
defaultInput4 = "text-decoration:underline"
lineEditPrompt5 = 'TTS Pitch. ie. 0.7"'
defaultInput5 = "0.7"
lineEditPrompt6 = 'TTS Speed Rate. ie. 1.1'
defaultInput6 = "1.1"

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
             lineEditPrompt3: defaultInput3,
             lineEditPrompt4: defaultInput4,
             lineEditPrompt5: defaultInput5,
             lineEditPrompt6: defaultInput6}

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
    tts_on_focus_style = items[lineEditPrompt4]
    tts_pitch = items[lineEditPrompt5]
    tts_rate = items[lineEditPrompt6]

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

    if bk.id_to_href("tts."+tts_lang) is not None:
        print("TTS javascript file is existed.")
        return 0
    else:
        print("TTS javascript file is added.")
# js
    if modified:
        jsdata = "\n"
        jsdata += "var tts_content_tag_name = '"+tts_content_tagname+"';\n"
        jsdata += "var tts_lang = '"+tts_lang+"';\n"
        jsdata += "var tts_icon_in_tagname = '"+tts_icon_in_tagname+"';\n"
        jsdata += "var tts_on_focus_style = '"+tts_on_focus_style+"';\n"
        jsdata += "var tts_pitch = '"+tts_pitch+"';\n"
        jsdata += "var tts_rate = '"+tts_rate+"';\n"
        jsdata += '''
  var tts_out_focus_style = "";
  var emojiPlayPaused = String.fromCharCode(9199);
  var emojiStop = String.fromCharCode(9209);
  var emojiSpeak = String.fromCharCode(55357, 56803);
  var tags;
  var i;
  var utterances=[];

  var tts = function() {
      a = document.createElement('a');
      a.id = 'tts';
      a.innerText = '  ' + emojiSpeak;
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

  fn_onstart = function (event) {
    tts_out_focus_style = tags[i].getAttribute('style');
    if (!tts_out_focus_style){
      tts_out_focus_style = "";
    }
    tags[i].setAttribute('style', tts_out_focus_style+";"+tts_on_focus_style);
    tags[i].scrollIntoView();
    console.log("started");
    document.getElementById('tts').innerHTML =  '  ' + emojiPlayPaused;
  };

  fn_onend = function(event) {
    if (!tts_out_focus_style){
      tags[i].removeAttribute('style');
    }else{
      tags[i].setAttribute('style',tts_out_focus_style);
    }
    i++;
    if(i < tags.length){
      console.log('Speak Next :' + i );
    }else{
      i = 0 ; //end of utterances
    }
    console.log('Finished in ' + event.elapsedTime + ' seconds.');
    document.getElementById('tts').innerHTML =  '  ' + emojiStop;
  };

  function speak(text, callback) {
    tags = document.getElementsByTagName(tts_content_tag_name)
    i = 0;
    for (var j = 0 ; j < tags.length ; j++){
      utterance = new SpeechSynthesisUtterance(tags[j].innerText);

      utterance.lang = tts_lang;
      utterance.pitch = tts_pitch;
      utterance.rate = tts_rate;

      utterance.onstart = fn_onstart;
      utterance.onend = fn_onend;

      utterances.push(utterance);

      speechSynthesis.speak(utterance);
    }
    document.getElementById('tts').innerHTML =  '  ' + emojiPlayPaused;
    document.getElementById('tts').removeEventListener('click', speak);
    document.getElementById('tts').addEventListener('click', p);
  }

document.addEventListener("DOMContentLoaded", tts);

'''
        baseFileName = "tts."+tts_lang+".js"
        uid = "tts."+tts_lang
        mime = "text/javascript"
        bk.addfile(uid, baseFileName, jsdata, mime)
    return 0


def run(bk):
    return runLXML(bk)


def main():
    print("I reached main when I should not have\n")
    return -1

if __name__ == "__main__":
    sys.exit(main())
