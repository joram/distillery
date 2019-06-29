/lib/systemd/system/distillery.service
```
[Unit]
Description=Distillery
After=multi-user.target

[Service]
ExecStart=/bin/bash -c "/usr/bin/python3 /home/pi/code/distillery/server/server.py"
User=root
Restart=always

[Install]
WantedBy=multi-user.target
```

