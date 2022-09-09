# - *- coding: utf- 8 - *-
import json
from base64 import b64decode
from datetime import datetime, timedelta, timezone

from async_class import AsyncClass

from tgbot.services.api_session import AsyncSession
from tgbot.utils.const_functions import get_unix


# Апи работы с QIWI P2P
class QiwiAPIp2p(AsyncClass):
    async def __ainit__(self, dp, secret, skip_key_validation=False):
        if not skip_key_validation:
            await self.validate_privkey(secret)

        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {secret}"}
        self.secret = secret
        self.dp = dp

    @staticmethod
    async def validate_privkey(privkey):
        try:
            key_decoded = b64decode(privkey).decode()
            key_decoded = json.loads(key_decoded)

            if "version" in key_decoded and "data" in key_decoded:
                key_data = key_decoded["data"]

                if "payin_merchant_site_uid" in key_data and "user_id" in key_data and "secret" in key_data:
                    return key_decoded["version"] == "P2P"
        except:
            pass

        raise ValueError("Invalid private key")

    # Конвертация времени
    @staticmethod
    async def convert_date(lifetime: int):
        datetime_new: datetime = datetime.now(timezone(timedelta(hours=3))).replace(microsecond=0)
        datetime_new = datetime_new + timedelta(minutes=lifetime)

        return datetime_new.astimezone(timezone(timedelta(hours=3))).replace(microsecond=0).isoformat()

    # Создание P2P формы
    async def bill(self, bill_amount, bill_id=None, lifetime=10):
        if bill_id is None: bill_id = get_unix(True)

        bill_amount = str(round(float(bill_amount), 2))

        send_json = {
            "amount": {
                "currency": "RUB",
                "value": bill_amount
            },
            "comment": bill_id,
            "expirationDateTime": await self.convert_date(lifetime)
        }

        status, response = await self._request(
            "put", f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}", send_json)

        return response['billId'], f"https://phoenix-bot.pw/api/v1/qiwi/create_bill/{response['payUrl'].split('=')[1]}"

    # Проверка P2P формы
    async def check(self, bill_id):
        status, response = await self._request(
            "get", f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}")

        return response['status']['value'], int(float(response['amount']['value']))

    # Отмена P2P формы
    async def reject(self, bill_id):
        status, response = await self._request(
            "post", f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}/reject")

        return status

    # Сам запрос
    async def _request(self, bill_method, bill_url, bill_json=None):
        aSession: AsyncSession = self.dp.bot['aSession']
        session = await aSession.get_session()

        try:
            response = await session.request(bill_method, bill_url, json=bill_json, headers=self.headers, ssl=False)

            if response.status == 200:
                return True, json.loads((await response.read()).decode())
        except:
            pass

        raise ValueError("Invalid private key")
