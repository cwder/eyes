#!/bin/bash

cd /root/cwd/eyes/
nohup uvicorn app:app --host '0.0.0.0'--port 9999 --reload