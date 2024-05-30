from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
file_path = os.path.join('volume', 'log','cowrie', 'cowrie.json')

def load_log_data():
    log_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line.strip())
                    log_data.append(data)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"Il file {file_path} non è stato trovato.")
    return log_data.reverse()

def load_log_data_filtered(session_id):
    log_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line.strip())
                    if(data["session"] == session_id or session_id == ''):
                        log_data.append(data)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"Il file {file_path} non è stato trovato.")
    return log_data

def sanitize_log_data(json_data):
    for x in json_data:
        x["timestamp"] = x["timestamp"].split("T")[0] +" "+ x["timestamp"].split("T")[1].split(".")[0]
        


@app.route('/')
def index():
    log_data = load_log_data()
    sanitize_log_data(log_data) 
    return render_template('index.html', log_data=log_data)

@app.route('/filter')
def filter_logs():
    session_number = request.args.get('session')
    print(session_number)
    log_data = load_log_data_filtered(session_number)
    sanitize_log_data(log_data) 
    return jsonify(log_data)

if __name__ == '__main__':
    app.run(debug=True)
