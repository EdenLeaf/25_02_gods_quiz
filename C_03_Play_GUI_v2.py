from tkinter import *
from functools import partial  # TO prevent unwanted windows
import csv
import random


# helper functions go here
# Gets god name & correct god
def get_gods():
    # Retrieve gods from csv file and put them in a list
    file = open("00_gods_data_v2.csv", "r")
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

    return god_names, correct_god


class StartGame:
    """
    Initial Game Interface (asks users how many rounds they would like to play)
    """

    def __init__(self):
        """
        Gets number of round from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button...
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"), fg="#FFFFFF",
                                  bg="#0057D8", text="Play", width=10, command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        Play(5)
        # Hide root window (ie: hide rounds choice window
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):

        # Integers / string variables
        self.gods_list = []
        self.target_score = IntVar()

        # rounds_played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # colour lists and score list
        self.round_gods_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels...
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Who is the god of #?", body_font, "#FFFFFF", 1],
            ["Choose a god below. Good luck. 🍀", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1], bg=item[2],
                                    wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve labels so that they can be configured later
        self.heading_label = play_labels_ref[0]
        self.results_label = play_labels_ref[3]
        self.question_label = play_labels_ref[1]

        # set up colour buttons
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        self.god_button_ref = []
        self.button_colours_ref = []

        # create 4 buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.god_button = Button(self.colour_frame, font=("Arial", "12"),
                                     text="God Name", width=15,
                                     command=partial(self.round_results, item))
            self.god_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

            self.god_button_ref.append(self.god_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#A0522D", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#60A917", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#E3C800", "", 10, 0, 1],
            [self.game_frame, "End", "#76608A", self.close_play, 21, 7, None]
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3],
                                         font=("Arial", "16", "bold"), fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Once interface has been created, invoke new round function for
        # first round
        self.new_round()

    def new_round(self):
        """
        Checks four colours, works out median for score to beat. Configures
        buttons with stolen colours
        """

        # retrieve no. of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get round gods and correct god
        self.gods_list = get_gods()
        self.round_gods_list = self.gods_list[0]
        correct_god = self.gods_list[1]
        print(correct_god[2])

        # set up background colour based of the correct god's mythology
        god_colour = ""
        if correct_god[0] == "Roman":
            god_colour = "#F8CECC"
        else:
            god_colour = "#DAE8FC"

        # due to their domain text, format Juno, Mercury, and Pluto questions differently.
        if correct_god[2] != "Juno" and correct_god[2] != "Mercury" and correct_god[2] != "Pluto":
            question_text = f"Who is the god of {correct_god[3]}?"
        else:
            question_text = f"Who is the {correct_god[3]}?"

        # Update heading, and score to beat labels. "Hide" results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")
        self.question_label.config(text=question_text, bg=god_colour)

        # shuffle god name list
        random.shuffle(self.round_gods_list)

        # configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at end of last round)
        for count, item in enumerate(self.god_button_ref):
            item.config(fg="#000000", bg="#FFFFFF",
                        text=self.round_gods_list[count], state=NORMAL, command=partial(self.round_results,
                                                                                        count, correct_god))

        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice, correct_god):
        """
         Retrieves which button was pushed (index 0 - 3), retrieves answer and then compares
         it with median, updates results and adds results to stats list.
         """
        # get user answer and colour based on button press...
        answer = self.round_gods_list[user_choice][1]

        # alternate way to get button name. Good for if buttons have been scrambled!
        god_name = self.god_button_ref[user_choice].cget('text')

        if god_name == correct_god[2]:
            result_text = f"Success! {god_name} is correct!!"
            result_bg = "#82B366"
            self.all_scores_list.append(answer)
        else:
            result_text = f"Oops, {god_name} is incorrect."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # enable stats and next buttons. disable colour buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.god_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie:choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
