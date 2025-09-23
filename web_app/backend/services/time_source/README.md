
Работа с источником времени на МАШИНЕ
Под Кубером это не запускаем т.к. важно время не внутри лкастера кубера а на машине!


nano /etc/systemd/system/time_source.service
"""
[Unit]
Description=Time source service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/solar/services/time_source/time_source.py
WorkingDirectory=/root/solar/services/time_source
StandardOutput=journal
StandardError=journal
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""

systemctl daemon-reload
systemctl restart time_source.service
systemctl enable time_source.service
systemctl status time_source.service
journalctl -u time_source.service 
 