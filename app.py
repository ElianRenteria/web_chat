from flask import Flask, request, jsonify, send_from_directory
from flask_sock import Sock
import sqlite3

app = Flask(__name__, static_folder='.')
sock = Sock(app)

def get_chat_history():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT message FROM messages')
    messages = c.fetchall()
    conn.close()
    return [message[0] for message in messages]

@app.route('/chat-history')
def chat_history():
    return jsonify(get_chat_history())

@sock.route('/ws')
def chat(ws):
    while True:
        message = ws.receive()
        if message:
            conn = sqlite3.connect('chat.db')
            c = conn.cursor()
            c.execute('INSERT INTO messages (message) VALUES (?)', (message,))
            conn.commit()
            conn.close()
            ws.send(message)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)