import data_handler

db = data_handler
games = data_handler.db["games"]
sport = db.sport


def stats_review():
    if sport == 1:
        all_points = sum(game["points"] for game in games)
        all_minutes = sum(game["minutes"] for game in games)
        all_2pt = sum(game["2ptshots_made"] for game in games)
        all_3pt = sum(game["3ptshots_made"] for game in games)
        all_assists = sum(game["assists"] for game in games)
        all_rebounds = sum(game["rebounds"] for game in games)
        all_blocks = sum(game["blocks"] for game in games)
        all_steals = sum(game["steals"] for game in games)
        all_missed = ((sum(game["3pt_attempts"] for game in games) - all_3pt)) + (sum(game["2pt_attempts"] for game in games) - all_2pt)
        all_turnovers = sum(game["turnovers"] for game in games)
        all_missed_free_throws = sum(game["missedFT"] for game in games)
        all_games = len(games)
        efficiency = calculate_efficiency(all_points, all_rebounds, all_assists, all_steals, all_blocks, all_missed, all_turnovers, all_missed_free_throws)

        if all_games == 0:
            print("You have no saved games.")
            return 
    
        table = [["Points", all_points, round(all_points / all_games, 2)], ["Minutes", all_minutes, None],
                ["2 Pointers", all_2pt, None], ["3 Pointers", all_3pt, None],
                ["Assists", all_assists, round(all_assists / all_games, 2)], ["Rebounds", all_rebounds, round(all_rebounds / all_games, 2)], 
                ["Blocks", all_blocks, round(all_blocks / all_games, 2)], ["Steals", all_steals, round(all_steals / all_games, 2)], 
                ["Missed", all_missed, round(all_missed / all_games, 2)], ["Missed Free Throws", all_missed_free_throws, round(all_missed_free_throws / all_games, 2)]
                ]

        print(f"{'STAT':<20} {'ALL-TIME':<10} {'PER-GAME'}")
        print("─" * 40)
        for stat, ag, pg in table:
            print(f"{stat:<20} {ag:<10} {pg}")
        print("─" * 40)
        print(f"Games: {all_games}\nEfficiency: {efficiency}")
        print("─" * 40)
    
    elif sport == 2:
        all_minutes = sum(game["minutes"] for game in games)
        all_goals = sum(game["goals"] for game in games)
        all_assists = sum(game["assists"] for game in games)
        all_shots = sum(game["shots"] for game in games)
        all_shots_on_target = sum(game["shots"] for game in games)
        all_yellow_cards = sum(game["yellow_cards"] for game in games)
        all_red_cards = sum(game["red_cards"] for game in games)
        all_games = len(games)
        
        if all_games == 0:
            print('You have no saved games.')
            return
        
        table = [["Minutes", all_minutes, None], ["Goals", all_goals, round(all_goals / all_games, 2)],
                ["Assists", all_assists, round(all_assists / all_games, 2)], ["Shots", all_shots, round(all_shots / all_games, 2)],
                ["Shots on target", all_shots_on_target, round(all_shots_on_target / all_games, 2)], ["Yellow Cards", all_yellow_cards, round(all_yellow_cards / all_games, 2)],
                ["Red Cards", all_red_cards, round(all_red_cards / all_games, 2)]
                ]
        
        print(f"{'STAT':<20} {'ALL-TIME':<10} {'PER-GAME'}")
        print("─" * 40)
        for stat, ag, pg in table:
            print(f"{stat:<20} {ag:<10} {pg}")
        print("─" * 40)
        print(f"Games: {all_games}")
        print("─" * 40)


def calculate_efficiency(points, rebounds, assists, steals, blocks, missed, missedFT, turnovers):
    efficiency = (points + rebounds + assists + steals + blocks) - (missed + missedFT + turnovers)
    return efficiency


def show_stats(matchIndex):
    if sport == 1:
        table = [["Points", str(games[matchIndex]["points"])], ["Minutes", str(games[matchIndex]["minutes"])],
                ["2 Pointers", (f'{str(games[matchIndex]["2ptshots_made"])}/{str(games[matchIndex]["2pt_attempts"])}')], ["3 Pointers", (f'{str(games[matchIndex]["3ptshots_made"])}/{str(games[matchIndex]["3pt_attempts"])}')],
                ["Assists", str(games[matchIndex]["assists"])], ["Rebounds", str(games[matchIndex]["rebounds"])],
                ["Blocks", str(games[matchIndex]["blocks"])], ["Steals", str(games[matchIndex]["steals"])],
                ["Personal fouls", str(games[matchIndex]["personal_fouls"])], ["Missed Free Throws", str(games[matchIndex]["missedFT"])],
                ["Turnovers", str(games[matchIndex]["turnovers"])], ["Won", str(games[matchIndex]["Won"])]
                ]
        print(f"{'STAT':<20} {'VALUE'}")
        print("─" * 35)
        for stat, value in table:
            print(f"{stat:<20} {value}")
        print("─" * 35)

    if sport == 2:
        table = [["Minutes", str(games[matchIndex]["minutes"])], ["Goals", str(games[matchIndex]["goals"])],
                ["Assists", str(games[matchIndex]["assists"])], ["Shots", str(games[matchIndex]["shots"])],
                ["Shots on target", str(games[matchIndex]["shots_on_target"])], ["Yellow Cards", str(games[matchIndex]["yellow_cards"])],
                ["Red Cards", str(games[matchIndex]["red_cards"])], ["Won", str(games[matchIndex]["Won"])]
                ]
        print(f"{'STAT':<20} {'VALUE'}")
        print("─" * 35)
        for stat, value in table:
            print(f"{stat:<20} {value}")
        print("─" * 35)
