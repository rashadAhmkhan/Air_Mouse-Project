import socket
import json
import pyautogui


LISTEN_IP = "0.0.0.0"
PORT = 5555
SENSITIVITY = 50
DEADZONE = 0.5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, PORT))
sock.setblocking(False)  

print(f"Server listening on Port {PORT}...")
print("Anti-Lag System: ACTIVE")

pyautogui.FAILSAFE = False

try:
    while True:
        try:
            
            last_data = None
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    last_data = data
                except BlockingIOError:
                    
                    break
            
            
            if last_data is None:
                continue

            
            message = json.loads(last_data.decode('utf-8'))
            values = message['v']

            x_tilt = values[0]
            y_tilt = values[1]

            dx = 0
            dy = 0

            
            if abs(x_tilt) > DEADZONE:
                dx = int(x_tilt * SENSITIVITY * -1) 

            
            if abs(y_tilt) > DEADZONE:
                dy = int(y_tilt * SENSITIVITY)      

            if dx != 0 or dy != 0:
                pyautogui.moveRel(dx, dy)

        except json.JSONDecodeError:
            pass 
        except Exception as e:
            pass 

except KeyboardInterrupt:
    print("\nStopped.")
