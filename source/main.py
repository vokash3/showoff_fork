import data_handler
import ui_handler
from ui_handler import Menu
import statistics_handler
import export_handler

db = data_handler
ui = ui_handler
stats = statistics_handler
games = data_handler.db["games"]
export = export_handler


def main():
    while True:
        Menu.show_info(False)
        user_choice = Menu.create_menu()

        if user_choice == 1:
            stats.add_match()
            print("Added!")
            db.save()
            input("Enter to continue... ")
            Menu.clear_screen()

        elif user_choice == 2:
            gamescount = len(games)
            for i in range(gamescount):
                print(f"{i + 1} - {str(games[i]['name'])}")
            choice = input("What game to show?(leave blank to exit)\n")
            if choice != '' and int(choice) - 1 in range(gamescount):
                stats.show_stats(int(choice) - 1)
            else:
                print("Game index out of range.")
            input("Enter to continue... ")
            Menu.clear_screen()

        elif user_choice == 3:
            stats.stats_review()
            input("Enter to continue... ")
            Menu.clear_screen()

        elif user_choice == 4:
            export.export_to_csv()
            Menu.clear_screen()

        elif user_choice == 5:
            Menu.clear_screen()
            Menu.show_info(True)
            input("Enter to continue... ")
            Menu.clear_screen()
        elif user_choice == 6:
            break


if __name__ == '__main__':
    main()
    db.save()
    exit()
