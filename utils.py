import httpx


class TelegramUpdateHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{token}/'

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'offset': offset, 'timeout': timeout}
        res = httpx.get(self.api_url + method, params=params, timeout=60)
        return res.json()['result']

    def send_message(self, chat_id, text, parse_mode='HTML'):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        method = 'sendMessage'
        return httpx.post(self.api_url + method, params=params, timeout=60)
