import os
import datetime

def update_chrony_config(addr):
    backup_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.system(f'cp /etc/chrony/chrony.conf /etc/chrony/chrony.conf.backup_{backup_time}')
    stop_daemon('chronyd')
    os.system("sed -i '1i\server " + addr + " iburst prefer' /etc/chrony/chrony.conf")
    start_daemon('chronyd')



def stop_daemon(daemon_name):
    os.system(f'systemctl stop {daemon_name}')



def start_daemon(daemon_name):
    os.system(f'systemctl start {daemon_name}')


