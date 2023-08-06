import json
import logging
import requests
# from .base import BaseTask
from tgaflow.base import BaseTask

logger = logging.getLogger('task')


class CheckTask(BaseTask):
    def __init__(self, flow_id, params):
        self.task_name = 'check'
        super().__init__(flow_id, params, ['refresh'])
        self.url = self.settings['base_url'] + '/open/user-cluster-refresh-progress'

    def process(self):
        try:
            result = requests.get(self.url, headers={
                'Content-Type': 'application/json',
            }, params={
                ('token', self.settings['token']),
                ('projectId', self.params['projectId']),
                ('clusterId', self.params['clusterId']),
            }, timeout=300)
            logger.info('checktask success:%s %s', self.flow_id, result.text)
            resultArr = json.loads(result.text)

            if 'return_code' in resultArr and resultArr['return_code'] != 0:
                return False, {'result': result.text}
            elif int(resultArr['data']['progress']) < 100:
                return False, {'result': result.text}
            else:
                return True, {'result': result.text}
        except Exception as e:
            error_text = f'celry task {self.flow_id} {self.task.task_name} process Exception {e}'
            logger.info(error_text)
            return False, {'exception': error_text}


if __name__ == '__main__':
    checkTask = CheckTask(1, {'projectId': 4, 'clusterId': 168})
    checkTask.handle()
