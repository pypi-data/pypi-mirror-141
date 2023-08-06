#!/bin/bash

#sudo kill -9 `sudo lsof -t -i:5860`
#cd /home/www/xiaoniu_cron
#source env/bin/activate

#gunicorn -c gun.py manage:app 
nohup gunicorn -c gun.py manage:app  >>/notechats/logs/notecorn/server-$(date +%Y-%m-%d).log 2>&1 &