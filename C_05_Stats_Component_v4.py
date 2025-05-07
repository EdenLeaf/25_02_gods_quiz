from tkinter import *
from functools import partial  # TO prevent unwanted windows
import csv
import random
from datetime import date


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
        self.rounds_played.set(3)
        self.rounds_won.set(3)
        self.win_streak = [3]
        self.lose_streak = [0]
        self.round_data = [["Who is the god of Sleep?", "Hypnos", "Hypnos"],
                           ["Who is the god of fire?", "Vulcan", "Vulcan"],
                           ["Who is the queen of the gods?", "Juno", "Juno"]]

        # Lowest Score Test Data
        # self.rounds_played.set(3)
        # self.rounds_won.set(0)
        # self.win_streak = [0]
        # self.lose_streak = [3]
        # self.round_data = [["Who is the god of Light?", "Hemera", "Aether"], ["Who is the god of beauty?",
        # "Flora", "Venus"], ["Who is the god of the night?", "Pax", "Nyx"]]

        # Random Score Test Data
        # self.rounds_played.set(3)
        # self.rounds_won.set(2)
        # self.win_streak = [2]
        # self.lose_streak = [1]
        # self.round_data = [["Who is the god of Poison?", "Achyls", "Achlys"], ["Who is the messenger of the gods?",
        # "Mercury", "Mercury"], ["Who is the god of the sea?", "Uranus", "Neptune"]]

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

        # make strings for Stats labels and add them to export lis...
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

        # create strings for round data
        data_string = ""
        export_data = ""
        for item in round_data:
            if item in round_data[-3:]:
                data_string += f"\n{item[0]} ({item[2]})\nYou answered: {item[1]}\n"
            export_data += f"\n{item[0]} \nYour answer: {item[1]}\nCorrect answer: {item[2]}\n"
        # add string to export list
        export_strings.append(export_data)

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label List (text | font 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [rounds_string, normal_font, "W"],
            [success_string, normal_font, "W"],
            [longest_win_string, normal_font, "W"],
            [longest_lose_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["Round Data", heading_font, ""]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=30, pady=10, bg="#FFF2CC")
            self.stats_label.grid(row=count, sticky=item[2], padx=60)
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
        self.line_label.grid(row=8)

        # move round data label
        round_data_label = stats_label_ref_list[6]
        round_data_label.grid(row=9)

        # overload notice
        self.overload_label = Label(self.stats_frame,
                                    text=f"Showing 3 most recent rounds - 3/{rounds_played}\n rounds shown, please "
                                         "export to file\nto see other rounds", font=("Arial", "14"), justify="left",
                                    background="#E3E1FF", padx=30, pady=15)
        self.overload_label.grid(row=10, pady=7)

        background = "#E3E1FF"
        if len(round_data) <= 3:
            background = "#FFFFFF"
            self.overload_label.destroy()

        # create a label to hold the past 3 rounds' data
        self.data_label = Label(self.stats_frame, text=data_string, font=("Arial", "14"), justify="left",
                                padx=30, pady=5, bg=background)
        self.data_label.grid(row=11, padx=20, pady=8)

        self.buttons_frame = Frame(self.stats_frame, bg="#FFF2CC")
        self.buttons_frame.grid(row=12, pady=5)

        # buttons info list (text | bg | width | command)
        buttons_strings = [
            ["Export to File", "#F0A30A", 15, partial(self.export_to_file, export_strings)],
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
    def export_to_file(self, strings):
        """
        export data to a text file
        """

        # **** Get current date for heading and filename
        today = date.today()

        # get day, month and year as individual strings
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        file_name = f"god_quiz_{year}_{month}_{day}"
        write_to = f"{file_name}.txt"

        with open(write_to, "w") as text_file:
            text_file.write("============= God Quiz =============\n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")
            text_file.write(f"{strings[0]}\n")
            text_file.write(f"{strings[1]}\n")
            text_file.write(f"{strings[2]}\n")
            text_file.write(f"{strings[3]}\n")
            text_file.write("-" * 25)
            text_file.write(strings[4])
            text_file.write("=" * 36)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
