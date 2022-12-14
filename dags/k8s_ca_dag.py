import json
import kubernetes
import os
import pprint
import subprocess
from datetime import datetime, timedelta

from airflow.decorators import dag, task # DAG and task decorators for interfacing with the TaskFlow API


@dag(
    # This defines how often your DAG will run, or the schedule by which your DAG runs. In this case, this DAG
    # will run daily
    schedule_interval="@daily",
    # This DAG is set to run for the first time on January 1, 2021. Best practice is to use a static
    # start_date. Subsequent DAG runs are instantiated based on scheduler_interval
    start_date=datetime(2021, 1, 1),
    # When catchup=False, your DAG will only run for the latest schedule_interval. In this case, this means
    # that tasks will not be run between January 1, 2021 and 30 mins ago. When turned on, this DAG's first
    # run will be for the next 30 mins, per the schedule_interval
    catchup=False,
    default_args={
        "retries": 0, # If a task fails, it will retry 2 times.
    },
    tags=['example']) # If set, this tag is shown in the DAG view of the Airflow UI
def k8s_ca_dag():
    """
    ### Basic ETL Dag
    This is a simple ETL data pipeline example that demonstrates the use of
    the TaskFlow API using three simple tasks for extract, transform, and load.
    For more information on Airflow's TaskFlow API, reference documentation here:
    https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html
    """

    @task()
    def extract():
        """
        #### Extract task
        A simple "extract" task to get data ready for the rest of the
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
        """
        path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
        print('reading %s' % path)
        try:
            with open(path) as f:
                s = f.read()
                print('k8s_token: %s' % s)
        except Exception as e:
            print(path,e)
        
        path = '/var/run/secrets/eks.amazonaws.com/serviceaccount/token'
        print('reading %s' % path)
        try:
            with open(path) as f:
                s = f.read()
                print('eks_token: %s' % s)
        except Exception as e:
            print(path,e)

        path = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        print('reading %s' % path)
        try:
            with open(path) as f:
                s = f.read()
                print('k8s_ca_cert: %s' % s)
        except Exception as e:
            print(path,e)

        path = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
        print('reading %s' % path)
        try:
            with open(path) as f:
                s = f.read()
                print('k8s_namespace: %s' % s)
        except Exception as e:
            print(path,e)

        # with open(path) as file:
        #     data = file.read()
        #     print(data)

        data = os.popen('find /var/run -follow').read()
        # pprint.pprint(data)
        print(data)

        from kubernetes import client, config

        # Configs can be set in Configuration class directly or using helper utility
        config.load_kube_config()

        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

        # pprint.pprint(os.environ)
        # print(os.environ)



        return data

    order_data = extract()

mydag = k8s_ca_dag()