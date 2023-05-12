<p align="center" style="vertical-align:center;">
  <a href="https://www.qlik.com/us/products/qlik-sense">
    <img alt="Qlik Sense Client Managed" src="https://mace-solutions.fr/wp-content/uploads/2022/02/qlik-square.png" width="80", height="80" />
  </a>
</p>

<h1 align="center">
  Airflow: Qlik Sense NPrinitng Provider
</h1>
  <h3 align="center">
    Qlik Sense NPrinting Provider to reload application, tasks from Airflow.
</h3>

<br/>

This repository provides basic Qlik NPrinting hooks and operators to trigger reloads of tasks available in a Qlik Sense NPrinting Site.

## Requirements

The package has been tested with Python 3.7, Python 3.8.

|  Package  |  Version  |
|-----------|---------------|
| apache-airflow | >2.0 |
| requests_ntlm2 | >=2 6.5.2 |

## How to install it ?


To install it, download and unzip source and launch the following pip install command: 

```bash
pip install .
```

You can also use 

```bash
python setup.py install
```

## How to use it ?
<br/>

On this provider, you can use three way to let Airflow connecting to your Qlik Sense NPrinting Site.

• NTLM Authentification: Authentification with a username and password used in Qlik in everyday life. Warning: Airflow will have the same rights of the user you provide.
• JWT Authentification: Authentification with a jwt token that you provide to Airflow. Warning: A JWT virtual proxy will have to be create on your Qlik Sense Site. To do this you can following the step of the section Appendix: How to create a JWT Virtual Proxy in Qlik or this article from Qlik Community: https://community.qlik.com/t5/Official-Support-Articles/Qlik-Sense-How-to-set-up-JWT-authentication/ta-p/1716226
• Certificates Authentification: Authentification with Certificates. Warning: In this case, you'll have to take client certificate generated by your Qlik Sense site during installation. The port **4242** MUST be open on your Qlik Sense Site from Airflow Server. With this type of authentifcation, Airflow will use sa_api user to trigger tasks, or application reloading.
<br/>

### 1. NTLM Authentification Example
<br/>

**Prerequisites**:  
<br>
• A login account with password
• URI of your Qlik Sense NPrinting Site 

**Step 1**: Login in your Airflow Server. 

**Step 2**: Go into Admin > Connections > Add A New Record. 

**Step 3**: Select [NTLM] Qlik Sense NPrinting.

**Step 4** Provide following informations:
    
           • Connection Id of your choice
           • Qlik Sense NPrinting URL without any port
           • Qlik Username (example: DOMAIN\\USERNAME)
           • Qlik Password of the account used

Be careful this Qlik NPrinting Account must have privilieges to trigger the task.

**Step 5** Save and your connection to Qlik Client NPrinting using NTLM auth is ready to use !

### 2. JWT Authentification Example
<br/>

**Prerequisites**:  
<br>
• A JWT token of the user that you want to trigger action with
• URL of your Qlik Sense Site (with the virtual proxy using JWT auth). If you don't have any JWT virtual proxy on your Qlik Sense Site, please follow: https://community.qlik.com/t5/Official-Support-Articles/Qlik-Sense-How-to-set-up-JWT-authentication/ta-p/1716226

**Step 1**: Login in your Airflow Server. 

**Step 2**: Go into Admin > Connections > Add A New Record. 

**Step 3**: Select [JWT] Qlik Sense Client Managed.

**Step 4** Provide following informations:
    
           • Connection Id of your choise
           • Qlik Sense Url using the JWT Virtual Proxy
           • Qlik JWT Token

**Step 5** Save and your connection to Qlik Client Managed using NTLM auth is ready to use !

### 3. Certificate Authentifcation Example
<br/>
Builing the section. No available yet.




### 4. Example: Creating a DAG with Qlik Sense NPrinting to reload tasks 

You can now use the operators in your dags to trigger a reload of an app in Qlik Sense from Airflow

Example: 

```python

from airflow.providers.qlik_sense_nprinting.operators.reload_task_operator import QlikNPrintingReloadTaskOperator
from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    'QlikSenseTriggerTaskExample',
    default_args=default_args,
    description='A simple tutorial DAG reloading Qlik Sense NPrinting Task',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['QlikNPrinting', 'Example'],
) as dag:
    
    nprintingTask = QlikNPrintingReloadTaskOperator(taskId="uiidofyournprintingtask", conn_id="hookNPrintingHook", task_id="MyHelloWorldNPrintingTask", waitUntilFinished=True)
    
    nprintingTask

```

<br/>


