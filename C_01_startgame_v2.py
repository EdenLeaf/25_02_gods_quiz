from tkinter import *
from functools import partial  # to prevent unwanted windows


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
                        "need to choose which of those 4 gods corresponds to that domain. \n\n"
                        "To begin, please state how many rounds you want to play and then press play.")

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
                               fg=item[2], wraplength=350, justify="left",
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

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "18", "bold"), width=10, bg="#DBDBDB",
                                      justify="center")
        self.num_rounds_entry.grid(row=0, column=0, padx=5, pady=10)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  bg="#E1D5E7", text="Play", width=10, command=partial(self.check_rounds, "Normal"))
        self.play_button.grid(row=0, column=1)

        # Create endless button...
        self.endless_button = Button(self.endless_frame, font=("Arial", "16", "bold"),
                                  bg="#76608A", fg="#FFFFFF", text="Endless Mode", width=21,
                                  command=partial(self.check_rounds, "Endless"))
        self.endless_button.grid(row=0, column=0)

    def check_rounds(self, round_mode):
        """
        Checks users have entered 1 or more rounds
        """

        # retrieve round wanted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than 0."
        has_errors = "no"

        if round_mode == "Normal":
            # checks that number of rounds wanted is more than 0
            try:
                rounds_wanted = int(rounds_wanted)
                if rounds_wanted > 0:
                    # invoke PLay Class (and take across number of rounds)
                    Play(rounds_wanted)
                    # Hide root window (ie: hide rounds choice window
                    self.choose_label.config(text="How many rounds do you want to play?")
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
            rounds_wanted = -1
            # invoke PLay Class (and take across number of rounds)
            Play(rounds_wanted)
            # Hide root window (ie: hide rounds choice window
            self.choose_label.config(text="How many rounds do you want to play?")
            self.num_rounds_entry.delete(0, END)
            root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        if how_many > 0:
            heading_text = f"Round 0 of {how_many}"
        else:
            heading_text = "Round 0"

        self.game_heading_label = Label(self.game_frame, text=heading_text,
                                        font=("Arial", "16", "bold"))
        self.game_heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game", font=("Arial", "16", "bold"),
                                      fg="#FFFFFF", bg="#990000",
                                      width="10", command=self.close_play)
        self.end_game_button.grid(row=1)

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
