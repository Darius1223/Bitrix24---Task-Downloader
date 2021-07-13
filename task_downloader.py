from fast_bitrix24 import Bitrix
from pprint import pprint

webhook = 'https://b24-j5kh1m.bitrix24.ru/rest/1/67g04mxqzhtfxtw0/'
b = Bitrix(webhook)

task_list = b.get_all(
    method='tasks.task.list.json',
    params={
        'filter':
            {
                "=STATUS": -1,
                "!PARENT_ID": None,
            },
        'select': [
            'TITLE',
            'ID',
            'DEPENDS_ON',
            'PARENT_ID',
            'STATUS'
        ]
    }
)

pprint(task_list)
