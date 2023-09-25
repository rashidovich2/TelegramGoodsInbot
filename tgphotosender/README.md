### Details

The script continuously send messages to Telegram groups, with configurable sleep time between messages.
- The text of message is read from file "message.txt" (can be changed to other file from "messageFile" variable from script)
- The groups to send messages to, are read from file "groups.txt" (can be changed to other file from "groupsFile" variable from script)
- The script has a default value of sleep between messages in script variable "defaultSleepMinutesBetweenMessages". This value can be changed for a specific group by adding in the groups.txt at the end of chat id ", X", and replace X with the number of minutes
- The structure of groups.txt is:
   - 23235324, 4    <- first is the chat id, then comma then the interval in minutes between messages
   - 34534534       <- the chat id, and the default interval between messages will be used
- To also send a picture with the message, add its path in "picturePath.txt" file (can be changed to other file from "pictureFile" variable from script)

### How to get chat id of a group?

Unfortunately you cannot get easily the chatId by Group Name. The best (almost automated) way I could find to get the chadId from Group Name, is that during the run of the script, to fetch the "updates" of the bot, and to try to get the chatId from there

How exactly to get the mapping between group name and chat id?

Start the script, add the bot to a grup, and at the next run (by default in 30 seconds), the mapping between gorupName and chatId will be written in "mapping.txt" file (can be changed to other file from "groupsMappingFile" variable from script)

If the bot is already in a group, take it out, and readd it.

IMPORTANT NOTE!
This file "mapping.txt" is continuously building as the bot is added in new groups, so DO NOT DELETE IT.

### Prerequisites

- python3
- pip3
- Run: pip3 install requests telepot 

### How to create a Telegram bot

Create bot (tutorial on the web, basically download app, search for user: BotFather, and use command /newbot), and keep the TOKEN
For example you can use this tutorial: https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot

### How to configure the bot for the first time

- Make sure prerequisites are installed
- Create a folder with the code
- Update the parameter "botToken" from script with the bot token created previously
- If you want a picture to be sent, add path to it in script, in parameter "picturePathToSend". Otherwise leave the parameter ""
- Create file "message.txt" and enter there the message
- Create file "groups.txt" and enter the chatIds, one per line. Leave empty if do not know the chatIds
- Create file "picturePath.txt" and write there the path to image. Leave empty if no image should be sent
- Run the bot: python3 telegramBotSendMessageToGroups.py
- Add the bot in one group you want
- Wait for the next run (by default 30 seconds)
- Check file "mapping.txt" to see the mapping between the group and corresponding chat id
- Take the ID, and put it in groups.txt
- No need to restart the bot, it will always check the groups/message/image every run

### How to run the bot
- If the configurations did not change just run: python3 telegramBotSendMessageToGroups.py