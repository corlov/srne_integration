
Поскольку данный сервис работает непосредственно с сетевыми интерфейсами хостовой машины то разворачивать его как докер-контейнер нельзя.


nano /etc/systemd/system/wifi_hotspot.service
"""
[Unit]
Description=Wifi on/off hotspot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/solar/services/wifi_hotspot_service/wifi_hotspot.py
WorkingDirectory=/root/solar/services/wifi_hotspot_service      
StandardOutput=journal
StandardError=journal
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""

systemctl daemon-reload
systemctl restart wifi_hotspot.service 
systemctl enable wifi_hotspot.service 
systemctl status wifi_hotspot.service
journalctl -u wifi_hotspot.service 
 


https://repka-pi.ru/blog/post/108

Что я делал на Репке:
apt-get install network-manager dnsmasq
при запуске оказалось что "dnsmasq" конфликутует на 53 порту с "systemd-resolved"

sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved


netstat -tulpn | grep ':53'


mv /etc/resolv.conf /etc/resolv.conf_systemd-resolve_edition
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

systemctl start dnsmasq
systemctl status dnsmasq


nmcli con add type wifi ifname wlan0 con-name Hotspot autoconnect no \
    ssid RepkaPi-AP \
    802-11-wireless.mode ap \
    802-11-wireless.band bg \
    ipv4.method shared \
    ipv4.addresses 192.168.4.1/24 \
    wifi-sec.key-mgmt wpa-psk \
    wifi-sec.psk "12345678"


Вот основные команды:

006  systemctl daemon-reload
 1007  systemctl enable wifi-checker
 1008  systemctl start wifi-checker
 1009  nmcli dev set wlan0 managed yes
 1010  reboot
 1011  nmcli radio wifi
 1012  nmcli radio wifi on
 1013  nmcli radio wifi
 1014  nmcli device
 1015  ip a s
 1016  journalctl -u wifi-checker -f
 1017  nmcli con up Hotspot
 1018  ip a s
 1019  nmcli device
 1020  nmcli radio wifi
 1021  nmcli con up Hotspot
 1022  history
 1023  nmcli con show
 1024  nmcli con down irz
 1025  nmcli con up Hotspot
 1026  nmcli con show
 1027  ip a s
 1028  history





Реализация:

nmcli con show:
NAME             UUID                                  TYPE      DEVICE 
Ifupdown (eth0)  681b428f-beaf-8932-dce4-687ed5bae28e  ethernet  eth0   
irz              cbbdd257-de8c-4cf1-85df-eb55ae27405f  wifi      wlan0  
Hotspot          59e55d2a-9668-4c81-a528-29b31408b93f  wifi      --     
KostyaAP         155cdc43-087e-48cc-bf89-106b8a626f83  wifi      --   
Тушим командой "nmcli con down irz" все остальные сети (если такие вообще есть) с TYPE=wifi и название которых не наше (NAME != Hotspot)

Затем активируем хотспот на 60 минут  nmcli con up Hotspot и активируем таймер с оратным отсчетом после которого  nmcli con down Hotspot





1) отключить сервсис проеверки соединения - иначе отрубает сеть нахер. и отключить wifi потом
Потом руками сделать чтобы вафля падала и подымалась. и смотреть статус в GUI)


Вот так проверить Wifi


ip -4 addr show wlan0
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 192.168.1.163/24 brd 192.168.1.255 scope global dynamic noprefixroute wlan0
       valid_lft 43013sec preferred_lft 43013sec












