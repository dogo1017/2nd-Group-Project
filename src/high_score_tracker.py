# MR 1st High Score Tracker

def display_top_scores(users, limit):






def saving_high_score(high_score, users):
    for user in users:
        if user["status"] == "active":
           user["highscore"] = str(high_score)
           return users
