#!/usr/bin/env python3
import os, sys


with open('/var/local/bot3101f/tgbot/locales/ru/LC_MESSAGES/en/mybot.po', encoding='UTF-8') as f:
    for row in f:
        print(row)

