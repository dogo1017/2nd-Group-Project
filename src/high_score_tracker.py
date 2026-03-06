# MR 1st High Score Tracker

def leader_board(information):
    top_scores = []
    top_user = []
    scores = []
    user = []
    not_allowed = []
    for i in information:
        scores.append(int(i["high score"]))
        user.append(i["username"])

    top_scores = sorted(scores, reverse = True)[:5]
    



    for score in top_scores:
        for i in information:
            if int(i["high score"]) == score:
                if i["username"] not in not_allowed:
                    top_user.append(i["username"])
                    not_allowed.append(i["username"])
    return top_scores, top_user



def display_high_scores(information):
    top_scores, top_user = leader_board(information)
    print("--------------------LEADER BOARD--------------------")
    print("These are the top 5 High Scores !")
    for x in range(5):
        print(f"{x+1}: {top_user[x]}, {top_scores[x]}")



def saving_high_score(high_score, users):
    for user in users:
        if user["status"] == "active":
           user["highscore"] = str(high_score)
           return users


