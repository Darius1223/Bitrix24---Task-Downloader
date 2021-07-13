from pprint import pprint
import json
from bitrix24 import *

webhook = 'https://b24-j5kh1m.bitrix24.ru/rest/1/67g04mxqzhtfxtw0'
bx24 = Bitrix24(webhook)

task_list = bx24.callMethod(
    method='tasks.task.list',
    select=['ID', 'TITLE', 'PARENT_ID', 'STATUS', 'PARENT_ID'],
    filter={
        'STATUS': '-1',
        '!PARENT_ID': None
    }

)

pprint(task_list)
