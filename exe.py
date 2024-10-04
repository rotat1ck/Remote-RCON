from rcon.source import Client

def get_list_of_players():
    with Client('77.37.246.6', 2589, passwd='zalupa1488') as client:
        response = client.run('list')
        
    prefix, player_names = response.split(':')
    player_names = player_names.strip()
    player_names = player_names.split(', ')
    words = prefix.split()
    numbers = [word for word in words if word.isdigit()]
    print(f"     {numbers[0]}/{numbers[1]}")
    for i in player_names:
        print(i)
get_list_of_players()