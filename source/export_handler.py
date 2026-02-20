import csv
import json

def export_to_csv(filename='export.csv'):
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File data.json not found.")
        return
    
    games = data['games']
    if not games:
        print('No games to export')
        return
    
    headers = ['date', 'points', 'assists', 'rebounds', 'blocks', 'steals', 'missed', 'missedFT', 'turnovers']

    with open(filename, 'w', newline='', encoding='utf-8') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=headers)
        writer.writeheader()
        for game in games:
            row = {key: game.get(key, '') for key in headers}
            writer.writerow(row)

    print(f'Export finished in file {filename}')
    input('Enter to continue...')