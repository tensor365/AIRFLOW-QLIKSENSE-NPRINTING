from typing import Any, Callable, Dict, Optional, Union
from wsgiref.validate import validator

import requests

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from requests_ntlm2 import HttpNtlmAuth

class QlikNPrintingHookNTLM(BaseHook):
    """
    Qlik Sense Hook to interract with a On-Promise Site Qlik Sense Server
    
    """

    conn_name_attr = 'qlik_nprinting_conn_id'
    default_conn_name = 'qlik_nprinting_default'
    conn_type = 'qlik_sense_nprinting'
    hook_name = 'Qlik Sense NPrinting'
    __cookie_session =''
    __web_cookie_session=''

    def __init__(self,conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.base_url: str = ""
    
    def reload_task(self, taskId: str= ""):
        """
        
        Method used to reload task
        
        """

        URI = 'api/v1/tasks/{taskId}/executions'.format(taskId=taskId)
        method = 'POST'
        headers={"Content-Type":"application/json"}
        ans = self.run(method, endpoint=URI, headers=headers)

        return ans

    def check_status_reload(self, taskId: str= "", id: str= ""):
        """
        
        Method used to check status of a task
        
        """
        
        URI = 'api/v1/tasks/{taskId}/executions/{id}'.format(taskId=taskId, id=id)

        method = 'GET'
        ans = self.run(method, URI)

        return ans

    def __get_cookies_session(self) -> requests.Session:
        """
        
        In NTLM Authentification for Qlik NPrinting, you have to use a GET request to obain cookies session. When you've got cookies session, you can use it to use POST, PUT, DELETE endpoint in QRS API. 
        This function is calling qrs/about in method GET to obtain the cookies session.    
    
        """

        session = self.get_conn_init()
        endpoint = 'api/v1/login/ntlm'

        if self.base_url and not self.base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
            url = self.base_url + '/' + endpoint
        else:
            url = (self.base_url or '') + (endpoint or '')

        req = requests.Request('GET', url)

        self.log.info("Sending GET about to url: %s to retrieve Qlik Session Cookie", url)

        prepped = session.prepare_request(req)
        try:
            response = session.send(prepped, verify=False)
            if response.status_code  == 200:
                self.__cookie_session = session.cookies.get_dict()['NPWEBCONSOLE_XSRF-TOKEN']
                return session
            else:
                raise ValueError('Error when trying to get qlik nprinting session cookies. Status Code returned {}'.format(response.status_code))

        except requests.exceptions.ConnectionError as ex:
            self.log.warning(
                '%s Tenacity will retry to execute the operation', ex)
            raise ex
        except:
            raise ValueError('Error when trying to get qlik nprinting session cookies.')

    def get_conn_init(self) -> requests.Session:
            """
            Returns http session to use with requests. Initialize a session without cookies X-Qlik-Session

            :param headers: additional headers to be passed through as a dictionary
            :type headers: dict
    
            """
            session = requests.Session()

            if self.conn_id:
                conn = self.get_connection(self.conn_id)

                host = conn.host if conn.host else ""
                host = host.strip('/')

                if not host.startswith('https://'):
                    host = 'https://'+host

                self.base_url = host + ':4993'
                
                #Ajout de l'authentification via NTLM    
                session.auth = HttpNtlmAuth(conn.login, conn.password)
                #AJout du user-agent
                session.headers.update({"User-Agent":"Windows"})

            return session
    
    def get_conn(self) -> requests.Session:
            """
            Returns http session to use with requests.

            :param headers: additional headers to be passed through as a dictionary
            :type headers: dict
    
            """

            session = self.__get_cookies_session()
            session.headers.update({'X-XSRF-TOKEN':self.__cookie_session})
            return session

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns NTLM Windows Connection Behaviour field"""
        
        return {
            "hidden_fields": ['port', 'schema'],  
            "relabeling": {
                'login':'Windows Account',
                'host':'Qlik NPrinting URI',

            },
            "placeholders": {
                'host': 'URI of Qlik Sense NPrinting',
                'login': "Domain\\Username",
            },
        }

    def run(
        self,
        method: str='GET',
        endpoint: Optional[str] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, Any]] = None,
        **request_kwargs: Any,
    ) -> Any:
        r"""
        Performs the request

        :param endpoint: the endpoint to be called i.e. resource/v1/query?
        :type endpoint: str
        :param data: payload to be uploaded or request parameters
        :type data: dict
        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """

        self.session = self.get_conn()

        if self.base_url and not self.base_url.endswith('/') and endpoint and not endpoint.startswith('/'):
            url = self.base_url + '/' + endpoint
        else:
            url = (self.base_url or '') + (endpoint or '')

        if method == 'GET':
            # GET uses params
            req = requests.Request(
                method, url, headers=headers)
        elif method=='POST':
            # Others use data
            import json
            req = requests.Request(
                method, url, data=json.dumps(data), headers=headers)
        else:
            raise RuntimeError('Method not handle by Qlik NPrinting Provider')

        self.log.info("Sending '%s' to url: %s", method, url)

        prepped = self.session.prepare_request(req)
        try:
            response = self.session.send(prepped, verify=False, allow_redirects=True)
            return response

        except requests.exceptions.ConnectionError as ex:
            self.log.warning(
                '%s Tenacity will retry to execute the operation', ex)
            raise ex