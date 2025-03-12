import csv
import random


# Retrieve gods from csv file and put them in a list
file = open("00_gods_data.csv", "r")
all_gods = list(csv.reader(file, delimiter=","))
file.close()

round_gods = []
god_names = []

# get the correct god
correct_god = random.choice(all_gods)
round_gods.append(correct_god)
god_names.append(correct_god[2])

# loop until we have 3 other gods with different names
while len(round_gods) < 4:
    potential_god = random.choice(all_gods)

    # Get the name and check it's not a duplicate
    if potential_god[2] not in god_names:
        round_gods.append(potential_god)
        god_names.append(potential_god[2])

print(f"Correct answer: {correct_god}")
print(f"Other answers: {round_gods[1], round_gods[2], round_gods[3]}")
print(f"All god names: {god_names}")
