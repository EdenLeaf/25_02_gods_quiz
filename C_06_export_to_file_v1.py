from datetime import date

rounds = [["Who is the god of Poison?", "Achyls", "Achlys"], ["Who is the messenger of the gods?",
        "Mercury", "Mercury"], ["Who is the god of the sea?", "Uranus", "Neptune"], ["Who is the queen of the gods?",
                                                    "Juno", "Juno"], ["Who is the god of Light?", "Hemera", "Aether"]]
results = [5, 3, [2, 1], [1, 1]]

# **** Get current date for heading and filename
today = date.today()

# get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

file_name = f"god_quiz_{year}_{month}_{day}"
write_to = f"{file_name}.txt"

# math to populate stats dialogue
success_rate = results[1] / results[0] * 100

# strings for Stats labels...
rounds_string = f"Rounds Played: {results[0]}\n"
success_string = (f"Success rate: {results[1]} / {results[0]} "
                  f"({success_rate:.0f})%\n")
longest_win_string = f"Longest Win Streak: {max(results[2])}\n"
longest_lose_string = f"Longest Lose Streak: {max(results[3])}\n"

# create strings for round data
data_string = ""
for item in rounds:
    data_string += f"\n{item[0]} \nYou answered: {item[1]} \nThe correct answer was: {item[2]}\n"

with open(write_to, "w") as text_file:

    text_file.write("***** God Quiz *****\n")
    text_file.write(f"Generated: {day}/{month}/{year}\n\n")
    text_file.write(rounds_string)
    text_file.write(success_string)
    text_file.write(longest_win_string)
    text_file.write(longest_lose_string)
    text_file.write(data_string)

