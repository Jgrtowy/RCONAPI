from flask import Flask, request, jsonify, redirect, url_for
from mctools import RCONClient
from flask_cors import CORS
from flask_limiter import Limiter


app = Flask(__name__)
limiter = Limiter(app)
CORS(app)

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/rcon', methods=['POST'])
@limiter.limit("100/minute")
def handle_rcon_command():
    ip = request.json['ip']
    port = request.json['port']
    password = request.json['password']
    command = request.json['command']

    rcon = RCONClient(ip, port)
    rcon.login(password)
    
    success = rcon.is_authenticated()
    
    if not success:
         return False;    
    rcon.start()
    response = rcon.command(command, frag_check=False)

    rcon.stop()

    return jsonify(response)

@app.route('/status', methods=['GET'])
def apiTest():
     return jsonify("🎉 API is working!")

if __name__ == '__main__':
    app.run(debug=True)