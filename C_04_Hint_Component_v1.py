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

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Colour Quest",
                                   font=("Arial", "16", "bold"), padx=5,
                                   pady=5)
        self.heading_label.grid(row=0)

        self.hints_button = Button(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Hints", width=15, fg="#FFFFFF", bg="#60A917",
                                   padx=10, pady=10, command=self.to_hints)
        self.hints_button.grid(row=1)

    def to_hints(self):
        """
        Displays hints for playing game
        :return:
        """
        DisplayHints(self)


class DisplayHints:
    """
    Displays hints for Colour Quest Game
    """

    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#D5E8D4"
        self.hint_box = Toplevel()

        # disable hint button
        partner.hints_button.config(state=DISABLED)

        # If user press cross at top, closes hint and 'releases' hint button
        self.hint_box.protocol('WM_DELETE_WINDOW', partial(self.close_hint, partner))

        self.hint_frame = Frame(self.hint_box, width=300,
                                height=200)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame,
                                        text="Hints",
                                        font=("Arial", "14", "bold"), bg="#FFFFFF")
        self.hint_heading_label.grid(row=0)

        hint_text = "The background colour of the question is relates to the mythology that the correct god is from:\n" \
                    "Red = Roman\n " \
                    "Blue = Greek\n " \
                    "This means that if the game asks you who the god of the sea is, you know that the answer would " \
                    "be Poseidon for a blue background, and Neptune for a red background."

        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text, wraplength=350,
                                     justify="left")
        self.hint_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hint_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#60A917", fg="#FFFFFF",
                                     command=partial(self.close_hint, partner))
        self.dismiss_button.grid(row=2, pady=10, padx=10)

        # List and loop to set background colour on everything except the buttons
        recolour_list = [self.hint_frame, self.hint_heading_label, self.hint_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_hint(self, partner):
        """
        Closes hint dialogue box (and enables hint button)
        """
        # put hint button back to normal...
        partner.hints_button.config(state=NORMAL)
        self.hint_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()