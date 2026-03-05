#RC 1st, my code

#Import hashlib
import hashlib
from user_registration import *
information = load_csv()
#Create function for logging in
def log_in(information):
    information = sign_out(information)
    #Put into loop
    while True:
        #Ask them what they want to sign into, or if they want to quit
        sign_in = input("Do you want to sign in? If you do put yes, otherwise type exit:").strip().lower()
        #Get correct input
        if sign_in == "yes" or sign_in == "exit":
            break
    if sign_in == "exit":
        return information, "exit"
    #Put into a loop
    while True:
        fix = False
        username = input("Please enter your username (put quit if you want to exit):").strip()
        #Then allow them to input passwords with an option to quit
        for i in information:
            if i["username"] == username:
                fix = True
                break
        if fix == True:
            break
        if username == "exit":
            return information, "exit"
        else: 
            print("That username doesn't exist...")
    while True:
            #if they entered a correct username, ask them for there password or quit
            password = input("Please tell me the password (Put quit if you want to exit):").strip()
                           #Check hashed password 
            mixer = hashlib.shake_128()
            h_password = password.encode('utf-8')
            mixer.update(h_password)
            f_password = str(mixer.hexdigest(4))
            if password == "exit":
                return information, "exit"
            for i in information:
                if f_password == i["password"]:
                    i["status"] = "active"
                    return information, "game"
            else:
                print("That is not the correct password...")


def view_delete(information):

    #This will allow the admin to view highscores and all acounts
    x = 0
    for i in information:
        x+= 1
        print(f"{x}. Username: {i['username']} \n   Password: {i['password']} \n   Online Status: {i['status']} \n   Highscore: {i['high score']}")
    #Also make it so that they can delete acounts
    while True:
        choice = input("Would you like to remove an account or go back to main? (To remove put remove, To go back to main put exit):").strip().lower()
        if choice == "remove":
            break
        elif choice == "exit":
            return information
        else:
            print("That is not an available input...")
    while True:
        num = input("Please put the number of the account you want to remove (If you want to exit, put exit):").strip()
        if int(num) >= 1 and int(num) <= len(information) and num.isdigit() == True:
            num = int(num)
            break
        elif num == "exit":
            return information
        else:
            print("That is not a valid input...")
    information.pop(num-1)
    return information



def sign_out(information):
    #Go through and check each to make sure that they are signed out
    for i in information:
        if i["status"] == "active":
            i["status"] = "inactive"
    return information




top_scores = []
top_user = []
scores = []
user = []
for i in information:
    scores.append(int(i["high score"]))
    user.append(i["username"])

top_scores = sorted(scores, reverse = True)[:5]



for score in top_scores:
    for i in information:
        if int(i["high score"]) == score:
            top_user.append(i["username"])


print(top_scores)
print(top_user)

