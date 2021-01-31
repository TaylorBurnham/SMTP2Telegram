import logging
import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.telegram.org/bot{TOKEN}/".format(TOKEN=self.token)

    def get_updates(self):
        request_url = self.base_url + "getUpdates"
        updates = requests.get(request_url)
        return updates.json()

    def send_message(self, chat_id, payload=None, text=None, notify=True):
        if not payload and not text:
            raise("Must supply text or payload.")
        request_url = self.base_url + "sendMessage"
        request_params = {
            "chat_id": chat_id,
            "disable_notification": not notify
        }
        # If it's only a text message go.
        if text:
            request_params['text'] = text
            sendmsg = requests.get(request_url, params=request_params)
            return sendmsg.json()
        else:
            request_params['parse_mode'] = payload['parse_mode']
            request_params['text'] = payload['text']
            sendmsg = requests.get(request_url, params=request_params)
            return sendmsg.json()