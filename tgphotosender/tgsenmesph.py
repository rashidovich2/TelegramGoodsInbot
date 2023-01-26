import os
import sys
import time # for sleep
import logging # for logging
import telepot # for telegram use
import datetime # for logging
import requests # for Telegram API manipulation
import traceback # for error handling
import sqlite3
from tgbot.services.api_sqlite import get_all_positionsx, get_itemsx, get_positionx, get_categoryx
from tgbot.utils.misc_funcrions import get_position_of_day 

## Author: Eusebiu Rizescu
## Email: rizescueusebiu@gmail.com

# pip3 install requests telepot

## Variables
botToken = "5714149586:AAHDntl_ZxXe-BjnutLvJ0qPIepPURuZkCs"
messageFile = "message.txt" # Relative path to the message file that contains the text of the sending message
groupsFile = "groups.txt" # Relative path to the groups file. One chat id per line.
pictureFile = "picturePath.txt" # Relative path to the groups file. This file contians path to the image, or is empty
groupsMappingFile = "mapping.txt" # Relative path to the message file. It will be created by script, in order to have a mapping between GroupName and ChatId
defaultSleepMinutesBetweenMessages = 3
sleepSecondsBetweenRuns = 1800 # This should be lower that the smallest number of wait minutes for a group. 30 seconds is good.

## Needed variables
currentDir = os.getcwd()
lastUpdateEvent = 0

# Logging function
def getLogger():
  # Create logs folder if not exists
  if not os.path.isdir(os.path.join(currentDir, "logs")):
    try:
      os.mkdir(os.path.join(currentDir, "logs"))
    except OSError:
      print("Creation of the logs directory failed")
    else:
      print("Successfully created the logs directory")

  now = datetime.datetime.now()
  log_name = "" + str(now.year) + "." + '{:02d}'.format(now.month) + "." + '{:02d}'.format(now.day) + "-telegramBotSendMessageToGroups.py.log"
  log_name = os.path.join(currentDir, "logs", log_name)
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.NOTSET,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log

