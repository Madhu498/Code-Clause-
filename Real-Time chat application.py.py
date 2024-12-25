from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users
users = {}

@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Chat App</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.4/socket.io.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
                #chat { max-width: 600px; margin: 50px auto; background: white; border: 1px solid #ddd; border-radius: 5px; padding: 10px; }
                #messages { height: 300px; overflow-y: scroll; border-bottom: 1px solid #ddd; padding: 10px; }
                #messages div { margin-bottom: 10px; }
                #message-form { display: flex; }
                #message-form input { flex: 1; padding: 10px; }
                #message-form button { padding: 10px; background: #007BFF; color: Grey; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <div id="chat">
                <h3>Real-Time Chat</h3>
                <div id="messages"></div>
                <form id="message-form">
                    <input type="text" id="message-input" placeholder="Type your message..." autocomplete="on" />
                    <button type="submit">Send</button>
                </form>
            </div>

            <script>
                const socket = io();

                // Prompt user for username and room
                const username = prompt("Enter your username:");
                const room = prompt("Enter chat room name:");
                socket.emit('join_room', { username, room });

                // Listen for messages
                socket.on('message', (data) => {
                    console.log('Message received:', data);  // Debugging line
                    const messagesDiv = document.getElementById('messages');
                    const messageEl = document.createElement('div');
                    messageEl.innerHTML = `<strong>${data.username || 'Server'}:</strong> ${data.msg} <small>${data.time || ''}</small>`;
                    messagesDiv.appendChild(messageEl);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                });

                // Send messages
                const form = document.getElementById('message-form');
                form.addEventListener('submit', (e) => {
                    e.preventDefault();
                    const input = document.getElementById('message-input');
                    const msg = input.value;
                    socket.emit('message', { room, msg });
                    input.value = '';
                });
            </script>
        </body>
        </html>
    """)

# Handle user connection
@socketio.on('connect')
def handle_connect():
    print('A user connected.')

# Handle user disconnection
@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(request.sid, 'Unknown')
    print(f'{user} disconnected.')

# Handle joining a chat room
@socketio.on('join_room')
def handle_join(data):
    username = data['username']
    room = data['room']
    users[request.sid] = username
    join_room(room)
    # Broadcast the message to the room
    emit('message', {'msg': f'{username} has joined the room.'}, room=room, broadcast=True)

# Handle leaving a chat room
@socketio.on('leave_room')
def handle_leave(data):
    username = users.pop(request.sid, 'Unknown')
    room = data['room']
    leave_room(room)
    # Broadcast the message to the room
    emit('message', {'msg': f'{username} has left the room.'}, room=room, broadcast=True)

# Handle message sending
@socketio.on('message')
def handle_message(data):
    username = users.get(request.sid, 'Unknown')
    room = data['room']
    msg = data['msg']
    timestamp = datetime.now().strftime('%H:%M:%S')
    emit('message', {'username': username, 'msg': msg, 'time': timestamp}, room=room, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)  # Change port to 5001 or any available port
