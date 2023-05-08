"""Setup.py for the Qlik Sense NPrinting Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-qlik-sense setup."""
setup(
    name='airflow-provider-qlik-sense-nprinting',
    version="0.0.1",
    description='Airflow package provider to perform action into Qlik Sense NPrinting (reload apps, tasks ...).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=airflow.providers.qlik_sense_nprinting.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['airflow.providers.qlik_sense_nprinting', 'airflow.providers.qlik_sense_nprinting.hooks', 
    'airflow.providers.qlik_sense_nprinting.operators',],
    install_requires=['apache-airflow>=2.0'],
    setup_requires=['setuptools', 'wheel'],
    author='Clement Parsy',
    author_email='cparsy@decideom.fr',
    url='',
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires='~=3.7',
)
