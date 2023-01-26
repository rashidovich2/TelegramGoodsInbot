from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.messages import ReadHistoryRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsRecent
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import InputPeerEmpty

import os, sys
import configparser
import csv
import time
from tgbot.services.api_sqlite import *

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
´´´´¶¶¶¶¶¶´´´´´´¶¶¶¶¶¶
´´¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶¶¶¶¶¶¶
´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ´¶¶¶¶¶´
´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶
´´´´´´´´´¶¶¶¶¶¶¶¶
´´´´´´´´´´´¶¶¶¶
{re}

by rikudo
        """)
        

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
 
os.system('clear')
banner()
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print(gr+'[+] Choose a group to scrape members :'+re)
i=0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+ g.title)
    i+=1
 
print('')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group=groups[int(g_index)]
 
print(gr+'[+] Fetching Members...')
time.sleep(1)

#all_participants = self.client.get_participants(target_Group)

#all_participants = []
#while_condition = True
#my_filter = ChannelParticipantsSearch('')
#offset = 0
#while while_condition:
#	participants = self.client(GetParticipantsRequest(channel=target_Group,  offset= offset, filter = my_filter, limit=200, hash=0))
#	all_participants.extend(participants.users)
#	offset += len(participants.users)
#	print(len(participants.users))
#	if len(participants.users) < 1 :
#		while_condition = False


offset = 0
limit = 100
all_participants = []
channel = 'building_work'
while True:
    participants = client(GetParticipantsRequest(
        channel, ChannelParticipantsRecent(), offset, limit,
        hash=0
    ))
    if not participants.users:
        break
    all_participants.extend(participants.users)
    offset += len(participants.users)
    print(offset)

 
print(gr+'[+] Saving In file...')
time.sleep(1)
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        state = ""
        groupname = target_group.title
        usah = user.access_hash
        usid = user.id
        source = 'groups'
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
        add_tgacc_todb(username,usid,usah,name,source,state)

print(gr+'[+] Members scraped successfully.')