Markdown

# Python Air Mouse (UDP)

I wanted to control my laptop cursor using my phone's accelerometer without installing any sketchy third-party apps. This is a simple client-server setup using Python and sockets.

It reads the sensor data from an Android phone (via Termux) and sends it to a Windows PC over Wi-Fi.

## How it Works
1.  **Phone (Sender):** Uses `termux-sensor` to get accelerometer data. I wrote a custom Regex parser to handle the raw output because the JSON stream was messy and kept crashing standard parsers.
2.  **Network:** Sends data via **UDP** (User Datagram Protocol) because TCP was too slow for real-time movement.
3.  **PC (Receiver):** Listens for packets and moves the mouse using `pyautogui`.
4.  **Lag Fix:** I ran into a "buffer bloat" issue where the mouse would lag 2 seconds behind. I fixed this by making the receiver loop non-blocking—it dumps all old packets in the queue and only acts on the very last one received.

## Setup

### 1. On your Laptop (Receiver)
You just need Python and `pyautogui`.

```bash
pip install pyautogui
```
Then run the receiver script:

```bash

python receiver.py
```
Make sure your Firewall isn't blocking Python.

2. On your Phone (Sender)
You need the Termux app and the Termux:API add-on app (available on F-Droid or Play Store).

Open Termux and install the basics:

```bash

pkg install python termux-api
```
3. Connection
Find your Laptop's IP address (Run ipconfig on Windows).

Open sender.py on your phone and replace TARGET_IP with your laptop's IP.

Run it:

```bash

python sender.py
```
Known Issues / Tips
Permissions: If the phone script hangs, you might need to Force Stop the "Termux:API" app in Android settings to unstick the sensor.

Orientation: The code assumes you are holding the phone in Portrait mode. If the mouse moves backwards, just flip the * -1 in the receiver.py math.

Network: Works best on a 5GHz Wi-Fi or a Mobile Hotspot.

Files
receiver.py - Runs on PC. Handles the socket buffer and mouse movement.

sender.py - Runs on Phone. Reads hardware sensors and blasts UDP packets.
NOTE : The project is purely coded and handled by Gemini Pro.I am adding this to make sure nobody gets a false expectation or a sudden emergency of being able to do all this on their own (even though its not a very big-of-a-deal).My sole role was to identify factors of error and identifying anomalies.

