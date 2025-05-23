from tkinter import *
from functools import partial  # to prevent unwanted windows
import random
import csv
from datetime import date


# helper functions go here
# Gets god name & correct god
def get_gods():
    # Retrieve gods from csv file and put them in a list
    file = open("00_gods_data_v2.csv", "r")
    all_gods = list(csv.reader(file, delimiter=","))
    file.close()

    round_gods = []
    # list to check there are no duplicate gods
    god_names = []

    # get the correct god
    correct_god = random.choice(all_gods)
    round_gods.append(correct_god)
    god_names.append(str(correct_god[2]).replace(" ", ""))

    # loop until we have three more gods
    while len(round_gods) < 4:
        potential_god = random.choice(all_gods)

        # Get the potential gods name and check it's not a duplicate
        if str(potential_god[2]).replace(" ", "") not in god_names:
            round_gods.append(potential_god)
            god_names.append(str(potential_god[2]).replace(" ", ""))

    return correct_god, round_gods


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

        # strings for labels
        intro_string = ("Each Round you will be given the domain of a god, and 4 gods to choose from. You will then "
                        "need to choose which of those 4 gods corresponds to that domain.\n\nThere are 2 options for "
                        "the number of rounds. You can either choose a specific number of rounds to play and then "
                        "press the play button, or you can play endless mode, where the game will not stop until "
                        "you end it.")

        # choose_string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Greek  & Roman Gods Quiz", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # Create labels and add them to the reference list

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], wraplength=375, justify="left",
                               pady=10, padx=10)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an error message if
        # necessary
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        # Frame so that endless button can take up a whole row while play button shares a row with entry box
        self.endless_frame = Frame(self.start_frame)
        self.endless_frame.grid(row=4)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=["Arial", "18", "bold"], width=10, bg="#DBDBDB",
                                      justify="center")
        self.num_rounds_entry.grid(row=0, column=0, padx=5, pady=10)

        # start button info list (frame | bg | fg | text | width | mode)
        start_button_list = [[self.endless_frame, "#76608A", "#FFFFFF", "Endless Mode", 21, "Endless"],
                             [self.entry_area_frame, "#E1D5E7", "#000000", "Play", 10, "Normal"]]
        # Create start buttons
        for count, item in enumerate(start_button_list):
            make_start_button = Button(item[0], font=["Arial", "16", "bold"], bg=item[1], fg=item[2], text=item[3],
                                       width=item[4], command=partial(self.check_rounds, item[5]))
            make_start_button.grid(row=0, column=count)

    def check_rounds(self, round_mode):
        """
        Checks users have entered 1 or more rounds
        """

        # retrieve round wanted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"),
                                 text="How many rounds do you want to play?")
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than 0."
        has_errors = "no"

        # checks that the no. of rounds wanted is valid
        if round_mode == "Normal":
            # checks that number of rounds wanted is more than 0
            try:
                rounds_wanted = int(rounds_wanted)
                if rounds_wanted > 0:
                    # invoke PLay Class (and take across number of rounds)
                    Play(rounds_wanted)
                    # Hide root window (ie: hide rounds choice window
                    self.num_rounds_entry.delete(0, END)
                    root.withdraw()
                else:
                    has_errors = "yes"

            except ValueError:
                has_errors = "yes"

            # display the error if necessary
            if has_errors == "yes":
                self.choose_label.config(text=error, fg="#990000", font=("Arial", "10", "bold"))
                self.num_rounds_entry.config(bg="#F4CCCC")
                self.num_rounds_entry.delete(0, END)

        else:
            # set rounds wanted to -1 to ensure game never ends
            rounds_wanted = -1
            # invoke PLay Class (and take across number of rounds)
            Play(rounds_wanted)
            # Hide root window (ie: hide rounds choice window
            self.num_rounds_entry.delete(0, END)
            root.withdraw()


