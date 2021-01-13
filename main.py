import asana
import time
import telegram
import config


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


fields = {'user', 'type', 'action', 'resource'}
client = asana.Client.access_token(config.asanaToken)
sync_token = ''

try:
    client.events.get({'resource': config.asanaProject}, opt_pretty=True)
except Exception as e:
    sync_token = e.sync
print('Started polling')

events = list()
while True:
    response = client.events.get({'resource': config.asanaProject, 'sync': sync_token}, opt_pretty=True,
                                 iterator_type=None)
    sync_token = response['sync']
    events = events + filterEmpty(response['data'])
    if not response['has_more']:
        telegram.sendUpdates(list(combineByTask(events).values()))
        events = list()
        time.sleep(5)
