# Sigil-Ebook-Plugins

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1f6ee51671344df8b0f1a613243354c1)](https://www.codacy.com/app/Kennyl/Sigil-Ebook-Plugins?utm_source=github.com&utm_medium=referral&utm_content=Kennyl/Sigil-Ebook-Plugins&utm_campaign=badger) [![Build Status](https://travis-ci.org/Kennyl/Sigil-Ebook-Plugins.svg?branch=master)](https://travis-ci.org/Kennyl/Sigil-Ebook-Plugins)

Various Plugins for [Sigil-Ebook](https://github.com/Sigil-Ebook/Sigil)

- [add-tts-engine](#add-tts-engine)
- [cross-reference-lang](#cross-reference-lang)
- [eyeball-replace-assistant](#eyeball-replace-assistant)
- [eyeball-replace-validator](#eyeball-replace-validator)
- [footnotes-regenerator](#footnotes-regenerator)
- [full-width-digit](#full-width-digit)
- [full-width-punctuation](#full-width-punctuation)
- [kobo-footnotes-enhance](#kobo-footnotes-enhance)
- [prompt-user-example](#prompt-user-example)
- [vertical-cjk-punctuation](#vertical-cjk-punctuation)
- [vertical-rtl](#vertical-rtl)

zip folder for each plugins

For example making footnotes-regenerator plugin

```
zip footnotes-regenerator.zip footnotes-regenerator/p*
```

## add-tts-engine

Add tts engine to selected files in Book Browser

Default settings:

1. Language to be process default Yue ie. zh-HK

2. TTS innerText of Element ID   ie. <? id=content></content> 
```getElementByID("content").innerText```
3. TTS icon "🗣 " add to Tag Name ie. <h1>
```<h1>Heading 1 🗣 </h1>```

## cross-reference-lang

Cross Reference for selected files in Book Browser

Default settings:

File to change: zh ie. \*.zh.{any_extension} 
File to be referenced: en ie. \*.en.{any_extension}
 
Changing file
From selected files
  \*.zh.html or \*.zh.{any_extension} 
to 
  \*.en.html or \*.en.{any_extension}


## eyeball-replace-assistant

Search input terms seperated by Spacebar (```term1  term2 term3```) using following regexp

.?.?.?term1.?.?.?

and place result in  Text/\_eyeball-replace-assistant\*.html

```
zip eyeball-replace-assistant.zip eyeball-replace-assistant/p*
```

## eyeball-replace-validator

Search input terms seperated by Spacebar (```term1  term2 term3```) using following regexp

.?.?.?term1.?.?.?

Result will show on validation window

```
zip eyeball-replace-validator.zip eyeball-replace-validator/p*
```

## footnotes-regenerator

This a plugin for Sigil

Inspire from epub forum user

Reorder footnote number push footnote to end of chapter file.

Using ```[^number]``` , ```[^number]:``` pairs as magic tag (Markdown Extra style)

```
<p>HTML[^1]</p>
<div>PY[^1]<div>

<div>[^1]: HyperTextMarkupLanuage</div>
<p>[^1]: Python</p>
```
will be regenerated within chapter.
```
<p>HTML<a class="duokan-footnote" href="#fn1" id="fnref1'></a></p>
<div>PY<a class="duokan-footnote" href="#fn2" id="fnref2'></a><div>

<aside epub:type="footnote"><div><a  href="#fnref1"></a>HyperTextMarkupLanuage<a href="#fnref1">\N{LEFTWARDS ARROW WITH HOOK}</a></div></aside>
<aside epub:type="footnote"><p><a  href="#fnref2"></a>Python<a href="#fnref2">\N{LEFTWARDS ARROW WITH HOOK}</a></p></aside>
```

if set in plugins ```useNumberOrderingInsteadOfIdeograph = False```

```
<p>HTML[1]</p>
<div>PY[1]<div>

<div>[1] HyperTextMarkupLanuage</div>
<p>[1] Python</p>
```
will be regenerated within chapter.
```
<p>HTML<a epub:type="noteref">注</a></p>
<div>PY<a epub:type="noteref">注</a><div>

<aside epub:type="footnote"><div>釋： HyperTextMarkupLanuage</div></aside>
<aside epub:type="footnote"><p>釋： Python</p></aside>
```

However for more complex style, you can edit ```footnote.css```

For footnote reference's style

```
body{
    counter-reset:footref-index;
}
a.duokan-footnote::before{
}
a.duokan-footnote{
}
a.duokan-footnote::after{
}
```

For footnote's style

```
.duokan-footnote-content{
    counter-reset:footnote-index;
}
.duokan-footnote-item a:first-of-type::before{
  ...
}
.duokan-footnote-item a:first-of-type{
  ...
}
.duokan-footnote-item a:first-of-type::after{}
  ...
}
.duokan-footnote-item a:last-of-type::before{
  ...
}
.duokan-footnote-item a:last-of-type::after{}
  ...
}
```

No License since the origin's source and idea are unknown.

Plugins binary for Sigil
```
zip footnotes-regenerator.zip footnotes-regenerator/plugin.py footnotes-regenerator/plugin.xml
```
<hr/>

## full-width-digit

Change [0-9] to \N{FULLWIDTH DIGIT [ZERO-NINE]}

Make Plugin for Sigil
```
zip full-width-digit.zip full-width-digit/plugin.py full-width-digit/plugin.xml
```
<hr/>

## full-width-punctuation

Change ";" ":" "," "?" "!" "." to \N{FULLWIDTH PUNCTUATION}

Make Plugin for Sigil
```
zip full-width-punctuation.zip full-width-punctuation/plugin.py full-width-punctuation/plugin.xml
```
<hr/>

## kobo-footnotes-enhance

This plugin will link (校記1）<-> section ■校記 of 1
and （注釋2）<-> section ■注釋 of 2

Adaptive for modification in source code.

Make Plugin for Sigil
```
zip kobo-footnotes-enhance.zip kobo-footnotes-enhance/plugin.py kobo-footnotes-enhance/plugin.xml
```
<hr/>

## prompt-user-example

Example used for prompt user input before plugin start

Support OneLineText and CheckBox

Set dict as following {"key":value}

```items = {"TextBox1": "",
         "CheckBox1": True,
         "CheckBox2": False,
         "TextBox2": "2"}
```

Make Plugin for Sigil

```
zip prompt-user-example.zip prompt-user-example/plugin.py prompt-user-example/plugin.xml
```

<hr />

## vertical-cjk-punctuation

Change － … to ｜ ⋮

Make Plugin for Sigil
```
zip vertical-cjk-punctuation.zip vertical-cjk-punctuation/plugin.py vertical-cjk-punctuation/plugin.xml
```
<hr/>

## vertical-rtl

Change horizontal to vertical passage ( top to bottom and right to left)

Make Plugin for Sigil
```
zip vertical-rtl.zip vertical-rtl/plugin.py vertical-rtl/plugin.xml
```
<hr/>

No License, No Warranty, No Bullshit