class Play:
    """
    Interface for playing the God Quiz Game
    """

    def __init__(self, how_many):

        # counters for stats
        self.round_info = []
        self.rounds_won = IntVar()
        self.rounds_won.set(0)
        self.win_streak = 0
        self.lose_streak = 0

        # put 0 in list so that there is at least one item in each list
        self.all_win_streaks = []
        self.all_lose_streaks = []
        self.round_questions = []

        # create list to prevent duplicates
        self.past_asked_gods = []

        # rounds_played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # god choices list
        self.round_gods_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels...
        body_font = ("Arial", "12")

        # If users press the 'x' on the game window, end the entire game!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Who is the god of #?", body_font, "#FFFFFF", 1],
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
        self.results_label = play_labels_ref[2]
        self.question_label = play_labels_ref[1]

        # set up god buttons
        self.god_frame = Frame(self.game_frame)
        self.god_frame.grid(row=3)

        self.god_button_ref = []
        self.button_colours_ref = []

        # create 4 buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.god_button = Button(self.god_frame, font=["Arial", "12"],
                                     text="God Name", width=15,
                                     command=partial(self.round_results, item))
            self.god_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

            self.god_button_ref.append(self.god_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round  →", "#A0522D", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#60A917", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#E3C800", self.to_stats, 10, 0, 1],
            [self.game_frame, "End", "#76608A", self.close_play, 21, 7, None]
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3],
                                         font=["Arial", "16", "bold"], fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # images for use on buttons
        self.hint_image = PhotoImage(file="images/hint_v2.png")
        self.stats_image = PhotoImage(file="images/chart.png")
        self.sad_face = PhotoImage(file="images/sad_face.png")
        self.happy_face = PhotoImage(file="images/happy_face.png")

        # Disable stats button so that users can't press it without having completed a round, & add image
        self.stats_button.config(state=DISABLED)
        self.stats_button.config(text="Stats  ",
                                 image=self.stats_image,
                                 compound="right", width=132, fg="#000000")

        # Hint Button with image
        self.hints_button.config(text="Hints  ",
                                 image=self.hint_image,
                                 compound="right", width=132)

        # End Game Button with sad face
        self.end_game_button.config(text="End Game  ",
                                    image=self.sad_face,
                                    compound="right", width=280)

        # Once interface has been created, invoke new round function for
        # first round
        self.new_round()

    def new_round(self):
        """
        Checks four gods, Configures buttons with god choices
        """

        # reset round data list
        self.round_info = []

        # get round gods and correct god
        # if a question about this god has been asked, get a different god.
        while True:
            # get round gods and correct god
            gods_list = get_gods()
            self.round_gods_list = gods_list[1]
            correct_god = gods_list[0]
            # If all gods have been asked about, allow duplicates
            if 0 <= len(self.past_asked_gods) < 64:
                if correct_god in self.past_asked_gods:
                    continue
            break

        # set up background colour based of the correct god's mythology
        if correct_god[0] == "Roman":
            god_colour = "#F8CECC"
        else:
            god_colour = "#DAE8FC"

        # due to their domain text, format Juno, Mercury, Pluto, and Pontus questions differently.
        exception_list = ["Juno", "Mercury", "Pluto", "Pontus "]
        if correct_god[2] not in exception_list:
            question_text = f"Who is the god of {correct_god[3]}?"
        else:
            question_text = f"Who is the {correct_god[3]}?"

        # add to round info list
        self.round_info.append(question_text)

        # retrieve no. of rounds played & no. of rounds wanted
        rounds_wanted = self.rounds_wanted.get()
        rounds_played = self.rounds_played.get()

        # Update heading label. "Hide" results label
        # change heading depending on round mode
        if rounds_wanted > 0:
            heading_text = f"Round {rounds_played + 1} of {rounds_wanted}"
        else:
            heading_text = f"Round {rounds_played + 1}"
        self.heading_label.config(text=heading_text, bg="#DEDEDE")
        # if the user has answered a question for all gods, give them a notice of duplicate questions
        if len(self.past_asked_gods) == 64:
            self.results_label.config(text=f"         ======= Well done! =======\nYou have answered a "
                                           f"question about all the gods in this quiz. "
                                           f"\nYou can keep on playing, but all questions will "
                                           f"be a duplicate from here on out. \nThank you for playing my game!",
                                      bg="#ffff99")
        else:
            self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # add question text to question label
        self.question_label.config(text=question_text, bg=god_colour)

        # shuffle god list
        random.shuffle(self.round_gods_list)

        # enable god buttons (disabled at end of last round)
        for count, item in enumerate(self.god_button_ref):
            # Get God Colour based on if it's a major or minor god
            if self.round_gods_list[count][1] == "Minor":
                button_colour = "#E0E0E0"
                text_color = "#404040"
            else:
                button_colour = "#FFF2CC"
                text_color = "#59460D"
            item.config(fg=text_color, bg=button_colour,
                        text=self.round_gods_list[count][2], state=NORMAL, command=partial(self.round_results,
                                                                                           count, correct_god))

        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice, correct_god):
        """
         Retrieves which button was pushed (index 0 - 3), retrieves answer and then compares
         it with median, updates results and adds results to stats list.
         """

        # retrieve no. of rounds played and add one to it
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        # alternate way to get button name. Good for if buttons have been scrambled!
        chosen_god = self.god_button_ref[user_choice].cget('text')

        # make the correct god's button green
        self.god_button_ref[self.round_gods_list.index(correct_god)].config(bg="#b2d99c")

        # add to question lists
        self.round_info.append(correct_god[2])
        self.round_info.append(chosen_god)
        self.round_questions.append(self.round_info)

        if chosen_god == correct_god[2]:
            result_text = f"Success! {chosen_god} is correct!!"
            result_bg = "#82B366"
            # add to stats lists
            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)
            # increase lose streak for stats
            self.win_streak += 1
            # add lose streak to stats list if the ongoing lose streak is longer than 0
            if self.lose_streak > 0:
                self.all_lose_streaks.append(self.lose_streak)
                self.lose_streak = 0
        else:
            # Change incorrectly chosen god button to red
            self.god_button_ref[user_choice].config(bg="#f5bcba")
            result_text = f"Oops, {chosen_god} is incorrect."
            result_bg = "#F8CECC"
            # increase lose streak for stats
            self.lose_streak += 1
            # add win streak to stats list if the ongoing win streak is longer than 0
            if self.win_streak > 0:
                self.all_win_streaks.append(self.win_streak)
                self.win_streak = 0

        # add correct god to past asked gods list to prevent duplicates of questions
        self.past_asked_gods.append(correct_god)

        self.results_label.config(text=result_text, bg=result_bg)

        # enable next round & stats button buttons. disable god buttons
        self.next_button.config(state=NORMAL)
        for item in self.god_button_ref:
            item.config(state=DISABLED)

        # check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()
        # only enable stats button after 1st round to prevent being able to open multiple boxes
        if rounds_played == 1:
            self.stats_button.config(state=NORMAL)

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            # change 'end game' button to 'play again' button once the game has ended
            self.end_game_button.config(text="Play Again  ", bg="#006600", image=self.happy_face)

    def close_play(self):
        # reshow root (ie:choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_hints(self):
        """
        Displays hints for playing game
        :return:
        """
        # get the no. of rounds played so that the stats button is not enabled if no rounds have been completed
        rounds_played = self.rounds_played.get()
        DisplayHints(self, rounds_played)

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics
        """

        # add final streak to list
        self.all_lose_streaks.append(self.lose_streak)
        self.all_win_streaks.append(self.win_streak)

        # IMPORTANT: retrieve number of rounds
        # won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        rounds_played = self.rounds_played.get()
        stats_bundle = [rounds_won, rounds_played, self.all_win_streaks, self.all_lose_streaks, self.round_questions]

        Stats(self, stats_bundle)


class DisplayHints:
    """
    Displays hints for God Quiz Game
    """

    def __init__(self, partner, rounds_played):
        self.rounds_played = rounds_played

        # Disable buttons to prevent program crashing
        partner.hints_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # setup dialogue box and background colour
        background = "#D5E8D4"
        self.hint_box = Toplevel()

        # If user press cross at top, closes hint and 'releases' hint button
        self.hint_box.protocol('WM_DELETE_WINDOW', partial(self.close_hint, partner))

        self.hint_frame = Frame(self.hint_box, width=300,
                                height=200, bg=background)
        self.hint_frame.grid()

        # label containing heading
        self.hint_heading_label = Label(self.hint_frame, bg="#FFFFFF", text="Hints", font=["Arial", "16", "bold"],
                                        width=6)
        self.hint_heading_label.grid(row=0, pady=10)

        hint_text = "The background colour of the question is relates to the " \
                    "mythology that the correct god is from:\nRed = Roman\nBlue = Greek\n" \
                    "This means that if the game asks you who the god of wisdom is, you know that the answer would " \
                    "be Athena for a blue background, and Minerva for a red background.\n\nThe colour of each button " \
                    "relates to whether the god is a Major(Gold) god or a Minor(Silver) god, and is NOT a hint."

        # label containing hints text
        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text, font=["Arial", "12"], wraplength=400,
                                     justify="left", bg=background)
        self.hint_text_label.grid(row=1, padx=15)

        # Dismiss button
        self.dismiss_button = Button(self.hint_frame,
                                     font=["Arial", "16", "bold"],
                                     text="Dismiss", bg="#60A917", fg="#FFFFFF", width=15,
                                     command=partial(self.close_hint, partner))
        self.dismiss_button.grid(row=2, pady=15, padx=10)


    def close_hint(self, partner):
        """
        Closes hint dialogue box (and enables hint button)
        """
        # put buttons back to normal
        partner.hints_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)
        # only enable stats button if played > 1 round
        if self.rounds_played > 1:
            partner.stats_button.config(state=NORMAL)
        self.hint_box.destroy()


class Stats:
    """
    Displays stats for Colour Quest Game
    """

    def __init__(self, partner, all_stats_info):

        # Disable buttons to prevent program crashing
        partner.hints_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # Extract info from master list
        rounds_won = all_stats_info[0]
        rounds_played = all_stats_info[1]
        win_streaks = all_stats_info[2]
        lose_streaks = all_stats_info[3]
        round_data = all_stats_info[4]

        # sort streaks to find the highest streak
        win_streaks.sort()
        lose_streaks.sort()

        # setup dialogue box
        self.stats_box = Toplevel()

        # list for strings to bring to export
        export_strings = []

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # If user press cross at top, closes stats and 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300,
                                 height=200, bg="#FFF2CC")
        self.stats_frame.grid()

        # math to populate stats dialogue
        success_rate = rounds_won / rounds_played * 100

        # make strings for Stats labels and add them to export lists...
        rounds_string = f"Rounds Played: {rounds_played}"
        export_strings.append(rounds_string)
        success_string = (f"Success rate: {rounds_won} / {rounds_played} "
                          f"({success_rate:.0f}%)")
        export_strings.append(success_string)
        longest_win_string = f"Longest Win Streak: {max(win_streaks)}"
        export_strings.append(longest_win_string)
        longest_lose_string = f"Longest Lose Streak: {max(lose_streaks)}"
        export_strings.append(longest_lose_string)

        # custom comment text and formatting
        if rounds_won == rounds_played:
            comment_string = "Well Done! You have won every\nround so far :)"
            comment_colour = "#D5E8D4"
            border_colour = "#82B366"

        elif rounds_won == 0:
            comment_string = "Oops - You've not won \nany rounds yet :( You might want \n" \
                             "to look at the hints!"
            comment_colour = "#F8CECC"
            border_colour = "#B85450"

        else:
            comment_string = ""
            comment_colour = "#FFF2CC"
            border_colour = "#FFF2CC"

        # create strings for round data
        left_round_string = ""
        right_round_string = ""
        round_string_list = []
        export_data = ""
        for count, item in enumerate(round_data):
            if item in round_data[-4:]:
                if len(round_data) >= 3:
                    if count == len(round_data) - 2 or count == len(round_data) - 4:
                        right_round_string += f"\n{item[0]}\nYou answered: {item[2]}\n" \
                                              f"The correct answer was: {item[1]}\n"
                    else:
                        left_round_string += f"\n{item[0]}\nYou answered: {item[2]}\n" \
                                             f"The correct answer was: {item[1]}\n"
                else:
                    left_round_string += f"\n{item[0]}\nYou answered: {item[2]}\nThe correct answer was: {item[1]}\n"
            export_data += f"\n{item[0]} \nYour answer: {item[2]}\nCorrect answer: {item[1]}\n"
        # add string to export list
        export_strings.append(export_data)
        # add round strings to list for label making
        round_string_list.append(left_round_string)
        round_string_list.append(right_round_string)

        # fonts for labels
        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # info frame for stats info
        self.info_frame = Frame(self.stats_frame, background="#FFF2CC")
        self.info_frame.grid(row=2, pady=10)

        # Label List (text | font | 'Sticky' | row | column | frame)
        all_stats_strings = [
            ["Statistics", heading_font, "", 1, 0, self.stats_frame],
            [rounds_string, normal_font, "W", 1, 0, self.info_frame],
            [success_string, normal_font, "W", 1, 1, self.info_frame],
            [longest_win_string, normal_font, "W", 2, 0, self.info_frame],
            [longest_lose_string, normal_font, "W", 2, 1, self.info_frame],
            [comment_string, comment_font, "", 3, 0, self.stats_frame],
            ["Round Data", heading_font, "", 4, 0, self.stats_frame]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            # change formatting if there is only one question
            # don't change formatting of stats frame strings
            if len(round_data) < 3 and item[5] != self.stats_frame:
                row = count
                column = 0
            else:
                row = item[3]
                column = item[4]
            self.stats_label = Label(item[5], text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=20, pady=10, bg="#FFF2CC")
            self.stats_label.grid(row=row, column=column, sticky=item[2])
            stats_label_ref_list.append(self.stats_label)

        # config heading label
        heading_label = stats_label_ref_list[0]
        heading_label.grid(pady=10)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[5]
        stats_comment_label.config(bg=comment_colour, highlightbackground=border_colour, highlightthickness=2)
        if comment_string == "":
            stats_comment_label.destroy()

        # line label rows
        line_rows = [5, 8]
        for item in line_rows:
            self.line_label = Label(self.stats_frame, text=f"{'-' * 180}", bg="#FFF2CC", font=["Arial", "5"])
            self.line_label.grid(row=item)

        # overload notice
        self.overload_label = Label(self.stats_frame,
                                    text=f"Showing 4 most recent rounds - 4/{rounds_played} rounds shown, \nplease "
                                         "export to file to see other rounds", font=["Arial", "14"], justify="left",
                                    background="#E3E1FF", padx=30, pady=15)
        self.overload_label.grid(row=6, pady=7)

        background = "#E3E1FF"        # if there are 4 or fewer questions completed, destroy overload notice & change round data background to white
        if len(round_data) <= 4:
            background = "#FFFFFF"
            self.overload_label.destroy()

        # create frame for round data
        self.data_frame = Frame(self.stats_frame, bg=background)
        self.data_frame.grid(row=7, pady=5, padx=20)

        # list to get labels for later editing
        data_labels = []
        # create a label to hold the past 3 rounds' data
        for count, item in enumerate(round_string_list):
            self.data_label = Label(self.data_frame, text=item, font=["Arial", "14"], justify="left",
                                    padx=10, pady=5, bg=background, wraplength=330, width=28)
            self.data_label.grid(row=1, column=count)
            data_labels.append(self.data_label)

        # if there are 2 or fewer questions answered, remove empty label
        if round_string_list[1] == "":
            data_labels[1].destroy()
            data_labels[0].config(width=30, wraplength=350, padx=10)

        self.buttons_frame = Frame(self.stats_frame, bg="#FFF2CC")
        self.buttons_frame.grid(row=9, pady=5)

        # buttons info list (text | bg | width | command)
        buttons_strings = [
            ["Export to File", "#F0A30A", partial(self.export_to_file, export_strings)],
            ["Dismiss", "#E3C800", partial(self.close_stats, partner)]
        ]

        # create buttons
        # button_ref
        self.stats_button_ref = []
        for count, item in enumerate(buttons_strings):
            self.stats_button = Button(self.buttons_frame,
                                       font=["Arial", "16", "bold"], text=item[0],
                                       bg=item[1], width=25,
                                       command=item[2])
            self.stats_button.grid(row=count, padx=30, pady=7)
            self.stats_button_ref.append(self.stats_button)

        # Get export button for configuring
        self.export_button = self.stats_button_ref[0]

    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enables stats button)
        """
        # put disabled buttons back to normal...
        partner.hints_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

    # export round data to file
    def export_to_file(self, strings):
        """
        export data to a text file
        """

        # Change exported button when pressed so users are aware it worked
        self.export_button.config(text="Exported!")

        # **** Get current date for heading and filename
        today = date.today()

        # get day, month and year as individual strings
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        file_name = f"god_quiz_{year}_{month}_{day}"
        write_to = f"{file_name}.txt"

        # open file and write in stats
        with open(write_to, "w") as text_file:
            text_file.write("============= God Quiz =============\n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")
            for item in strings[:4]:
                text_file.write(f"{item}\n")
            text_file.write("-" * 25)
            text_file.write(strings[4])
            text_file.write("=" * 36)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("God Quiz")
    StartGame()
    root.mainloop()
