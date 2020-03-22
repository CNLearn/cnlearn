# The Plan
This should (probably is not) a reflection of the features that are/will be implemented:

## 1. Find open source dictionary
[CC-CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict) is an [CC licensed](https://creativecommons.org/licenses/by-sa/3.0/) dictionary.   
Right now the format of each word is as like the following:  
**交戰 交战 [jiao1 zhan4] /to fight/to wage war/**
So it has the traditional character, simplified character, pinyin with tone numbers, followed by the definitions.  
I also wanted to have the tone accents and not just the numbers, so inspired by [this link here](https://github.com/mdsills/cccedict/blob/master/src/Entry.php) I wrote a Python (i.e. definitely not PHP version of the script).

Before doing that, I played around with it and extracted to different files. Bash commands and unix programs are simpler to use. To extract the various parts:
```bash
awk '{print $1}' >traditional
awk '{print $2}' >simplified
awk '{for(i=3; i<=NF; i++) printf FS$i; print NL }' cedict_1_0_ts_utf-8_mdbg.txt >pinyin_definition
cat pinyin_definition | cut -d "[" -f2 | cut -d "]" -f1 >numeric_pinyin
awk -F " /" '{print $2}' pinyin_definition >definition
```
The following description related to the **dict** folder in the main directory. The script is available there (extract.py). The dictionary used (and its associated license) is in the **cedict** folder. In the **parts** folder one can find the dictionary split into pinyin, definition, simplified and traditional parts.
