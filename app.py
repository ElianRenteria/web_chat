from flask import Flask, jsonify, send_from_directory
from flask_sock import Sock
import sqlite3
'''from pyngrok import ngrok
from dotenv import load_dotenv
import os'''

app = Flask(__name__)
sock = Sock(app)

clients = []

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
    clients.append(ws)
    try:
        while True:
            message = ws.receive()
            if message:
                conn = sqlite3.connect('chat.db')
                c = conn.cursor()
                c.execute('INSERT INTO messages (message) VALUES (?)', (message,))
                conn.commit()
                conn.close()
                for client in clients:
                    client.send(message)
    finally:
        clients.remove(ws)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    # Load environment variables from .env file
    '''load_dotenv()
    # Set your ngrok auth token (if needed)
    ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))

    # Open a ngrok tunnel to the local server on port 8000
    public_url = ngrok.connect(8000)

    print(f"Public URL: {public_url}")'''
    # Run your Flask application
    app.run(debug=True, host='localhost', port=8000)
