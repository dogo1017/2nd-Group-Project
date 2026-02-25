#RC 1st, my code

#Import hashlib
import hashlib

#Create function for logging in
def log_in(information):
    #Put into loop
    while True:
        #Ask them what they want to sign into, or if they want to quit
        sign_in = input("Do you want to sign in? If you do put yes, otherwise type quit:").strip().lower()
        #Get correct input
        if sign_in == "yes" or sign_in == "quit":
            break
    if sign_in == "quit":
        return information, "quit"
    #Put into a loop
    while True:
        fix = False
        username = input("Please enter your username (put quit if you want to exit):")
        #Then allow them to input passwords with an option to quit
        for i in information:
            if i["username"] == username:
                fix = True
                break
        if fix == True:
            break
        if username == "quit":
            return information, "quit"
        else: 
            print("That username doesn't exist...")
    while True:
            #if they entered a correct username, ask them for there password or quit
            password = input("Please tell me the password (Put quit if you want to exit):")
                           #Check hashed password 
            mixer = hashlib.shake_128()
            h_password = password.encode('utf-8')
            mixer.update(h_password)
            f_password = mixer.hexdigest(16)
            if password == "quit":
                return information, "quit"
            for i in information:
                if f_password == list(i[username])[0]:
                    list(i[username])[1] = "Active"
                    return information, "game"
            else:
                print("That is not the correct password...")


def view_delete(information):
    pass
    #This will allow the admin to view highscores and all acounts
    #Also make it so that they can delete acounts

#Example of values
#[{"username": username
#  "highscore": 357
#  "status": inactive}]