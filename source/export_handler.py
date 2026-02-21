import csv
import json

def export_to_csv(sport, filename='export.csv'):
    if sport == 1:
        try:
            with open('basketball.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File basketball.json not found.")
            input('Enter to continue...')
            return
        except Exception as e:
            print(f'ERROR: {e}')
            input('Enter to continue...')
            return
        
        games = data['games']
        if not games:
            print('No games to export')
            return
    
        headers = ['Date', 'POS', 'MIN', 'PTS', 'AST', '2PTA', '2PTM', '3PTA', '3PTM', 'REB', 'BLK', 'STL', 'PF', 'Missed Free Throws', 'Turnovers', 'WIN']

        key_mapping = {
        'Date': 'date',
        'POS': 'position',
        'MIN': 'minutes',
        'PTS': 'points',
        'AST': 'assists',
        '2PTA': '2pt_attempts',
        '2PTM': '2ptshots_made',
        '3PTA': '3pt_attempts',
        '3PTM': '3ptshots_made',
        'REB': 'rebounds',
        'BLK': 'blocks',
        'STL': 'steals',
        'PF': 'personal_fouls',
        'Missed Free Throws': 'missedFT',
        'Turnovers': 'turnovers',
        'WIN': 'Won'
        }

        with open(filename, 'w', newline='', encoding='utf-8') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=headers)
            writer.writeheader()
            for game in games:
                row = {csv_key: game.get(json_key, '') for csv_key, json_key in key_mapping.items()}
                writer.writerow(row)

    if sport == 2:
        try:
            with open('soccer.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File soccer.json not found.")
            input('Enter to continue...')
            return
        except Exception as e:
            print(f'ERROR: {e}')
            input('Enter to continue...')
            return
        
        games = data['games']
        if not games:
            print('No games to export')
            return
    
        headers = ['Date', 'POS', 'MIN', 'GOALS', 'AST', 'SHOTS', 'SHOTS MADE', 'Yellow cards', 'Red cards', 'Fouls', 'WIN']

        key_mapping = {
        'Date': 'date',
        'POS': 'position',
        'MIN': 'minutes',
        'GOALS': 'goals',
        'AST': 'assists',
        'SHOTS': 'shots',
        'SHOTS MADE': 'shots_on_target',
        'Yellow cards': 'yellow_cards',
        'Red cards': 'red_cards',
        'Fouls': 'fouls',
        'WIN': 'Won'
        }

        with open(filename, 'w', newline='', encoding='utf-8') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=headers)
            writer.writeheader()
            for game in games:
                row = {csv_key: game.get(json_key, '') for csv_key, json_key in key_mapping.items()}
                writer.writerow(row)

    
    print(f'Export finished in file {filename}')
    input('Enter to continue...')