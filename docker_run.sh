#!/bin/bash
docker run -it -v /var/log/syslog:/app/syslog syslog python /app/parser.py --path /app/syslog $@
