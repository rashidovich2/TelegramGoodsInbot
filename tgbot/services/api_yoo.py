# - *- coding: utf- 8 - *-
import asyncio
import json
import time

from aiohttp import ClientConnectorCertificateError
from async_class import AsyncClass
from yoomoney import Client
from yoomoney import Quickpay


from tgbot.services.api_session import RequestsSession
from tgbot.services.api_sqlite import update_paymentx, get_upaymentx, get_paymentx, update_upaymentx
from tgbot.utils.misc_functions import send_admins


# Апи работы с YooMoney
class YooAPI(AsyncClass):
    async def __ainit__(self, suid, acc_number=None, token=None, client_id=None, redirect_url=None, **kwargs):
        print(suid['chat']['id'])
        self.suser_id = 919148970 #suid['chat']['id'] or
        self.token = get_upaymentx(self.suser_id)['yoo_token']
        self.client_id = get_upaymentx(self.suser_id)['yoo_client_id']
        self.acc_number = get_upaymentx(self.suser_id)['yoo_acc_number']
        self.redirect_url = get_upaymentx(self.suser_id)['yoo_redirect_url']

    # Рассылка админам о нерабочем киви
    @staticmethod
    async def error_wallet():
        await send_admins("<b> Yoo кошелёк недоступен ❌</b>\n"
                          "❗ Как можно быстрее его замените ❗")

    #Обновление данных
    async def update_yoo(self):
        update_upaymentx(user_id=self.suser_id, yoo_acc_number=self.acc_number, yoo_token=self.token, yoo_client_id=self.client_id, yoo_redirect_url=self.redirect_url)


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
                    update_upaymentx(user_id=self.suser_id, qiwi_login=self.login, qiwi_token=self.token, qiwi_secret=self.secret)
                else:
                    return False
            elif self.check_pass:
                if status:
                    text_secret = "Отсутствует" if self.secret == "None" else self.secret
                    await self.dp.answer(f"<b>🥝 Qiwi кошелёк полностью функционирует ✅</b>\n"
                                         f"◾ Номер: <code>{self.login}</code>\n"
                                         f"◾ Токен: <code>{self.token}</code>\n"
                                         f"◾ Приватный ключ: <code>{text_secret}</code>")
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

    # Проверка баланса
    async def get_balance(self):
        response = await self.pre_checker()
        if response:
            status, response, code = await self._request(
                "funding-sources",
                "v2",
                "accounts",
            )

            save_balance = []
            for balance in response['accounts']:
                if balance['alias'] == "qw_wallet_usd":
                    save_balance.append(f"🇺🇸 Долларов: <code>{balance['balance']['amount']}$</code>")

                if balance['alias'] == "qw_wallet_rub":
                    save_balance.append(f"🇷🇺 Рублей: <code>{balance['balance']['amount']}₽</code>")

                if balance['alias'] == "qw_wallet_eur":
                    save_balance.append(f"🇪🇺 Евро: <code>{balance['balance']['amount']}€</code>")

                if balance['alias'] == "qw_wallet_kzt":
                    save_balance.append(f"🇰🇿 Тенге: <code>{balance['balance']['amount']}₸</code>")

            save_balance = "\n".join(save_balance)
            await self.dp.answer(f"<b>🥝 Баланс кошелька <code>{self.login}</code> составляет:</b>\n"
                                 f"{save_balance}")

    # Проверка п2п ключа
    async def check_secret(self):
        try:
            qiwi_p2p = QiwiP2P(self.secret)
            bill = qiwi_p2p.bill(amount=1, lifetime=1)
            qiwi_p2p.reject(bill_id=bill.bill_id)
            return True
        except Exception:
            return False

    # Создание платежа
    async def bill_pay(self, get_amount, get_way, lang):
        print(self, get_amount, get_way, lang)

        receipt = str(int(time.time() * 100))
        print(receipt)

        if get_way == "ForYm":
            quickpay = Quickpay(
            receiver=self.acc_number, #'410011512189686', 
            quickpay_form="shop",
            targets="Pay for goods in bot",
            paymentType="SB",
            sum=get_amount,
            label=receipt,
            )

            print(quickpay.base_url)

            send_requests = quickpay.base_url

            print(quickpay.redirected_url)

            if lang == "ru":
                return_message = f"<b>🆙 Пополнение баланса Yoomoney</b>\n" \
                                 f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                                 f"🥝 Для пополнения баланса, нажмите на кнопку ниже \n" \
                                 f"<code>Перейти к оплате</code> и оплатите выставленный вам счёт\n" \
                                 f"❗ У вас имеется 30 минут на оплату счета.\n" \
                                 f"💰 Сумма пополнения: <code>{get_amount}₽</code>\n" \
                                 f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                                 f"🔄 После оплаты, нажмите на <code>Проверить оплату</code>"

            if lang == "en":
                return_message = f"<b>🆙 Put money to your account by Yoomoney</b>\n" \
                                 f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                                 f"🥝 To fill balance, push button beside. \n" \
                                 f"<code>Go to payment</code> and create this one.\n" \
                                 f"❗ You  have 30 minutes for paying operation.\n" \
                                 f"💰 Ammount to pay: <code>{get_amount}₽</code>\n" \
                                 f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                                 f"🔄 After payout, press on <code>Check payment</code>"

            return return_message, send_requests, receipt
        return False, False, False

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

    # Запросы
'''    async def _request(self, action, version, get_way, params=None):
        url = self.base_url.format(action, version, self.login, get_way)

        rSession: RequestsSession = self.dp.bot['rSession']
        session = await rSession.get_session()

        try:
            response = await session.get(url, params=params, headers=self.headers, ssl=False)
            return True, json.loads((await response.read()).decode()), response.status
        except ClientConnectorCertificateError:
            return False, None, "CERTIFICATE_VERIFY_FAILED"
        except:
            return False, None, response.status'''
