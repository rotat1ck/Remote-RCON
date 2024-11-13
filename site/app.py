from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import string

app = Flask(__name__)
app.secret_key = 'rcon9883_secret_session_key'  # For session management

# Dummy credentials (replace with proper authentication)
VALID_CREDENTIALS = {
    'admin': 'password123'
}

# In-memory storage for access codes (for demonstration purposes)
access_codes = {}

def generate_access_code(length=16):
    """Generate a random access code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if it's a JSON request (from AJAX)
        if request.is_json:
            data = request.json
            username = data.get('username')
            password = data.get('password')
        else:
            # Handle traditional form submission
            username = request.form.get('username')
            password = request.form.get('password')

        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            # Create a new access code for the user
            access_code = generate_access_code()
            access_codes[access_code] = username  # Store the access code with the associated username
            
            # For AJAX request, return JSON
            if request.is_json:
                return jsonify({
                    'access_code': access_code,
                    'username': username  # Include username in the response
                })
            
            # For traditional form submission, redirect
            return redirect(url_for('dashboard'))
        
        # For traditional form submission, you might want to add error handling
        return render_template('login.html', error='Invalid credentials')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = access_codes.get(request.cookies.get('access_code'), 'User')
    return render_template('dashboard.html', username=username)

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.json
    access_code = data.get('access_code')
    command = data.get('command', '')

    # Validate the access code
    username = access_codes.get(access_code)
    if not username:
        return jsonify({'msg': 'Invalid access code'}), 401

    try:
        # Be very careful with command execution
        print(f'Executing command: {command} for user: {username}')
        return jsonify({'output': f'Executed command: {command}'})
    except Exception as e:
        return jsonify({'output': str(e)})
    
@app.route('/get_players', methods=['POST'])
def get_players():
    access_code = request.json.get('access_code')
    
    # Validate access code (similar to execute route)
    username = access_codes.get(access_code)
    if not username:
        return jsonify({'msg': 'Invalid access code'}), 401

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
    access_code = request.json.get('access_code')
    if access_code in access_codes:
        del access_codes[access_code]
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Listen on all available network interfaces
        port=7777,       # Choose your desired port
        debug=True       # Set to False in production
    )