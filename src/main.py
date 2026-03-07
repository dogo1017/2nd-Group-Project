# MAIN FUNCTION
from log_in import *
from dino_game import *
from high_score_tracker import *
from user_registration import *


def main():
    while True:
        information = load_csv()
        print("Welcome to the High Score Tracker!")
        print("1. Log in")
        print("2. Create an Account")  
        print("3. Quit")      
        user_choice = input("What would you like to do?")
        if user_choice == '1':
            information,text =log_in(information)
            if text == "exit":
                pass
            else:
                for i in information:
                    if i["status"] == 'active':
                        if i["username"] == "admin":
                            while True:
                                #View leaderboared, go back to main, play, view/delete
                                options = ["View leaderboard",  "Play the game", "View all users and delete them if you want", "Go back to main"]
                                for x in range(4):
                                    print(f"{x+1}. {options[x]}")

                                num = input("Please pick one of the options:").strip().lower()
                                if num.isdigit() == True:
                                    num = int(num)
                                    if num == 1:
                                        display_high_scores(information)
                                    elif num == 2:
                                        run_game(int(i["high score"]))
                                    elif num == 3:
                                        information = view_delete(information)
                                    elif num == 4:
                                        break
                                    else:
                                        print("Please put a number 1-4...")
                                else:
                                    print("Please enter a valid number")
                        else:
                            while True:
                                options = ["View leaderboard",  "Play the game", "Go back to main"]
                                for x in range(3):
                                    print(f"{x+1}. {options[x]}")

                                num = input("Please pick one of the options:").strip().lower()
                                if num.isdigit() == True:
                                    num = int(num)
                                    if num == 1:
                                        display_high_scores(information)
                                    elif num == 2:
                                        run_game(int(i["high score"]))
                                    elif num == 3:
                                        break
                                    else:
                                        print("Please put a number 1-3...")
                                else:
                                    print("Please enter a valid number")
                    else:
                        pass



        elif user_choice == '2':
            information = register(information)


        elif user_choice == '3':
            information = sign_out(information)
            save_changes(information)
            print("Thank you for playing!")
            break
        else:
            print("Please enter a valid choice")
        save_changes(information)


main()