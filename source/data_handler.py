import json

sport = int(input('''
Select a sport:
[1] - Basketball
[2] - Soccer
'''))
if sport == 1:
    try:
        with open('basketball.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
    except FileNotFoundError:
        player = input("Enter your name: ")
        db = {"player": player, "games": []}
    except Exception as e:
        print(f'ERROR: {e}')

elif sport == 2:
    try:
        with open('soccer.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
    except FileNotFoundError:
        player = input('Enter your name: ')
        db = {"player": player, "games": []}
    except Exception as e:
        print(f'ERROR: {e}')



def add_match():
    if sport == 1:
        new_game = {
            "name": input("Enter name for a match: "),
            "date": input("Enter date: "),
            "position": input('Enter position: '),
            "minutes": int(input('Enter on-court minutes: ')),
            "points": int(input("Enter points: ")),
            "assists": int(input("Enter assists: ")),
            "2pt_attempts": int(input('Enter 2-pointer throw attempts: ')),
            "3pt_attempts": int(input('Enter 3-pointer throw attempts: ')),
            "2ptshots_made": int(input('Enter 2-pointers made: ')),
            "3ptshots_made": int(input('Enter 3-pointers made: ')),
            "rebounds": int(input("Enter rebounds: ")),
            "blocks": int(input("Enter blocks: ")),
            "steals": int(input("Enter steals: ")),
            "personal_fouls": int(input("Enter personal fouls: ")),
            "missedFT": int(input("Enter missed free throws: ")),
            "turnovers": int(input("Enter turnovers: ")),
            "Won": bool(input("Result (True for W/False for L): "))
        }
    
    elif sport == 2:
        new_game = {
            "name": input("Enter name for a match: "),
            "date": input("Enter date: "),
            "position": input('Enter position: '),
            "minutes": int(input('Enter on-field minutes: ')),
            "goals": int(input('Enter goals: ')),
            "assists": int(input('Enter assists: ')),
            "shots": int(input('Enter shot attempts: ')),
            "shots_on_target": int(input('Enter shots on target: ')),
            "yellow_cards": int(input("Enter yellow cards: ")),
            "red_cards": int(input('Enter red cards: ')),
            "fouls": int(input('Enter fouls: ')),
            "Won": bool(input("Result (True for W/False for L): "))
        }
    
    db["games"].append(new_game)


def save():
    if sport == 1:
        with open('basketball.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    if sport == 2:
        with open('soccer.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
