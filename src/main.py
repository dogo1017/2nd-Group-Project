# MAIN FUNCTION
from log_in import *
from high_score_tracker import *
from user_registration import *


def main():
    current_user = None
    while True:
        information = load_csv()
        print("Welcome to the High Score Tracker!")
        print(" 1. Log in")
        print(" 2. Create an Account")  
        print(" 3. Quit")      
        user_choice = input("What would you like to do?")
        if user_choice == '1':

            information, text =log_in(information)
            if text == 'game':
                for i in information:
                    if i["status"] == 'active':
                        if i["username"] == "admin":
                            pass
                        else:
                            pass



        elif user_choice == '2':
            register()
        elif user_choice == '3':
            
            save_changes()
            print("Thank you for playing!")
            break
        else:
            print("Please enter a valid choice")
        save_changes()

main()