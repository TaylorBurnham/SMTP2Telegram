import html
import logging
from email import message_from_bytes
from email.policy import default
from .telegrambot import TelegramBot

class SMTPHandler:
    """
        Heavily lifted from the controller docs

        https://aiosmtpd.readthedocs.io/en/latest/controller.html
    """
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address == 'taylor@burnham.io':
            return "550 not relaying to that recipient"
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        # Print Output
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print('End of message')
        # Process the Envelope
        message = self.parse_envelope(envelope)
        payload = self.conv_envelope(message)
        bot = TelegramBot(token=bot_token)
        bot.send_message(
            chat_id=bot_chat_id, payload=payload
        )
        del bot
        return '250 Message accepted for relay'

    def parse_envelope(self, envelope):
        """ Parses the envelope from aiosmtpd """
        message = message_from_bytes(envelope.content, policy=default)
        body = self.get_msg_text(message)
        content = {
            "date": message['Date'],
            "from": message['From'],
            "to": message['To'],
            "subject": message['Subject'],
            "body": body
        }
        return content

    def conv_envelope(self, msg):
        plmsg = """
<b>Message Received from {msg_from} at {msg_date}</b>
<b>Subject:</b> {msg_subj}
<pre>
{msg_body}
</pre>
        """.format(
            msg_from=html.escape(msg['from']),   msg_date=html.escape(msg['date']),
            msg_subj=html.escape(msg['subject']), msg_body=html.escape(msg['body'])
        )
        pl = {
            "parse_mode": "HTML",
            "text": plmsg
        }
        return pl

    def get_msg_text(self, msg):
        if msg.is_multipart():
            return self.get_msg_text(msg.get_payload(0))
        else:
            return msg.get_payload(None)

