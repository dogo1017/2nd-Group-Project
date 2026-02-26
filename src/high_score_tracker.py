# MR 1st High Score Tracker
import csv

filename = "user_info.csv"

def high_score_tracker():
    pass
    
def display_high_score():
        pass
        
def save_scores():
            pass
            
def load_scores():


    scores = {}
def update_leaderboard(name, new_score):
    scores = load_scores()
    if name in scores:
        if new_score > score[name]:
            score[name] = new_score
            print(f"New high score for {name}!")
        else:
            print(f"Score of {new_score} didn't beat your record of {scores[name]}")

    else:
        scores[name] = new_score
        print(f"First score recorded for {name}!")
    save_scores(scores)

dinosaur_game = ""

def main():
    while True:
        print("Welcome to the HIGH SCORE TRACKER!")
        print("Here you can play the dinosaur game and compare your high score to other users!")
        choice = input("Would you like to play, view your high score, or view leaderboard")
        if choice == '1':
            dinosaur_game()
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        else:
            break

main()