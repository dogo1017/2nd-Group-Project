# MH 1st user registration 

import hashlib
import csv

def register(users):
    while True:
        username = input("Please input a username: ")
        for user in users:
            if user["username"] == username: 
                print("There is already a user with that name.")
                continue
        password = input("Please input a password: ")
        password_encoded = password.encode("utf-8")
        hashed_password = hashlib.shake_128(password_encoded)
        hex_password = hashed_password.hexdigest()
        users.append({"username" : username, "password" : hex_password, "high score" : 0, "status" : "active"})
        return users
    
def display_profile(users):
    for user in users:
        if user["status"] == "active":
            print(f"Useranme: {user["username"]}\nHighscore: {user["high score"]}")

def load_csv():
    with open("docs/user_info.csv", "r") as user_list:
        content = csv.reader(user_list)
        row_count = sum(1 for row in content)
        user_list.seek(0)
        if row_count == 0:
            headers = ["username", "password", "high score", "status"]
        else:
            headers = next(content)
        rows = []
        for line in content:
            rows.append({headers[0] : line[0], headers[1]})