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

        # Lowest Score Test Data
        # self.rounds_played.set(5)
        # self.rounds_won.set(0)
        # self.win_streak = [0]
        # self.lose_streak = [5]

        # Random Score Test Data
        self.rounds_played.set(5)
        self.rounds_won.set(3)
        self.win_streak = [2, 1]
        self.lose_streak = [1, 1]

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
        stats_bundle = [rounds_won, rounds_played, self.win_streak, self.lose_streak]

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
            comment_string = ("Amazing! You got every question correct!")
            comment_colour = "#D5E8D4"
            border_colour = "#82B366"

        elif max(lose_streaks) == rounds_played:
            comment_string = ("Oops - You've lost every round! \nYou might want "
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
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
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

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "16", "bold"), text="Dismiss",
                                     bg="#E3C800", width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=30, pady=30)

        # closes help dialogue (used by button and x at top of dialogue

    def close_stats(self, partner):
        """
        Closes stats dialogue box (and enables stats button)
        """
        # put stats button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
