#!/bin/bash
apt-get install -y systemd
pip3 install -r requirements.txt
echo "[Unit]
Description=Detective Iconan

[Service]
ExecStart=/usr/bin/bash /path/to/faviconfinder.py -u <URL>-s wildcard -mail yes

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/iconan.service

echo "[Unit]
Description=Schedule a message every 1 hour

[Timer]
#Execute job if it missed a run due to machine being off
Persistent=true
#Run 120 seconds after boot for the first time
OnBootSec=120
#Run every 1 hour thereafter
OnUnitActiveSec=1h
#File describing job to execute
Unit=iconan.service
[Install]
WantedBy=timers.target" > /etc/systemd/system/iconan.timer


systemctl daemon-reload

systemctl enable iconan.service
systemctl enable iconan.timer

systemctl start iconan.service
systemctl start iconan.timer

systemctl status iconan.service
systemctl status iconan.timer