# Function that sends a message to a chatId
def sendTelegramMessage(log, chatId):
  try:
    # Read message
    #message = open(os.path.join(currentDir, messageFile), mode="r").read()
    bot = telepot.Bot(botToken)
    #picturePathToSend = open(os.path.join(currentDir, pictureFile), mode="r").read().replace(os.linesep, "").strip()
    #if picturePathToSend == "":
      # Send only message
    #  bot.sendMessage(chatId, message)
    #else:
      # Send photo with caption
    message, picturePathToSend=get_position_of_day()
    bot.sendPhoto(chatId, caption=message, photo=open(picturePathToSend, "rb"))

    return True
  except Exception as e:
    log.info("Error when sending Telegram message: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    return False

# Read the group mapping files to get the already known chat ids
# A line in group mapping file is:
# Name: <<<My_Group_X>>>, ChatId: <<<1938451051>>>
def readGroupsMapping(log):
  alreadyKnownGroups = []
  try:
    groupsMappings = open(os.path.join(currentDir, groupsMappingFile), "r")
    groupsMappings = groupsMappings.read().split(os.linesep)
    # Get group name from
    for groupMapping in groupsMappings:
      groupMapping = groupMapping.strip()
      if groupMapping == "" or groupMapping == os.linesep:
        continue
      try:
        groupName = groupMapping.split("<<<")[1].split(">>>")[0]
        alreadyKnownGroups.append(groupName)
      except Exception as e:
        log.info("ERROR when reading from group mapping, when processing: " + groupMapping)
        tracebackError = traceback.format_exc()
        log.info(tracebackError)

  except Exception as e:
    log.info("Error when reading groups mapping for bot: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)

  return alreadyKnownGroups


# For each run, get the updates of the bot and update the group mapping file with the new
# chat_ids. When a bot is added to a group, an update is accessible, and we parse that, and
# add the chat id to the group mapping file
def updateGroupsMapping(log):

  try:
    log.info("##### Run updateGroupsMapping")
    # Get groups from groups mapping
    alreadyKnownGroups = readGroupsMapping(log)

    # Get updates from Telegram
    bot = telepot.Bot(botToken)
    global lastUpdateEvent
    response = bot.getUpdates(offset=lastUpdateEvent)
    if len(response) == 0:
      log.info("No new updates for now. Nothing to add in the mappings file")
      return

    lastUpdateEvent = response[-1]["update_id"]

    # For each update, try to get if the bot was added in a group
    for update in response:
      if "my_chat_member" not in update:
        continue
      # Get the groupName and chatId
      groupName = update["my_chat_member"]["chat"]["title"]
      chatId = str(update["my_chat_member"]["chat"]["id"])
      log.info("Bot was added to group: " + groupName + " with chat id: " + chatId)
      if groupName in alreadyKnownGroups:
        log.info("We already have this group in mapping groups file")
      else:
        log.info("This is a new group, add it to the group mapping file")
        with open(os.path.join(currentDir, groupsMappingFile), 'a') as file:
          file.write("Name: <<<" + groupName + ">>>, ChatId: <<<" + chatId + ">>>" + os.linesep)

  except Exception as e:
    log.info("Error when getting Updates for bot: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)

# Function that read groups to send messages to from the file
# Groups file has the following format:
# 23235324, 4    <- first is the chat id, then comma then the interval between messages
# or
# 34534534       <- the chat id, and the default interval between messages will be used
def readGroups(log, oldDict):
  groups = open(os.path.join(currentDir, groupsFile), "r")
  groups = groups.read().split(os.linesep)

  groupsDict = {}
  # Get group name from
  for group in groups:
    group = group.strip()
    if group == "" or group == os.linesep:
      continue
    if "," in group:
      chatId = group.split(",")[0].strip()
      messageInterval = float(group.split(",")[1].strip())
    else:
      chatId = group
      messageInterval = defaultSleepMinutesBetweenMessages
    # Add the group to the dict
    if chatId in oldDict.keys():
      groupsDict[chatId] = {"messageInterval": messageInterval, "lastMessageTimestamp": oldDict[chatId]["lastMessageTimestamp"]}
    else:
      groupsDict[chatId] = {"messageInterval": messageInterval, "lastMessageTimestamp": 0}

  return groupsDict

# Main function
def mainFunction():
  log = getLogger()
  log.info("###################################################### New MAIN run")

  try:
    # Break if config files not found
    if os.path.isfile(os.path.join(currentDir, messageFile)) is False:
      log.info("Message file " + messageFile + " not found. Exiting.")
    if os.path.isfile(os.path.join(currentDir, groupsFile)) is False:
      log.info("Groups file " + groupsFile + " not found. Exiting.")
    if os.path.isfile(os.path.join(currentDir, pictureFile)) is False:
      log.info("Picture file " + pictureFile + " not found. Exiting.")

    # Create mappings group if not present
    if os.path.isfile(os.path.join(currentDir, groupsMappingFile)) is False:
      f = open(os.path.join(currentDir, groupsMappingFile), "a")
      f.write("")
      f.close()

    # At the start we assume that we should send messages to all groups
    oldGroupsDict = {}

    # Main while
    while True:
      log.info("##################### New run")
      # Get bot updates in order to see if the bot was added to a new group.
      updateGroupsMapping(log)

      # Read the groups
      groups = readGroups(log, oldGroupsDict)

      log.info("Groups: " + str(groups))

      # Send the message
      for group in groups.keys():

        log.info("### Processing group: " + group)
        now = time.time()

        if now - groups[group]["lastMessageTimestamp"] < groups[group]["messageInterval"] * 60:
          log.info("Time interval not already passed. Wait " + str(groups[group]["messageInterval"] * 60 - (now - groups[group]["lastMessageTimestamp"])) + " seconds.")
        else:
          log.info("Time interval passed. Sending message")
          status = sendTelegramMessage(log, group)
          if status == True:
            log.info("Message successfully sent.")
            groups[group]["lastMessageTimestamp"] = now
          else:
            log.info("Error, message not sent.")

      oldGroupsDict = groups
      # Sleep between runs
      log.info("Sleeping " + str(sleepSecondsBetweenRuns) + " seconds.")
      time.sleep(sleepSecondsBetweenRuns)

  ##### END #####
  except KeyboardInterrupt:
    log.info("Quit")
    sys.exit(0)
  except Exception as e:
    log.info("Fatal Error: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    sys.exit(98)


##### BODY #####
if __name__ == "__main__":

  if len(sys.argv) != 1:
    log.info("Wrong number of parameters. Use: python telegramBotSendMessageToGroups.py.py")
    sys.exit(99)
  else:
    mainFunction()
