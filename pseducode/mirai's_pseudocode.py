# MH 1st high score tracker pseudocode

# import hashlib

# function to register new user, takes in the list of users:
    # asks user for new username
    # if there's already a user registered under that name ask again
    # if not asks user for new password
    # if there's already a user with that password ask again
    # if not hash password
    # update list with new username and hashed password
    # return updated list

# function to display profile, takes in list with user logged in (used when user is already logged in):
    # searches through list for the user with status logged in
    # once found prints that users username, and current highscore

# save changes function, takes in the list of users:
    # updates csv with the entire list of users