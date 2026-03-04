# MR 1st High Score Tracker
import csv
import os

FILENAME = "user_info.csv"


def load_scores():
    """Loads scores from CSV into a dictionary {name: score}."""
    scores = {}
    if not os.path.exists(FILENAME):
        return scores
    
    with open(FILENAME, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row: # Check for empty rows
                name, score = row[0], int(row[1])
                scores[name] = score
    return scores

def update_high_scores(username, new_score):
    """Updates the dictionary and saves to CSV after sorting."""
    scores = load_scores()
    
    # Only update if the user is new or the new score is higher
    if username not in scores or new_score > scores[username]:
        scores[username] = new_score
        
    # 1. Convert dictionary to a list of tuples to sort by score (value)
    # 2. Sort descending (reverse=True)
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    # Save the full updated list back to the CSV
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sorted_scores)

def display_top_scores(limit=5):
    """Loads and displays the top N high scores."""
    scores = load_scores()
    # Sort for display purposes
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    print(f"\n--- TOP {limit} HIGH SCORES ---")
    for i, (name, score) in enumerate(sorted_scores[:limit], 1): # Slicing for top N
        print(f"{i}. {name}: {score}")

def menu():
    while True:
        pass