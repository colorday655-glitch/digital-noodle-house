#!/bin/bash
ORDERS_FILE="/var/www/html/digital-noodle-house/orders.txt"
STATS_FILE="/var/www/html/digital-noodle-house/stats.json"

while true; do
    CPU=$(top -bn1 | grep Cpu | awk '{print $2}' | cut -d'%' -f1)
    MEM=$(free | grep Mem | awk '{printf "%d", $3/$2*100}')
    LOAD=$(cat /proc/loadavg | awk '{print $1}')
    UPTIME=$(cat /proc/uptime | awk '{print $1}')
    DAYS=$(echo "$UPTIME / 86400" | bc | cut -d. -f1)
    HOURS=$(echo "($UPTIME % 86400) / 3600" | bc | cut -d. -f1)
    
    # 统计订单数
    if [ -f "$ORDERS_FILE" ]; then
        ORDERS=$(wc -l < "$ORDERS_FILE")
    else
        ORDERS=0
    fi
    
    JSON="{\"cpu\":$CPU,\"memory\":\"$MEM%\",\"load\":\"$LOAD\",\"hostname\":\"racknerd\",\"orders\":$ORDERS,\"uptime\":$UPTIME,\"uptimeFormatted\":\"${DAYS}天${HOURS}小时\"}"
    echo "$JSON" > "$STATS_FILE"
    sleep 5
done