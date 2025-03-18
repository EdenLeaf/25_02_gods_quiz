from tkinter import *
from functools import partial  # TO prevent unwanted windows
import csv
import random


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
        self.rounds_played = IntVar()
        self.rounds_won = IntVar()

        # Lists for stats component

        # Highest Score Test Data
        # self.rounds_played.set(5)
        # self.rounds_won.set(5)
        # self.win_streak = [5]
        # self.lose_streak = [0]
        # self.round_data = [["Who is the god of Sleep?", "Hypnos", "Hypnos"], ["Who is the god of fire?",
        # "Vulcan", "Vulcan"], ["Who is the queen of the gods?", "Juno", "Juno"]]

        # Lowest Score Test Data
        # self.rounds_played.set(5)
        # self.rounds_won.set(0)
        # self.win_streak = [0]
        # self.lose_streak = [5]
        # self.round_data = [["Who is the god of Light?", "Hemera", "Aether"], ["Who is the god of beauty?",
        # "Flora", "Venus"], ["Who is the god of the night?", "Pax", "Nyx"]]

        # Random Score Test Data
        self.rounds_played.set(5)
        self.rounds_won.set(3)
        self.win_streak = [2, 1]
        self.lose_streak = [1, 1]
        self.round_data = [["Who is the god of Poison?", "Achyls", "Achlys"], ["Who is the messenger of the gods?",
        "Mercury", "Mercury"], ["Who is the god of the sea?", "Uranus", "Neptune"]]

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="God Quiz",
                                   font=("Arial", "16", "bold"), padx=5,
                                   pady=5)
        self.heading_label.grid(row=0)

        self.stats_button = Button(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Stats", width=15, fg="#FFFFFF", bg="#FF8000",
                                   padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics
        """

        # IMPORTANT: retrieve number of rounds
        # won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        rounds_played = self.rounds_played.get()
        stats_bundle = [rounds_won, rounds_played, self.win_streak, self.lose_streak, self.round_data]

        Stats(self, stats_bundle)


class Stats:
    """
    Displays stats for Colour Quest Game
    """

    def __init__(self, partner, all_stats_info):

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

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # If user press cross at top, closes stats and 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300,
                                 height=200, bg="#FFF2CC")
        self.stats_frame.grid()

        # math to populate stats dialogue
        success_rate = rounds_won / rounds_played * 100

        # strings for Stats labels...
        rounds_string = f"Rounds Played: {rounds_played}"
        success_string = (f"Success rate: {rounds_won} / {rounds_played} "
                          f"({success_rate:.0f})%")
        longest_win_string = f"Longest Win Streak: {max(win_streaks)}"
        longest_lose_string = f"Longest Lose Streak: {max(lose_streaks)}"

        # custom comment text and formatting
        if max(win_streaks) == rounds_played:
            comment_string = ("Well Done! You have won every\nround so far :)")
            comment_colour = "#D5E8D4"
            border_colour = "#82B366"

        elif max(lose_streaks) == rounds_played:
            comment_string = ("Oops - You've not won \nany rounds yet :( You might want \n"
                              "to look at the hints!")
            comment_colour = "#F8CECC"
            border_colour = "#B85450"

        else:
            comment_string = ""
            comment_colour = "#FFF2CC"
            border_colour = "#FFF2CC"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label List (text | font | bg | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [rounds_string, normal_font, "W"],
            [success_string, normal_font, "W"],
            [longest_win_string, normal_font, "W"],
            [longest_lose_string, normal_font, "W"],
            [comment_string, comment_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=30, pady=10, bg="#FFF2CC")
            self.stats_label.grid(row=count, sticky=item[2], padx=40)
            stats_label_ref_list.append(self.stats_label)

        # config heading label
        heading_label = stats_label_ref_list[0]
        heading_label.config(bg="#FFFFFF")
        heading_label.grid(pady=10)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[5]
        stats_comment_label.config(bg=comment_colour, highlightbackground=border_colour, highlightthickness=2)
        if comment_string == "":
            stats_comment_label.destroy()

        self.line_label = Label(self.stats_frame, text=f"{'-' * 160}", bg="#FFF2CC", font=("Arial", "5"))
        self.line_label.grid(row=8, pady=10)

        # create strings for round a
        data_string = ""
        for item in round_data:
            data_string += f"\n{item[0]} \nYou answered: {item[1]} \nThe correct answer was: {item[2]}\n"

        # create a label to hold the past 3 rounds' data
        self.data_label = Label(self.stats_frame, text=data_string, font=("Arial", "14"), justify="left",
                                padx=30, pady=5, bg="#FFFFFF")
        self.data_label.grid(row=9, padx=20)

        self.buttons_frame = Frame(self.stats_frame, bg="#FFF2CC")
        self.buttons_frame.grid(row=10, pady=15)

        # buttons info list (text | bg | width | command)
        buttons_strings = [
            ["Export to File", "#F0A30A", 20, self.export_to_file],
            ["Dismiss", "#E3C800", 15, partial(self.close_stats, partner)]
        ]

        # create buttons
        for count, item in enumerate(buttons_strings):
            self.stats_button = Button(self.buttons_frame,
                                       font=("Arial", "16", "bold"), text=item[0],
                                       bg=item[1], width=item[2],
                                       command=item[3])
            self.stats_button.grid(row=count, padx=30, pady=7)

        # closes help dialogue (used by button and x at top of dialogue

    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enables stats button)
        """
        # put stats button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

    # export round data to file
    def export_to_file(self):
        """
        Closes stats dialogue box (and enables stats button)
        """

        print("EXPORT GOES HERE")


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
