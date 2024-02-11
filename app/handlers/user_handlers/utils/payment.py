import base64
import hashlib
from json import dumps, JSONDecodeError
import uuid
from os import getenv

from httpx import AsyncClient, Response


class PaymentError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code: int | None = error_code


class CryptoPayment:
    @staticmethod
    def __make_invoice_payment(price: int) -> dict:
        return {
            "amount": str(price),
            "currency": "USD",
            "order_id": str(uuid.uuid4()),
        }

    @staticmethod
    def __make_invoice_check_payment(payment_id: str) -> dict:
        return {"uuid": payment_id}

    @staticmethod
    def __make_signature(invoice_data: dict) -> str:
        encoded_data = base64.b64encode(
            dumps(invoice_data).encode("utf-8")
        ).decode("utf-8")
        return hashlib.md5(
            f"{encoded_data}{getenv('API_KEY')}".encode("utf-8")
        ).hexdigest()

    @staticmethod
    def __dispatch_response(response: Response) -> dict | str:
        try:
            return response.json()
        except JSONDecodeError:
            return ""

    @classmethod
    async def __make_request(
        cls, url: str, signature: str, invoice_data: dict
    ):
        async with AsyncClient() as client:
            response = await client.request(
                method="POST",
                url=url,
                headers={
                    "merchant": getenv("MERCHANT_ID"),
                    "sign": signature,
                },
                json=invoice_data,
                timeout=10,
            )
        response_data = cls.__dispatch_response(response)
        if not isinstance(
            response_data, dict
        ) and response.status_code in range(200, 300):
            raise PaymentError(
                f"Не удалось получить успешный ответ от апи.\n"
                f"Response: {response_data}"
            )
        elif not response_data.get("result", False):
            raise PaymentError(
                f"Необработанный ответ от апи.\n" f"Response: {response_data}"
            )
        return response.json()["result"]

    @classmethod
    async def make_payment(cls, price: int):
        invoice_data = cls.__make_invoice_payment(price=price)
        return await cls.__make_request(
            url="https://api.cryptomus.com/v1/payment",
            signature=cls.__make_signature(invoice_data),
            invoice_data=invoice_data,
        )

    @classmethod
    async def check_payment(cls, payment_id: str):
        invoice_data = cls.__make_invoice_check_payment(payment_id=payment_id)
        return await cls.__make_request(
            url="https://api.cryptomus.com/v1/payment/info",
            signature=cls.__make_signature(invoice_data),
            invoice_data=cls.__make_invoice_check_payment(
                payment_id=payment_id
            ),
        )
