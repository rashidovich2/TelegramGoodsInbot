# - *- coding: utf- 8 - *-
import asyncio
import json
import time

from aiohttp import ClientConnectorCertificateError
from async_class import AsyncClass
#from yoomoney import Client
from coinbase.wallet.client import Client

from tgbot.services.api_session import RequestsSession
from tgbot.services.api_sqlite import update_paymentx, get_upaymentx, get_paymentx, update_upaymentx
from tgbot.utils.misc_functions import send_admins


# Апи работы с YooMoney
class CoinbaseAPI(AsyncClass):
    async def __ainit__(self, suser_id=None, api_key=None, api_token=None):
        self.suser_id = 919148970
        self.api_token = get_upaymentx(self.suser_id)['coinbase_token']
        self.api_key = get_upaymentx(self.suser_id)['coinbase_key']
        self.pay_method = get_upaymentx(self.suser_id)['way_coinbase']
        print(self.api_token, self.api_key, self.pay_method)
        client = Client(api_key, api_secret)
        account_id = client.get_primary_account()['id']
        print(usdt_price)
        sum = float(str(get_amount / usdt_price)[:10]) #сколько сатох нужно юзеру оплатить
        address_for_tranz = client.create_address(account_id)['address'] #получение кошелька для оплаты
        print(address_for_tranz)

        '''if suser_id is not None:
            self.suser_id = suser_id
            self.api_token = get_upaymentx(self.suser_id)['coinbase_token']
            self.api_key = get_upaymentx(self.suser_id)['coinbase_key']
            self.pay_method = get_upaymentx(self.suser_id)['way_coinbase']
                #self.token = token
                #self.client_id = client_id
                #self.acc_number = acc_number
                #self.redirect_url = redirect_url
        else:
            #self.login = get_upaymentx(self.user_id)['qiwi_login']
            #self.token = get_upaymentx(self.user_id)['qiwi_token']
            #self.secret = get_upaymentx(self.user_id)['qiwi_secret']
            #self.login = get_paymentx()['qiwi_login']
            self.suser_id = 919148970
            self.api_token = get_upaymentx(self.suser_id)['coinbase_token']
            self.api_key = get_upaymentx(self.suser_id)['coinbase_key']
            self.pay_method = get_upaymentx(self.suser_id)['way_coinbase']
            #self.base_url = "https://yoomoney.ru/api/"
            #self.headers = {"authorization": f"Bearer {self.token}"}
            #self.client_id = get_paymentx()['yoo_client_id']
            #self.user_check_pass = user_check_pass
            #self.user_bill_pass = user_bill_pass
            #self.check_pass = check_pass
            #self.add_pass = add_pass
            #self.dp = dp
        print(self.api_token, self.api_key, self.pay_method)

            #api_key = 'QUmnMHJ7OrOJnIM4'
            #api_secret = 'gQr0L7ypPQXTpYRDzXJFILcAARRjBynH'
            #client = Client(api_key, api_secret)
            #account_id = client.get_primary_account()['id']


            #sum = int(sum) + 10 #прибавляется комиссия в btc
            #btc_price = round(float((client.get_buy_price(currency_pair='BTC-RUB')["amount"])))
            #print(btc_price)
            #sum = float(str(sum / btc_price)[:10]) #сколько сатох нужно юзеру оплатить
            #address_for_tranz = client.create_address(account_id)['address'] #получение кошелька для оплты
            #print(address_for_tranz)'''

    # Рассылка админам о нерабочем киви
    @staticmethod
    async def error_wallet():
        await send_admins("<b> Yoo кошелёк недоступен ❌</b>\n"
                          "❗ Как можно быстрее его замените ❗")

    #Обновление данных
    async def update_coinbase(self):
        update_upaymentx(user_id=self.suser_id, coinbase_key=self.api_key, coinbase_token=self.api_token, yoo_client_id=self.client_id)

    # Обязательная проверка перед каждым запросом
    async def pre_checker(self):
        if self.acc_number != "None":
            if self.add_pass:
                status, response = await self.check_account()
            else:
                status, response, code = await self.check_logpass()
            await asyncio.sleep(0.5)

            if self.add_pass:
                await self.dp.edit_text(response)
                if status:
                    update_upaymentx(user_id=self.suser_id, coinbase_key=self.api_key, coinbase_token=self.api_token, yoo_client_id=self.client_id)
                else:
                    return False
            elif self.check_pass:
                if status:
                    text_secret = "Отсутствует" if self.secret == "None" else self.secret
                    await self.dp.answer(f"<b> Coinbase кошелёк полностью функционирует ✅</b>\n"
                                         f"◾ Кошелек: <code>{self.login}</code>\n"
                                         f"◾ Токен: <code>{self.token}</code>")
                else:
                    await self.error_wallet()
                    return False
            elif self.user_bill_pass:
                if not status:
                    await self.dp.edit_text(
                        "<b>❗ Извиняемся за доставленные неудобства, пополнение временно недоступно.\n"
                        "⌛ Попробуйте чуть позже.</b>")
                    await self.error_wallet()
                    return False
            elif self.user_check_pass:
                if not status:
                    await self.dp.answer(
                        "❗ Извиняемся за доставленные неудобства, проверка временно недоступна.\n"
                        "⌛ Попробуйте чуть позже.", True)
                    await self.error_wallet()
                    return False
            elif not status:
                await self.error_wallet()
                return False

            return True
        else:
            if self.user_bill_pass:
                await self.dp.edit_text(
                    "<b>❗ Извиняемся за доставленные неудобства, пополнение временно недоступно.\n"
                    "⌛ Попробуйте чуть позже.</b>")
            await self.error_wallet()
            return False


    # Создание платежа
    async def bill_pay(self, get_amount, get_way):
        client = Client(api_key, api_secret)
        account_id = client.get_primary_account()['id']
        print(usdt_price)
        sum = float(str(get_amount / usdt_price)[:10]) #сколько сатох нужно юзеру оплатить
        address_for_tranz = client.create_address(account_id)['address'] #получение кошелька для оплаты
        print(address_for_tranz)
        '''account_id = client.get_primary_account()['id']
        sum = int(sum) + 10 #прибавляется комиссия в btc
        usdt_price = round(float((client.get_buy_price(currency_pair='USDT-RUB')["amount"])))
        print(usdt_price)
        sum = float(str(sum / usdt_price)[:10]) #сколько сатох нужно юзеру оплатить
        address_for_tranz = client.create_address(account_id)['address'] #получение кошелька для оплты
        print(address_for_tranz)
        receipt = str(int(time.time() * 100))'''

        if get_way == "CoinBase":
            return_message = f"<b>🆙 Пополнение баланса USDT</b>\n" \
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                             f"🥝 Для пополнения баланса, нажмите на кнопку ниже \n" \
                             f"<code>Перейти к оплате</code> и оплатите выставленный вам счёт\n" \
                             f"❗ У вас имеется 30 минут на оплату счета.\n" \
                             f"❗ Адрес:{address_for_tranz}.\n" \
                             f"💰 Сумма пополнения: <code>{get_amount}₽</code>\n" \
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                             f"🔄 После оплаты, нажмите на <code>Проверить оплату</code>"

            return return_message, receipt
        return False, False

    # Проверка платежа по форме
    async def check_formy(self, receipt):

        print(self.token)

        client = Client(self.token)
        history = client.operation_history(label=receipt)

        for operation in history.operations:

            pay_status = operation.status  # Получение статуса платежа
            pay_amount = int(float(operation.amount))  # Получение суммы платежа в рублях

        return pay_status, pay_amount

    # Проверка платежа по переводу
    async def check_send(self, receipt):
        response = await self.pre_checker()
        if response:
            status, response, code = await self._request(
                "payment-history",
                "v2",
                "payments",
                {"rows": 30, "operation": "IN"},
            )

            pay_status = False
            pay_amount = 0

            for check_pay in response['data']:
                if str(receipt) == str(check_pay['comment']):
                    if str(check_pay['sum']['currency']) == "643":
                        pay_status = True
                        pay_amount = int(float(check_pay['sum']['amount']))
                    else:
                        return_message = 1
                    break

            return_message = 3 if pay_status else 2
            return return_message, pay_amount

        return 4, False
