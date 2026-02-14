import data_handler
import ui_handler
from ui_handler import menu
import statistics_handler

VERSION = 1
db = data_handler
ui = ui_handler
stats = statistics_handler


def main():

    while True:
        menu.showInfo(VERSION, False)
        user_choice = menu.createMenu()

        if user_choice == 1:
            stats.addMatch()
            print("Added!")
            db.save()
            input()
            menu.clearScreen()

        elif user_choice == 2:
            stats.statsReview()
            input()
            menu.clearScreen()

        elif user_choice == 4:
            '''
            menu.clearScreen()
            print("Coach mode is a mode that helps to track statistics of all your players")
            if input("Enable? (Y/N)") == "Y":
                data_handler.enableCoachMode()
                print("Enabled!")
            else:
                pass
            '''
            print("Coach mode is currently under work. Stay tuned for updates")
            input()
            menu.clearScreen()
            pass

        elif user_choice == 5:
            menu.clearScreen()
            menu.showInfo(VERSION, True)
            input()
            menu.clearScreen()
        elif user_choice == 6:
            break

main()
db.save()
exit()