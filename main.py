import tkinter as tk
from kill_tracker_controller import KillTrackerController
from kill_tracker_view import KillTrackerView, ConsoleView

def run_gui():
    root = tk.Tk()
    controller = KillTrackerController()
    app = KillTrackerView(root, controller)
    root.mainloop()

def run_console():
    controller = KillTrackerController()
    view = ConsoleView(controller)
    view.run()

if __name__ == "__main__":
    # To run the GUI version:
    run_gui()
    
    # To run the console version instead:
    # run_console()