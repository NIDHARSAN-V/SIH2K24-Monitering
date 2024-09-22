from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/emit', methods=['POST'])
def emit_message():
    event = request.json.get('event')
    data = request.json.get('data')
   
    if event == 'question':
        # Emit the question to all connected WebSocket clients
        socketio.emit('question', data)
   
    return {'status': 'Message emitted'}

@socketio.on('answer')
def handle_answer(answer):
    # Forward the answer to the normal Flask server
    response = requests.post('http://normal-server-url/receive_answer', json={'answer': answer})
   
    return {'status': 'Answer sent to normal server'}
#main function
if __name__ == '__main__':
    socketio.run(app, port=6000)
