from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random, string, requests, json


app = Flask(__name__)


@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if it's a JSON request (from AJAX)
        if request.is_json:
            data = request.json
            print(data)
            hash_value = data.get('hash')
            username = data.get('username')

    data = {"hash": hash_value}
    response = requests.post("http://localhost:8000/checkhash", json=data)

    if response.status_code == 200:
        try:
            data = response.json()
            userid = data.get("id")
            oplvl = data.get("oplvl")
            accesscode = data.get("code")
            print(f"Подключился пользователь: {userid} \nУровень доступа: {oplvl}\nКод: {accesscode}")
            if request.is_json:
                return jsonify({
                    'access_code': accesscode,
                    'username': username 
                })
            
            return redirect(url_for('dashboard'))
        except json.JSONDecodeError:
            print("Invalid JSON response:", response.text)
    else:
        print("Error:", response.status_code)
        # For traditional form submission, you might want to add error handling
        return render_template('login.html', error='Invalid credentials')
            

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    jsondata = request.json
    accesscode = jsondata.get('access_code')
    command = jsondata.get('command', '')

    data = {"code": accesscode}
    response = requests.post("http://localhost:8000/main", json=data)
    if response.status_code == 200:
        try:
            data = response.json()
            userid = data.get("id")
            oplvl = data.get("oplvl")
            code = data.get("accesscode")
            # выполнение rcon команды
            import rconexec
            try:
                dataToSend = rconexec.check(command, oplvl)
            except TimeoutError:
                dataToSend = 'Server is down. Use /start'
            print(f"Пользователь {userid} | Выполнил команду {command}")
            return jsonify({'output': f'{dataToSend}'})
        except json.JSONDecodeError:
            print("Invalid JSON response:", response.text)
    else:
        print("Error:", response.status_code)
    
    
@app.route('/get_players', methods=['POST'])
def get_players():
    accesscode = request.json.get('access_code')
    data = {"code": accesscode}
    response = requests.post("http://localhost:8000/main", json=data)
    
    if response.status_code == 200:
        

        try:
            # Simulate getting player list (replace with actual RCON command)
            # This is a mock response - replace with actual RCON command execution
            from rconexec import get_list_of_players
            try:
                players_response = get_list_of_players()
            except TimeoutError:
                return jsonify({'output': 'Server is down. Use /start'})
            
            if ':' in players_response:
                prefix, player_names = players_response.split(':')
                player_names = player_names.strip()
                player_names = player_names.split(', ')
                
                # Extract player count
                words = prefix.split()
                numbers = [word for word in words if word.isdigit()]
                
                return jsonify({
                    'total_players': numbers[0],
                    'max_players': numbers[1],
                    'players': player_names
                })
            
            return jsonify({'players': []})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the access code
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(
        host='localhost',  # Listen on all available network interfaces
        port=7777,       # Choose your desired port
        debug=True       # Set to False in production
    )