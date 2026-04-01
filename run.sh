#!/bin/bash
while true; do
    CPU=$(top -bn1 | grep Cpu | awk '{print $2}' | cut -d'%' -f1)
    MEM=$(free | grep Mem | awk '{printf "%d", $3/$2*100}')
    LOAD=$(cat /proc/loadavg | awk '{print $1}')
    UPTIME=$(cat /proc/uptime | awk '{print $1}')
    DAYS=$(echo "$UPTIME / 86400" | bc | cut -d. -f1)
    HOURS=$(echo "($UPTIME % 86400) / 3600" | bc | cut -d. -f1)
    JSON="{\"cpu\":$CPU,\"memory\":\"$MEM%\",\"load\":\"$LOAD\",\"hostname\":\"racknerd\",\"uptime\":$UPTIME,\"uptimeFormatted\":\"${DAYS}天${HOURS}小时\"}"
    echo "$JSON" > /var/www/html/digital-noodle-house/stats.json
    sleep 5
done