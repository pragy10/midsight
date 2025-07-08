import json
import time
import re

class log_monitor:

    def extract_ip(self, message):
        IP = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        match = IP.search(message)
        return match if match else None
    

