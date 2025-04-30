# Author: Gabi Melby
#
# Date: 4/30/2025
#
# Description: This is the view file. Creates the style of
# the app, the widgets, showing the saving and saved games,
# collects user input, and presents the data.
#
#Used ChatGPT and DeepSeek. Prompt: convert all the dart/flutter
# over to Python for my View file. 
# -------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class KillTrackerView:
    #use a mixture of pack and grid format to help me have a nice GUI application
    def __init__(self, root, controller): #Constructor!!
        self.root = root
        self.controller = controller
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=10)
        self.style.configure('TButton', padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Active.TLabel', foreground='green', font=('Arial', 12, 'bold'))
        self.style.configure('Inactive.TLabel', foreground='red', font=('Arial', 12, 'bold'))
        
        self.create_widgets()
        self.update_display()
    
    #For the widgets, used ChatGPT by uploading a sketch of what I wanted
    # and it gave me this!
    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
        # Kills display
        kills_frame = ttk.LabelFrame(self.main_frame)
        kills_frame.pack(fill=tk.X, padx=5, pady=5)
    
        # title styling for "Kills by Quarter"
        kills_title = ttk.Label(kills_frame, text="Kills by Quarter", font=('Arial', 16, 'bold'), anchor='center')
        kills_title.pack(pady=5)
    
        self.q_labels = {}
        kill_grid_frame = ttk.Frame(kills_frame)
        kill_grid_frame.pack()
        for i, q in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
            frame = ttk.Frame(kill_grid_frame)
            frame.grid(row=0, column=i, padx=10, pady=5)
            ttk.Label(frame, text=q).pack()
            self.q_labels[q] = ttk.Label(frame, text="0", font=('Arial', 14, 'bold'))
            self.q_labels[q].pack()
    
        # Quarter selector
        quarter_frame = ttk.LabelFrame(self.main_frame, text="Current Quarter")
        quarter_frame.pack(fill=tk.X, padx=5, pady=5)
    
        self.quarter_var = tk.StringVar(value=self.controller.current_quarter)
        for q in ['Q1', 'Q2', 'Q3', 'Q4']:
            ttk.Radiobutton(
                quarter_frame, 
                text=q, 
                variable=self.quarter_var, 
                value=q,
                command=self.on_quarter_change
            ).pack(side=tk.LEFT, padx=5)
    
        # Stops display
        stops_frame = ttk.LabelFrame(self.main_frame, text="Stops")
        stops_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(stops_frame, text="Total Stops:").pack(side=tk.LEFT, padx=5)
        self.total_stops_label = ttk.Label(stops_frame, text="0", font=('Arial', 12))
        self.total_stops_label.pack(side=tk.LEFT, padx=5)
    
        ttk.Label(stops_frame, text="Consecutive Stops:").pack(side=tk.LEFT, padx=5)
        self.consecutive_stops_label = ttk.Label(stops_frame, text="0", font=('Arial', 12))
        self.consecutive_stops_label.pack(side=tk.LEFT, padx=5)
    
        # Kill status
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Kill Status")
        self.status_frame.pack(fill=tk.X, padx=5, pady=5)
        self.status_label = ttk.Label(self.status_frame, text="No Kill Active")
        self.status_label.pack()
    
        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
    
        ttk.Button(
            button_frame, 
            text="Add Stop", 
            command=self.add_stop
        ).pack(side=tk.LEFT, padx=5, expand=True)
    
        ttk.Button(
            button_frame, 
            text="Scored (Reset Stops)", 
            command=self.reset_stops
        ).pack(side=tk.LEFT, padx=5, expand=True)
    
        ttk.Button(
            button_frame, 
            text="Add Kill", 
            command=self.add_kill
        ).pack(side=tk.LEFT, padx=5, expand=True)
    
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
    
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Save Game", command=self.save_game)
        game_menu.add_command(label="View Saved Games", command=self.view_saved_games)
        game_menu.add_separator()
        game_menu.add_command(label="Reset All", command=self.reset_all)
        game_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        # Add these commands to the game_menu
        game_menu.add_command(label="Save to File", command=self.save_to_file)
        game_menu.add_command(label="Load from File", command=self.load_from_file)
        game_menu.add_separator()
        
    #got this from assignment p5 for JSON
    def save_to_file(self):
        filename = simpledialog.askstring("Save to File", "Enter filename (default: basketball_stats.txt):")
        if filename is None:  # User cancelled
            return
    
        if not filename:
            filename = "basketball_stats.txt"
    
        try:
            self.controller.save_to_file(filename)
            messagebox.showinfo("Success", f"Game data saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    #Loads in the file and data
    def load_from_file(self):
        filename = simpledialog.askstring("Load from File", "Enter filename (default: basketball_stats.txt):")
        if filename is None:  # User cancelled
            return
    
        if not filename:
            filename = "basketball_stats.txt"
    
        if self.controller.load_from_file(filename):
            self.quarter_var.set(self.controller.current_quarter)
            self.update_display()
            messagebox.showinfo("Success", f"Game data loaded from {filename}")
        else:
            messagebox.showerror("Error", "Failed to load file or file not found")
    
    def on_quarter_change(self):
        self.controller.change_quarter(self.quarter_var.get())
        self.update_display()
    
    def add_stop(self):
        self.controller.add_stop()
        self.update_display()
    
    def add_kill(self):
        self.controller.add_kill()
        self.update_display()
    
    def reset_stops(self):
        self.controller.reset_stops()
        self.update_display()
    
    def reset_all(self):
        self.controller.reset_all()
        self.quarter_var.set('Q1')
        self.update_display()
    
    def save_game(self):
        opponent = simpledialog.askstring("Save Game", "Enter opponent name:")
        if not opponent:
            return
        
        date_str = simpledialog.askstring("Save Game", "Enter date (YYYY-MM-DD):")
        try:
            if date_str:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date = datetime.now().date()
            
            self.controller.save_game(opponent, date)
            messagebox.showinfo("Success", "Game saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
    
    def view_saved_games(self):
        if not self.controller.saved_games:
            messagebox.showinfo("Saved Games", "No games saved yet.")
            return
        
        top = tk.Toplevel(self.root)
        top.title("Saved Games")
        #these are the widgets for the saved Game Box
        #It's a list of all the saved games and the view shows the date, total kills, total stops 
        tree = ttk.Treeview(top, columns=('date', 'kills', 'stops'), show='headings')
        tree.heading('#0', text='Opponent')
        tree.heading('date', text='Date')
        tree.heading('kills', text='Total Kills')
        tree.heading('stops', text='Total Stops')
        #Got help for this by ChatGPT and DeepSeek. 
        for game in self.controller.saved_games:
            tree.insert('', 'end', text=game.opponent, 
                        values=(game.date.strftime('%Y-%m-%d'), 
                                game.stats.total_kills, 
                                game.stats.total_stops))
        #double click on the game and it shows all the game details 
        tree.pack(fill=tk.BOTH, expand=True)
        
        #This method shows that double click on the saved game to show the details
        #got this from DeepSeek
        def on_item_double_click(event):
            item = tree.selection()[0]
            opponent = tree.item(item, 'text')
            game = next(g for g in self.controller.saved_games if g.opponent == opponent)
            self.show_game_details(game)
        
        tree.bind('<Double-1>', on_item_double_click)
    
    def show_game_details(self, game):
        top = tk.Toplevel(self.root)
        top.title(f"Game vs {game.opponent}")
        
        frame = ttk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text=f"Date: {game.date.strftime('%Y-%m-%d')}", 
                 font=('Arial', 12)).pack(pady=5)
        
        # Quarter stats
        quarter_frame = ttk.Frame(frame)
        quarter_frame.pack(pady=10)
        
        ttk.Label(quarter_frame, text="Quarter", style='Header.TLabel').grid(row=0, column=0, padx=10)
        ttk.Label(quarter_frame, text="Kills", style='Header.TLabel').grid(row=0, column=1, padx=10)
        
        for i, q in enumerate(['Q1', 'Q2', 'Q3', 'Q4'], 1):
            ttk.Label(quarter_frame, text=q).grid(row=i, column=0, padx=10, pady=2)
            kills = getattr(game.stats, f'{q.lower()}_kills')
            ttk.Label(quarter_frame, text=str(kills)).grid(row=i, column=1, padx=10, pady=2)
        
        # Totals
        ttk.Label(frame, text=f"Total Kills: {game.stats.total_kills}", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
        ttk.Label(frame, text=f"Total Stops: {game.stats.total_stops}", 
                 font=('Arial', 12)).pack(pady=5)
    
    def update_display(self):
        # Update quarter kills
        for q in ['Q1', 'Q2', 'Q3', 'Q4']:
            kills = getattr(self.controller.game_stats, f'{q.lower()}_kills')
            self.q_labels[q].config(text=str(kills))
        
        # Update stops
        self.total_stops_label.config(text=str(self.controller.game_stats.total_stops))
        self.consecutive_stops_label.config(text=str(self.controller.consecutive_stops))
        
        # Update status
        if self.controller.is_kill_active:
            self.status_label.config(text="KILL ACTIVE!", style='Active.TLabel')
            self.status_frame.configure(style='Active.TFrame')
        else:
            self.status_label.config(text="No Kill Active", style='Inactive.TLabel')
            self.status_frame.configure(style='Inactive.TFrame')


