#!/usr/bin/env python3
import json
import os.path
import telebot


def updateConfFile(conf): json.dump(conf, open('conf.json', 'w'))


def createConfFile():
    data = {
        'asanaToken': '',
        'asanaProject': '',
        'asanaProjectName': '',
        'tgToken': '',
        'tgChatId': ''
    }
    updateConfFile(data)


def setupAsanaToken(conf):
    conf['asanaToken'] = input('Введите token для доступа к Asana API:')
    updateConfFile(conf)


def setupAsanaProject(conf):
    conf['asanaProject'] = input('Введите id проекта в Asana:')
    conf['asanaProjectName'] = input('Введите название проекта в Asana:')
    updateConfFile(conf)


def setupTgKey(conf):
    conf['tgToken'] = input('Введите ключ от телеграм-бота:')
    updateConfFile(conf)


def setupTgChat(conf):
    bot = telebot.TeleBot(conf['tgToken'])
    input('Напишите боту, чтобы он запомнил хозяина, и нажмите здесь Enter.')
    conf['tgChatId'] = bot.get_updates()[-1].message.chat.id
    updateConfFile(conf)


if not os.path.exists("conf.json"): createConfFile()
currentConfig = json.load(open('conf.json'))
if currentConfig['tgToken'] == '': setupTgKey(currentConfig)
if currentConfig['tgChatId'] == '': setupTgChat(currentConfig)
if currentConfig['asanaToken'] == '': setupAsanaToken(currentConfig)
if currentConfig['asanaProject'] == '' or currentConfig['asanaProjectName'] == '': setupAsanaProject(currentConfig)

tgToken = currentConfig['tgToken']
tgChatId = currentConfig['tgChatId']
asanaToken = currentConfig['asanaToken']
asanaProject = currentConfig['asanaProject']
asanaProjectName = currentConfig['asanaProjectName']
