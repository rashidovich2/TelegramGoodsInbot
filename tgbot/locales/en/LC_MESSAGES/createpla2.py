#!/usr/bin/env python3
import os, sys
'''from deep_translator import (GoogleTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)'''
from googletrans import Translator
#from translatepy import Translator
translator = Translator()

x = open("mybotr.po", "a")
with open('mybot.po', encoding='UTF-8') as f:
    idblock=""
    idblock2=""
    lines = f.readlines()
    for row in lines:
        if row[0] == '"':
            idblock = idblock + row
            #erow = translator.translate(row)
            #erow = translator.translate(row, src='ru', dest='en')
            #print(erow)
            #xr2 = translator.translate_text(row, target_lang="RU-RU")
            #xr2 = GoogleTranslator(source='ru', target='en').translate(text=row)
            #xr2 = deepl.translate(source_language="RU", target_language="EN", text=row)

            idblock2 = idblock2 + row
            print(idblock)
            print(idblock2)
            print("1")
        if 'msgid ' in row:
            print("2")
            print("2-1")
            if 'msgid ""' in row:
                idblock= idblock + 'msgid ""' + "\n"
                idblock2= idblock2 + 'msgstr ""' + "\n"
            #x.write('msgid ""\n')
            else:
                idblock= idblock + row + "\n"
                ##erow = translator.translate(row)
                #print(row['text'])
                #xb2 = translator.translate_text(row[7:], target_lang="RU-RU")
                #xb2 = GoogleTranslator(source='ru', target='en').translate(text=row)
                #xb2 = deepl.translate(source_language="RU", target_language="EN", text=row[7:])
                #erow = translator.translate(row, src='ru', dest='en')
                #print(erow)
                #idblock2= idblock2 + 'msgstr ' + erow[7:]
                continue
            print(row[7:])
            #x.write('msgstr ' + row[6:])
        elif 'msgstr' in row:
            print("3")
            #x.write(idblock)
            #x.write(idblock2)
            idblock = ""
            idblock2 = ""
            continue
        elif row[0] == "\n":
            print("4")
            x.write('\n')
            #idblock= idblock + row
            #idblock2= idblock2 + row
        else:
            #xrow = translator.translate(row)
            #trow = translator.translate(row, src='ru', dest='en')
            print(row)
            #print(row)
            #xrow = translator.translate_text(row, target_lang="RU-RU")
            #xrow = GoogleTranslator(source='ru', target='en').translate(text=row)
            #xrow = deepl.translate(source_language="RU", target_language="EN", text=row)
            #x.write(xrow)
x.close()
f.close()







