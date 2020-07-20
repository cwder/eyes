#!/bin/bash

pip install icalendar smtplib
cd /root/www/huifu_interview_api/
nohup gunicorn -c gunicorn.conf -t 60 manage:app