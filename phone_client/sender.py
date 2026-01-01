import subprocess
import socket
import json
import sys

TARGET_IP = "192.168.122.82"
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sensor_name = "LIS2DS Accelerometer"

cmd = ['termux-sensor', '-s', sensor_name, '-d', '20']

print(f"Targeting {TARGET_IP}...")
print("Reading sensor stream...")

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

json_buffer = ""
brace_count = 0

try:
    for line in process.stdout:
        json_buffer += line
        
        brace_count += line.count('{')
        brace_count -= line.count('}')
        
        if brace_count == 0 and json_buffer.strip():
            try:
                data = json.loads(json_buffer)
                
                if sensor_name in data:
                    values = data[sensor_name]["values"]
                    
                    payload = json.dumps({"v": values}).encode('utf-8')
                    sock.sendto(payload, (TARGET_IP, PORT))
            
            except json.JSONDecodeError:
                pass 
            
            json_buffer = ""
            
except KeyboardInterrupt:
    print("\nStopped.")
