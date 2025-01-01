from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests, json


app = Flask(__name__)

@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # получения хэша и имени пользователя
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            print(data)
            hash_value = data.get('hash')
            username = data.get('username')

    data = {"hash": hash_value}
    # отправка в api
    response = requests.post("http://localhost:8000/checkhash", json=data)

    if response.status_code == 200:
        try:
            data = response.json()
            userid = data.get("id")
            oplvl = data.get("oplvl")
            accesscode = data.get("code")
            # лог подключения
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
        return jsonify({"success": False}), 403

            

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    # получение временного кода и команды от пользователя
    jsondata = request.json
    accesscode = jsondata.get('access_code')
    command = jsondata.get('command', '')

    data = {"code": accesscode}
    # отправка в api
    response = requests.post("http://localhost:8000/main", json=data)
    if response.status_code == 200:
        try:
            data = response.json()
            userid = data.get("id")
            oplvl = data.get("oplvl")
            # выполнение rcon команды
            import rconexec
            try:
                dataToSend = rconexec.check(command, oplvl)
            except TimeoutError:
                dataToSend = 'Server is down. Use /start'
            
            # лог исполняемых команд
            print(f"Пользователь {userid} | Выполнил команду {command}")
            
            return jsonify({'output': f'{dataToSend}'})
        except json.JSONDecodeError:
            print("Invalid JSON response:", response.text)
    else:
        print("Error:", response.status_code)
    
    
@app.route('/get_players', methods=['POST'])
def get_players():
    # получение временного кода
    accesscode = request.json.get('access_code')
    data = {"code": accesscode}
    # отправка в api
    response = requests.post("http://localhost:8000/main", json=data)
    
    if response.status_code == 200:
        try:
            # исполнение rcon команды - list
            from rconexec import get_list_of_players
            try:
                players_response = get_list_of_players()
            except TimeoutError:
                return jsonify({'output': 'Server is down. Use /start'})
            
            if ':' in players_response:
                # разделение на префикс (кол-во игроков) и список игроков
                prefix, player_names = players_response.split(':')
                player_names = player_names.strip()
                player_names = player_names.split(', ')
                
                # разделение префикса на кол-во игроков и максимальное кол-во игроков
                words = prefix.split()
                numbers = [word for word in words if word.isdigit()]
                
                # отправка результата
                return jsonify({
                    'total_players': numbers[0],
                    'max_players': numbers[1],
                    'players': player_names
                })
            
            # соединение с сервером не установлено
            # назначает "0:0" в меню игроков 
            return jsonify({'players': []})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Failed to fetch players, status code: {}'.format(response.status_code)}), response.status_code


@app.route('/logout', methods=['POST'])
def logout():
    
    return jsonify({'success': True})

# запуск приложения
if __name__ == '__main__':
    app.run(
        host='0.0.0.0', # оставьте '0.0.0.0' или выберите нужный вам интерфейс
        port=7777, # измените на нужный вам порт
        debug=False
    )