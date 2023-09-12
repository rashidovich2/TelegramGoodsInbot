#!/usr/bin/env python3
import os, sys
import deepl

with open("mybotr.po", "a") as x:
    with open('mybot.po', encoding='UTF-8') as f:
        idblock=""
        idblock2=""
        lines = f.readlines()
        for row in lines:
            if row[0] == '"':
                idblock = idblock + row
                xr2 = deepl.translate(source_language="RU", target_language="EN", text=row)
                idblock2 = idblock2 + xr2
                print(idblock)
                print(idblock2)
                print("1")
            if 'msgid ' in row:
                print("2")
                print("2-1")
                if 'msgid ""' in row:
                    idblock = f'{idblock}msgid ""' + "\n"
                    idblock2 = f'{idblock2}msgstr ""' + "\n"
                else:
                    idblock= idblock + row + "\n"
                    xb2 = deepl.translate(source_language="RU", target_language="EN", text=row[7:])
                    idblock2 = f'{idblock2}msgstr {xb2}'
                    continue
                print(row[7:])
                        #x.write('msgstr ' + row[6:])
            elif 'msgstr' in row:
                print("3")
                x.write(idblock)
                x.write(idblock2)
                idblock = ""
                idblock2 = ""
                continue
            elif row[0] == "\n":
                print("4")
                x.write('\n')
                #idblock= idblock + row
                #idblock2= idblock2 + row
            else:
                xrow = deepl.translate(source_language="RU", target_language="EN", text=row)
                x.write(xrow)
f.close()







