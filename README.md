# Asana telegram notifications bot

Для установки создайте бота в телеграм в [@BotFather](https://t.me/BotFather) и сохраните токен для доступа.

Также понадобится токен для доступа к API Asana, он создается в [developer console](https://app.asana.com/0/developer-console)



Запустите скрипт `start.sh` и следуйте инструкциям:

Название проекта - любая строка, используется только для составления уведомлений. 

ID проекта можно получить из адресной строки браузера при просмотре списка задач:
app.asana.com/0/`[projectID]`/list или используя [API explorer](https://developers.asana.com/explorer)


Важно: скрипт отправляет уведомления в телеграм с использованием MarkdownV2, при этом экранируются только символы `\_ \- \.`\. Если из Asana вы ожидаете получить 
один из спецсимволов Markdown, добавьте их экранирование в функцию `escapeChars` для названий обьектов Asana и в `replaceChars` для тегов задач в файле `task_formatter.py`
