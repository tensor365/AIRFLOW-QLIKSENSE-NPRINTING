from typing import Any, Callable, Dict, Optional

import time
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.models.connection import Connection
from airflow.providers.qlik_sense_nprinting.hooks.qlik_nprinting_hook_ntlm import QlikNPrintingHookNTLM

class QlikNPrintingReloadTaskOperator(BaseOperator):
    """
    Trigger a reload task of the app id passed in params.

    :conn_id: connection to run the operator with it
    :appId: str
    
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['taskId']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#00873d'

    @apply_defaults
    def __init__(self, *, taskId: str = None, conn_id: str = 'qlik_conn_sample', waitUntilFinished: bool = True, **kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.conn_type = Connection(conn_id=self.conn_id).conn_type
        self.taskId = taskId
        self.waitUntilFinished = waitUntilFinished
        
    def execute(self, context: Dict[str, Any]) -> Any:

        self.log.info("Initiating NTLM Hook")
        hook = QlikNPrintingHookNTLM(conn_id=self.conn_id)

        self.log.info("Call HTTP method to reload task {}".format(self.taskId))

        response = hook.reload_task(self.taskId)

        idExecution = None
        self.log.info('Status Code Return {}'.format(response.status_code))
        self.log.info('Answer Return {}'.format(response.text))
        if response.status_code in range(200,300):
            body = response.json()
            idExecution = body['data']['id'] # Adding Execution Id
        elif response.status_code == 403:
            raise ValueError("Error API: Authentification to triggered the task failed. Please check credentials in connection {}".format(self.conn_id))
        else:
            raise ValueError("Error API when triggering the new task {}".format(self.taskId))

        if self.waitUntilFinished:
            self.log.info('Synchronous mode activated waiting the ending of the execution {}'.format(idExecution))
            self.log.info('Heartbeat of the execution {} will start in 15s'.format(idExecution))
            time.sleep(15)
            flag=True
            while flag:
                ans = hook.check_status_reload(taskId=self.taskId, id=idExecution)
                self.log.info('Task status: {}'.format(ans.text))
                if ans.status_code == 200:
                    body = ans.json()
                    progressStatus = body['data']['progress']
                    reloadStatus = body['data']['status']
                    if progressStatus == 1.0:
                        flag=False
                        if reloadStatus.lower() == 'failed': 
                            raise ValueError('Error API: Task Run has failed. Please check logs to get more informations')
                else:
                    raise ValueError("API Error return")

        return response.text
