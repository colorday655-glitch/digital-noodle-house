#!/usr/bin/env python3
import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

ORDERS_FILE = '/var/www/html/digital-noodle-house/orders.txt'

def get_cpu():
    try:
        with open('/proc/stat', 'r') as f:
            line = f.readline()
            values = list(map(int, line.split()[1:]))
            idle = values[3]
            total = sum(values)
            return int((1 - idle / total) * 100)
    except:
        return 0

def get_memory():
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
            total = int(lines[0].split()[1])
            available = int(lines[2].split()[1])
            used = total - available
            return f"{int(used/total*100)}%"
    except:
        return "0%"

def get_load():
    try:
        with open('/proc/loadavg', 'r') as f:
            return f.read().split()[0]
    except:
        return "0.0"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            return float(f.read().split()[0])
    except:
        return 0

def get_hostname():
    try:
        with open('/etc/hostname', 'r') as f:
            return f.read().strip()
    except:
        return "unknown"

class StatsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/stats':
            uptime = get_uptime()
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
            
            # 统计订单数
            try:
                with open(ORDERS_FILE, 'r') as f:
                    orders = len([l for l in f.readlines() if l.strip()])
            except:
                orders = 0
            
            stats = {
                'cpu': get_cpu(),
                'memory': get_memory(),
                'load': get_load(),
                'hostname': get_hostname(),
                'orders': orders,
                'uptime': int(uptime),
                'uptimeFormatted': f"{days}天{hours}小时"
            }
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/order':
            try:
                with open(ORDERS_FILE, 'a') as f:
                    f.write(f"{int(time.time())}\n")
            except:
                pass
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    port = 8888
    server = HTTPServer(('0.0.0.0', port), StatsHandler)
    print(f'Stats server running on port {port}')
    server.serve_forever()