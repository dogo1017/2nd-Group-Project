# MR 1st High Score Tracker

def leader_board(information):
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

def saving_high_score(high_score, users):
    for user in users:
        if user["status"] == "active":
           user["highscore"] = str(high_score)
           return users

