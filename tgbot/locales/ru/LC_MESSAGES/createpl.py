#!/usr/bin/env python3
import os, sys

x = open("mybotr.po", "a")
with open('mybot.po', encoding='UTF-8') as f:
    idblock=""
    idblock2=""
    lines = f.readlines()
    for row in lines:
        if row[0] == '"':
            idblock = idblock + row
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
                idblock2= idblock2 + 'msgstr ' + row[7:]
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
        else: x.write(row)
x.close()
f.close()







