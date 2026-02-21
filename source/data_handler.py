import json

try:
    with open('data.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError:
    player = input("Enter your name: ")
    db = {"player": player, "games": []}


def add_match(name, date, points, assists, rebounds, blocks, steals, pf, missed, missedFT, TO, Result):
    new_game = {
        "name": str(name),
        "date": str(date),
        "points": int(points),
        "assists": int(assists),
        "rebounds": int(rebounds),
        "blocks": int(blocks),
        "steals": int(steals),
        "personal_fouls": int(pf),
        "missed": int(missed),
        "missedFT": int(missedFT),
        "turnovers": int(TO),
        "Won": bool(Result)
    }

    db["games"].append(new_game)


def save():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)
