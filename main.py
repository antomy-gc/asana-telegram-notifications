import asana
import time
import telegram
import config

fields = {'user', 'type', 'action', 'resource'}
client = asana.Client.access_token(config.asanaToken)
pollTimeout = 30


def filterEmpty(updates):
    result = list()
    for update in updates:
        if (update['type'] == 'task') and (update['resource']['name'] != ''):
            result.append(update)
    return result


def combineByTask(updates):
    result = dict()
    for update in updates:
        gid = update['resource']['gid']
        if gid not in result: result[gid] = list()
        result[gid].append(update)
    return result


def obtainSyncToken():
    try:
        client.events.get({'resource': config.asanaProject}, opt_pretty=True)
    except Exception as e:
        return e.sync
    print('Started polling')


events = list()
syncToken = obtainSyncToken()
try:
    while True:
        try:
            response = client.events.get({'resource': config.asanaProject, 'sync': syncToken}, opt_pretty=True, iterator_type=None)
            syncToken = response['sync']
            events = events + filterEmpty(response['data'])
            if not response['has_more']:
                telegram.sendUpdates(list(combineByTask(events).values()))
                events = list()
                time.sleep(pollTimeout)
        except Exception:
            telegram.sendPlainText('Exception occurred. Trying to recover')
            syncToken = obtainSyncToken()
except Exception:
    telegram.sendPlainText('Bot crashed. Please, restart')
