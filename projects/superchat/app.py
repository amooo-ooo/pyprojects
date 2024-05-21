from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

USERS = {}
USER_REF = {}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    data = request.form.to_dict()
    username, password = data.values()

    if username in USER_REF:
        if USERS.get(USER_REF[username], None)["password"] != password:
            return render_template("index.html", error="Incorrect password!")
        uid = USER_REF[username]
    else:
        uid = uuid.uuid4().hex
        USER_REF[username] = uid
        USERS[uid] = {"username": username, "password": password}
    return render_template('chat.html', uid=uid, username=username)

@socketio.on('joined')
def joined(message):
    user = USERS.get(message['uid'], False)
    if user:
        emit('message', {'username': 'Server', 
                         'text': f"@{user['username']} entered the party!", 
                         'mode': 'server'},
             broadcast=True)

@socketio.on('message')
def handle_message(message):
    user = USERS.get(message['uid'], False)
    if user:
        emit('message', { 'username': user['username'], 'text': message['text'], 'mode': 'public'},
            broadcast=True)
    
if __name__ == "__main__":
    app.run()
