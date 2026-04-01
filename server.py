#!/usr/bin/env python3
import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import subprocess

ORDERS_FILE = '/var/www/html/digital-noodle-house/orders.txt'

def get_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r') as f:
            return len(f.read().strip().split('\n')) if f.read().strip() else 0
    return 0

def get_cpu():
    try:
        result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split('\n'):
            if '%Cpu' in line:
                return int(float(line.split(',')[0].split(':')[1].strip()))
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

def get_connections():
    try:
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=5)
        return str(len([l for l in result.stdout.split('\n') if ':80' in l and 'ESTABLISHED' in l]))
    except:
        return "0"

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
    protocol_version = 'HTTP/1.1'
    
    def do_GET(self):
        if self.path == '/api/stats' or self.path == '/stats':
            uptime = get_uptime()
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
            
            stats = {
                'cpu': get_cpu(),
                'memory': get_memory(),
                'load': get_load(),
                'connections': get_connections(),
                'hostname': get_hostname(),
                'orders': get_orders(),
                'uptime': int(uptime),
                'uptimeFormatted': f"{days}天{hours}小时"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
        elif self.path == '/' or self.path == '/dashboard.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(b'Redirect to dashboard')
        else:
            self.send_response(404)
            self.send_header('Connection', 'close')
            self.end_headers()
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Connection', 'close')
        self.end_headers()
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    port = 8888
    server = HTTPServer(('0.0.0.0', port), StatsHandler)
    print(f'Stats server running on port {port}')
    server.serve_forever()
