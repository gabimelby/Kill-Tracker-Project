# Author: Gabi Melby
#
# Date: 4/30/2025
#
# Description: Create an app that tracks the amount
# of kills in a basketball game and saves as a json file.
#
#Used ChatGPT, DeepSeek, GeeksForGeeks, and class assignments. 
# -------------------------------------------------------


import tkinter as tk
from kill_tracker_controller import KillTrackerController
from kill_tracker_view import KillTrackerView 

def run_gui(): #runs the actual app 
    root = tk.Tk()
    controller = KillTrackerController()
    app = KillTrackerView(root, controller)
    root.mainloop()

 

if __name__ == "__main__":
    # To run the GUI version:
    run_gui()
