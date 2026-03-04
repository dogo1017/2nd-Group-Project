# MAIN FUNCTION
from log_in import *
from high_score_tracker import *
from user_registration import *


def main():
    current_user = None
    while True:
        print("Welcome to the High Score Tracker!")
        print(" 1. Log in")
        print(" 2. Create an Account")        
        user_choice = input("What would you like to do?")
        if user_choice == '1':
            log_in.log_in()
        elif user_choice == '2':
            user_registration.register()
        else:
            break

main()