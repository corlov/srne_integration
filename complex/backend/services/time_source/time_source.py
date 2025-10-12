#!/usr/bin/python3

import redis
import os
import datetime
import subprocess



def logmsg(message, level="INFO", log_file='time_source.log'): 
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level.upper()}]: {message}"    
    print(log_entry)    
    if log_file:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')



def check_chronyd_status():
    try:
        result = subprocess.run('systemctl is-active chronyd', check=True, shell=True, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip() == 'active'
    except subprocess.CalledProcessError:
        return False



def update_chrony_config(addr):
    logmsg(f'update_chrony_config({addr})')
    backup_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        subprocess.run(f'cp /etc/chrony/chrony.conf /etc/chrony/chrony.conf.backup_{backup_time}', check=True, shell=True)
        subprocess.run('systemctl stop chronyd', check=True, shell=True)
        subprocess.run(f"sed -i '1i\\server {addr} iburst prefer' /etc/chrony/chrony.conf", check=True, shell=True)
        subprocess.run('systemctl start chronyd', check=True, shell=True)
        
        # Проверка состояния chronyd
        if check_chronyd_status():
            logmsg('chronyd is active and running.')
        else:
            logmsg('chronyd failed to start.', level="ERROR")
        
        logmsg('update OK')
    except subprocess.CalledProcessError as e:
        logmsg(f'Error updating chrony config: {e}', level="ERROR")



def handle_message(message):
    addr = message['data'].decode('utf-8')
    if addr:
        update_chrony_config(addr)
    else:
        subprocess.run('systemctl stop chronyd', check=True, shell=True)
        logmsg('stop OK')



r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe('chrony_updates')

for message in p.listen():
    if message['type'] == 'message':
        handle_message(message)

