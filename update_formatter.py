import config
import asana

updateActionsText = {
    'changed': 'изменена',
    'added': 'добавлена',
    'removed': 'перемещена',
    'deleted': 'удалена',
    'undeleted': 'восстановлена'
}

fieldActionsText = {
    'changed': 'Изменено',
    'added': 'Добавлено',
    'removed': 'Удалено'
}


def escapeChars(text):
    return text.replace('.', '\.').replace('_', '\_').replace('-', '\-')


def replaceChars(text):
    return text.replace('_', '\_').replace('.', '\_').replace('-', '\_')


def changed(update):
    change = update['change']
    return '{} поле `{}`\n'.format(fieldActionsText[change['action']], change['field'])


def added(update):
    return 'Добавлена в `{}`\n'.format(escapeChars(update['parent']['name']))


def removed(update):
    return 'Удалена из `{}`\n'.format(escapeChars(update['parent']['name']))


def deleted(update):
    return 'Удалена\n'


def undeleted(update):
    return 'Восстановлена\n'


actions = {
    'changed': changed,
    'added': added,
    'removed': removed,
    'deleted': deleted,
    'undeleted': undeleted
}


def header(firstUpdate):
    return 'Задача `{}` {}\.\n'.format(escapeChars(firstUpdate['resource']['name']), updateActionsText[firstUpdate['action']])


def footer(lastUpdate):

    try:
        client = asana.Client.access_token(config.asanaToken)
        fullTask = client.tasks.get_task(lastUpdate['resource']['gid'], opt_pretty=True)
        result = 'Статус: `{}`\. [Подробнее]({})\n' \
            .format('завершена' if fullTask['completed'] else 'не завершена', fullTask['permalink_url'])
        for tag in fullTask['tags']:
            result += '\#{} '.format(replaceChars(tag['name']))
        return result
    except Exception:
        return ''


def formatTask(taskUpdates):
    result = 'Проект: `{}`\n'.format(config.asanaProjectName)
    result += header(taskUpdates[1])
    result += 'Все события:\n'
    for update in taskUpdates:
        result += actions[update['action']](update)
    result += footer(taskUpdates[-1])
    return result
