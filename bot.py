import logging
import telegram
from time import sleep

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError  # python 2

def help_message():
    response = 'Hi, I am a repeater bot!'
    return response

def main():
    # Telegram Bot Authorization Token
    bot = telegram.Bot('175682133:AAEkOAAMHUTDIH3ozHXAJ003cZD8CCWJ_lQ')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            update_id = echo(bot, update_id)
        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            elif e.message == "Unauthorized":
                # The user has removed or blocked the bot.
                update_id += 1
            else:
                raise e
        except URLError as e:
            # These are network problems on our end.
            sleep(1)


def echo(bot, update_id):

    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1
        message = update.message.text

        if message:
            if message == '/help':
                bot.sendMessage(chat_id=chat_id,
                            text= help_message())
            # Reply to the message
            else:
                bot.sendMessage(chat_id=chat_id,
                            text= message + str(update_id))

    return update_id


if __name__ == '__main__':
    main()
