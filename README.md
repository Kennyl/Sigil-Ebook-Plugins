# Sigil-Ebook-Plugins

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1f6ee51671344df8b0f1a613243354c1)](https://www.codacy.com/app/Kennyl/Sigil-Ebook-Plugins?utm_source=github.com&utm_medium=referral&utm_content=Kennyl/Sigil-Ebook-Plugins&utm_campaign=badger)

Various Plugins for [Sigil-Ebook](https://github.com/Sigil-Ebook/Sigil)

- [footnotes-regenerator](#footnotes-regenerator)
- [vertical-rtl](#vertical-rtl)
- [full-width-digit](#full-width-digit)
- [full-width-punctuation](#full-width-punctuation)

zip folder for each plugins

For example making footnotes-regenerator plugin

```
zip footnotes-regenerator.zip footnotes-regenerator/p*
```

## footnotes-regenerator

This a plugin for Sigil

Inspire from epub forum user

Reorder footnote number
push footnote to end of chapter file.
Using [number] as magic tag.
```
<p>HTML[1]</p>
<div>PY[1]<div>

<div>[1] HyperTextMarkupLanuage</div>
<p>[1] Python</p>
```
will be regenerated within chapter.
```
<p>HTML<a epub:type="noteref">[1]</a></p>
<div>PY<a epub:type="noteref">[2]</a><div>

<aside epub:type="footnote"><div>[1] HyperTextMarkupLanuage</div></aside>
<aside epub:type="footnote"><p>[2] Python</p></aside>
```
No License since the origin's source and idea are unknown.

Plugins binary for Sigil
```
zip footnotes-regenerator.zip footnotes-regenerator/plugin.py footnotes-regenerator/plugin.xml
```
<hr/>

## vertical-rtl

Change horizontal to vertical passage ( top to bottom and right to left)

Make Plugin for Sigil
```
zip vertical-rtl.zip vertical-rtl/plugin.py vertical-rtl/plugin.xml
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

No License, No Warranty, No Bullshit
