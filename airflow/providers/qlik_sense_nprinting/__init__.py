## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "airflow-provider-qlik-sense-nprinting", # Required
        "name": "Qlik Sense NPrinting Airflow Provider", # Required
        "description": 'Airflow package provider to perform actions on Qlik Sense NPrinting Server.', # Required
        "hook": [
            {
                "integration-name": "Qlik Sense NPrinting",
                "python-modules": [ "airflow.providers.qlik_sense_nprinting.hooks.qlik_nprinting_hook_ntlm.QlikNPrintingHookNTLM",]
            }
            ],
        "operators":[
                        {
                            "integration-name": "Qlik NPrinting Task Operator",
                            "python-modules":"airflow.providers.qlik_sense_nprinting.operators.reload_task_operator.QlikNPrintingReloadTaskOperator"
                        }, 

        ],
        'connection-types': [
            {
                'hook-class-name': 'airflow.providers.qlik_sense_nprinting.hooks.qlik_nprinting_hook_ntlm.QlikNPrintingHookNTLM',
                'connection-type': 'qlik_sense_nprinting',
            },
        ],
        #"extra-links": ["qlik_sense_cloud.operators.sample_operator.ExtraLink"],
        "versions": ["0.0.1"] # Required
    }