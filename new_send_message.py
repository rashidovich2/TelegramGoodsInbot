import time
from selenium import webdriver
import telegram

def updateStatus():
    browser.find_element_by_xpath('//*[@id="paramInvcNo"]').send_keys(num)
    browser.find_element_by_xpath('//*[@id="btnSubmit"]').click()
    status = browser.find_element_by_xpath('//*[@id="statusDetail"]')
    return status.text

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
browser = webdriver.Chrome("Location of Chrome Driver", options = options)
browser.implicitly_wait(5)
url = 'https://www.cjlogistics.com/ko/tool/parcel/tracking'
browser.get(url)
myToken = 'TelegramToken'
bot = telegram.Bot(token = myToken)
chat_id = ID#bot.getUpdates()[-1].message.chat.id #가장 최근에 온 메세지의 chat id를 가져옵니다
num = 운송장 번호
statusArr = ["", ""]

i = 0
while True:
    status = updateStatus()
    statusArr[i%2] = str(status)
    if statusArr[0] != statusArr[1]:
        bot.sendMessage(chat_id=chat_id, text=statusArr[i%2])
        print('Different')
    browser.refresh()
    time.sleep(1)
    i = i+1