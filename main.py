import httpx
import time
import os
from dotenv import load_dotenv
from endpoints import (
    BINANCE_SYMBOL_PRICE_TICKER,
    KUCOIN_SYMBOL_PRICE_TICKER,
    BYBIT_SYMBOL_PRICE_TICKER,
    BINGX_SYMBOL_PRICE_TICKER)
from utils import TelegramUpdateHandler
from messages import WELCOME_MESSAGE, PRICE_LIST, ONLY_SUPPORTS_USDT

load_dotenv()

TELEGRAM_ACCESS_TOKEN = os.getenv('TELEGRAM_ACCESS_TOKEN')


def main():
    TELEGRAM_BOT = TelegramUpdateHandler(TELEGRAM_ACCESS_TOKEN)
    new_offset = 0

    while True:
        all_updates = TELEGRAM_BOT.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                first_update_id = current_update['update_id']

                if 'message' in current_update:
                    message = current_update['message']

                    if 'text' in message:
                        chat = message['chat']
                        chat_id = str(chat['id'])
                        symbol = message['text'].upper()

                        if symbol == '/START':
                            TELEGRAM_BOT.send_message(chat_id, WELCOME_MESSAGE)

                        elif symbol.endswith('USDT') or symbol == 'USDT':
                            # XXX Binance XXX
                            params = {'symbol': symbol}
                            res = httpx.get(
                                BINANCE_SYMBOL_PRICE_TICKER,
                                params=params
                            )

                            content = res.json()

                            if res.status_code == 200:
                                binance_price = float(content['price'])
                            else:
                                binance_price = '❌'

                            # XXX Kucoin XXX
                            params = {
                                'symbol': symbol.replace('USDT', '-USDT')
                            }

                            res = httpx.get(
                                KUCOIN_SYMBOL_PRICE_TICKER,
                                params=params
                            )

                            content = res.json()
                            data = content['data']
                            if data is not None:
                                kucoin_price = float(data['price'])
                            else:
                                kucoin_price = '❌'

                            # XXX Bybit XXX
                            params = {
                                'category': 'spot',
                                'symbol': symbol
                            }

                            res = httpx.get(
                                BYBIT_SYMBOL_PRICE_TICKER,
                                params=params
                            )

                            content = res.json()
                            if content['retCode'] == 0:
                                result = content['result']
                                result_list = result['list'][0]
                                bybit_price = float(result_list['lastPrice'])
                            else:
                                bybit_price = '❌'

                            # XXX BingX XXX
                            params = {
                                'symbol': symbol.replace('USDT', '-USDT'),
                                'timestamp': int(time.time() * 1000)
                            }

                            res = httpx.get(
                                BINGX_SYMBOL_PRICE_TICKER,
                                params=params
                            )

                            content = res.json()
                            if content['code'] == 0:
                                data = content['data'][0]
                                bingx_price = float(data['lastPrice'])

                            else:
                                bingx_price = '❌'

                            message = PRICE_LIST.format(
                                symbol=symbol,
                                binance_price=binance_price,
                                kucoin_price=kucoin_price,
                                bybit_price=bybit_price,
                                bingx_price=bingx_price
                            )

                            TELEGRAM_BOT.send_message(chat_id, message)

                        else:
                            TELEGRAM_BOT.send_message(
                                chat_id, ONLY_SUPPORTS_USDT)

                new_offset = first_update_id + 1


if __name__ == '__main__':
    while True:
        try:
            print('Launching CryptoPrice Checker Bot ...')
            main()

        except Exception as error:
            print(f'Caught an error: {error}')
            time.sleep(5)
