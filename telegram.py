import telebot
import time
import config
import task_formatter

bot = telebot.TeleBot(config.tgToken)


def sendPlainText(text):
    if len(text) > 4090:
        bot.send_message(config.tgChatId, text[:4089] + '[...]', parse_mode='MarkdownV2')
        sendPlainText('[...]' + text[4089:])
    else:
        bot.send_message(config.tgChatId, text, parse_mode='MarkdownV2')
    time.sleep(1)


def sendUpdates(updates):
    for task in updates:
        sendPlainText(task_formatter.formatTask(task))
