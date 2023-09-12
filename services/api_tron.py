import time
import pytz
import requests
import json
from async_class import AsyncClass
from tronpy import Tron
from tronpy.keys import PrivateKey
from tgbot.utils.misc_functions import get_or_create_tron_account

class PaymentInfo:
    def __init__(self):
        self.data = [('status', ''), ('details', '')]

    def __repr__(self):
        return str(self.data)

class TronAPI(AsyncClass):
    client = None
    wallet = None
    tron_address = 'TYDpVsaSz2MuXYq4BhL3jgsJo7c1exNgQ9'
    private_key = None
    type_net = None

    async def __ainit__(self): #, user_id, type_net
        self.tron_address="TYDpVsaSz2MuXYq4BhL3jgsJo7c1exNgQ9"
        #self.tron_address = tron_address
        '''self.client = Tron(network='nile')
        self.type_net = type_net
        profile, check = await get_or_create_tron_account(wallet_user=user_id, wallet_net=type_net)
        if check:
            self.tron_address = profile['tron_address']
            self.type_net = profile['type_net']
            self.private_key = profile['private_key']
        else:
            self.tron_address = await self.client.generate_address(priv_key=PrivateKey(
                bytes.fromhex(profile['private_key']))
            )'''
        #print(self.tron_address)

    #@staticmethod
    async def get_address(self):
        #return self.wallet['tron_address']
        return self.tron_address

    # Создание платежа
    async def bill_pay(self, get_amount, get_way, get_coin):
        receipt = str(int(time.time() * 100))

        if get_way == "Tron":
            return_message = f"<b>🆙 Пополнение баланса {get_coin}</b>\n" \
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                             f"🥝 Для пополнения баланса, нажмите на кнопку ниже \n" \
                             f"<code>Перейти к оплате</code> и оплатите выставленный вам счёт\n" \
                             f"❗ У вас имеется 30 минут на оплату счета.\n" \
                             f"❗ Адрес: <code> TYDpVsaSz2MuXYq4BhL3jgsJo7c1exNgQ9 </code>.\n" \
                             f"💰 Сумма пополнения: <code>{get_amount} </code>\n" \
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                             f"🔄 После оплаты, нажмите на <code>Проверить оплату</code>"


            return return_message, receipt
        return False, False

    def get_balance(self):
        wallet = self.get_address()
        if self.type_net == 'TRX':
            try:
                return self.client.get_account_balance(wallet)
            except tronpy.exceptions.AddressNotFound:
                return 'AccountNotFound'
        elif self.type_net == 'USDT':
            r = requests.get('https://nileapi.tronscan.org/api/account/tokens'
                             f'?address={wallet}'
                             '&start=0'
                             '&limit=20'
                             '&token='
                             '&hidden=0'
                             '&show=0'
                             '&sortType=0')
            if r.status_code == 200:
                for token in r.json()['data']:
                    if token['tokenAbbr'].lower() == 'usdt':
                        print(token)
                        return token['quantity']
                else:
                    return float(0)

    def get_trans_by_wallet(self, type_net):
        #payload = {}
        #req = requests.get("https://api-pub.bitfinex.com/v2/ticker/tTRXUSD")
        #cresponse = requests.get(url, payload)
        #print(cresponse)
        #response = json.loads(cresponse.text)
        #wallet = self.get_address()
        wallet = 'TYDpVsaSz2MuXYq4BhL3jgsJo7c1exNgQ9'
        payload = {}
        if type_net == 'TRX':
            url = f"https://nileapi.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=20&start=0&address={wallet}"
            cresponse = requests.get(url, payload)
            print(cresponse)
            return json.loads(cresponse.text)
                #else:
                #    return {}
        elif type_net == 'USDT':
            url = f"https://nileapi.tronscan.org/api/token_trc20/transfers?sort=-timestamp&count=true&limit=20&start=0&relatedAddress={wallet}"
            cresponse = requests.get(url, payload) #, payload
            return json.loads(cresponse.text)
            #else:
            #    return {}


    def check_payment(self, user_id, local_worker, net, starttime=time.time(), payment=PaymentInfo().data):
        payment[1] = (False, 'WaitPay')
        total = local_worker.get_trans_by_wallet()['total']
        while True:
            if int(time.time()) - starttime >= 1800:
                payment[user_id] = (False, 'timeend')
                return
            trans = local_worker.get_trans_by_wallet()
            if net == 'TRX':
                if trans['total'] == total:
                    time.sleep(10)
                elif trans['data'][0]['toAddress'] == local_worker.get_address():
                    if int(trans['data'][0]['amount']) / 1000000 >= self:
                        print('Payment complete!')
                        payment[user_id] = (True, 'allpay')
                    else:
                        paysum_new = self - int(trans['data'][0]['amount']) / 1000000
                        payment[user_id] = (False, f'notall:{paysum_new}')
                        time.sleep(1)
                        check_payment(paysum_new, user_id, local_worker, net, starttime=starttime)
                    return
            elif trans['total'] == total:
                time.sleep(10)
            elif trans['token_transfers'][0]['to_address'] == local_worker.get_address():
                if int(trans['token_transfers'][0]['quant']) / 1000000 >= self:
                    payment[user_id] = (True, 'allpay')
                else:
                    paysum_new = self - int(trans['token_transfers'][0]['quant']) / 1000000
                    payment[user_id] = (False, f'notall:{paysum_new}')
                    time.sleep(1)
                    check_payment(paysum_new, user_id, local_worker, net, starttime=starttime)
                return