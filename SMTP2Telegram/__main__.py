import click
import asyncio
import logging
from aiosmtpd.controller import Controller
from .smtphandler import SMTPHandler
from .telegrambot import TelegramBot


async def amain(loop):
    controller = Controller(SMTPHandler(), hostname='', port=8025)
    controller.start()

def main():
    # Init
    bot = TelegramBot(token=bot_token)
    bot.send_message(chat_id=bot_chat_id, text="SMTP2Telegram Relay Initialized.")
    del bot
    # Initialize the loop
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(amain(loop=loop))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process Interrupted")
    finally:
        loop.close()

bot_token = '<token>'
bot_chat_id = <id>
if __name__ == "__main__":
    main()