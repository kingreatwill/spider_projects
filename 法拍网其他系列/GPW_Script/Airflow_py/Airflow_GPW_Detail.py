import pytz
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "email": ["wangdong@iunispace.com"],
    "email_on_failure": True,
}
tz = pytz.timezone('Asia/Shanghai')
dt = datetime(2022, 11, 1, tzinfo=tz)
utc_dt = dt.astimezone(pytz.utc).replace(tzinfo=None)
# 00 01-23/1   01~23：00，每小时运行一次
with DAG(
        dag_id="Spider_GPW_Detail", catchup=False, default_args=default_args, tags=['spider'],
        start_date=utc_dt, max_active_runs=1, schedule_interval='00 01-23/1 * * *') as dag:
    SpiderBD = SSHOperator(ssh_conn_id="ssh.192.168.1.119.wangdong",
                           task_id="GPW_Detail",
                           command="cd /home/wangdong/fp_spider/GPW_Script/; /home/wangdong/anaconda3/envs/python3.9.5/bin/python -u Crawl_GPW_Detail.py",
                           dag=dag
                           )
