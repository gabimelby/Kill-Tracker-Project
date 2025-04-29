import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class KillTrackerView:
    def __init__(self, root, controller):
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
    
    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
        # Kills display
        kills_frame = ttk.LabelFrame(self.main_frame)
        kills_frame.pack(fill=tk.X, padx=5, pady=5)
    
        # Custom title styling for "Kills by Quarter"
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
        # ... (rest of existing code)
        
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
        
        tree = ttk.Treeview(top, columns=('date', 'kills', 'stops'), show='headings')
        tree.heading('#0', text='Opponent')
        tree.heading('date', text='Date')
        tree.heading('kills', text='Total Kills')
        tree.heading('stops', text='Total Stops')
        
        for game in self.controller.saved_games:
            tree.insert('', 'end', text=game.opponent, 
                        values=(game.date.strftime('%Y-%m-%d'), 
                                game.stats.total_kills, 
                                game.stats.total_stops))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
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


class ConsoleView:
    def __init__(self, controller):
        self.controller = controller
    
    def run(self):
        while True:
            self._display_menu()
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self._change_quarter()
            elif choice == '2':
                self.controller.add_stop()
            elif choice == '3':
                self.controller.add_kill()
            elif choice == '4':
                self.controller.reset_stops()
            elif choice == '5':
                self._save_game()
            elif choice == '6':
                self.controller.reset_all()
            elif choice == '7':
                self._view_saved_games()
            elif choice == '8':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def _display_menu(self):
        print("\n=== Basketball Kill Tracker ===")
        print(f"Current Quarter: {self.controller.current_quarter}")
        print(f"Kill Status: {'ACTIVE!' if self.controller.is_kill_active else 'Not Active'}")
        print(f"Consecutive Stops: {self.controller.consecutive_stops}")
        print(f"Total Stops: {self.controller.game_stats.total_stops}")
        print("\nQuarter Kills:")
        print(f"Q1: {self.controller.game_stats.q1_kills} | Q2: {self.controller.game_stats.q2_kills} | "
              f"Q3: {self.controller.game_stats.q3_kills} | Q4: {self.controller.game_stats.q4_kills}")
        print("\nMenu:")
        print("1. Change Quarter")
        print("2. Add Stop")
        print("3. Add Kill")
        print("4. Reset Stops (Scored)")
        print("5. Save Game")
        print("6. Reset All")
        print("7. View Saved Games")
        print("8. Exit")

    def _change_quarter(self):
        print("\nSelect Quarter:")
        print("1. Q1")
        print("2. Q2")
        print("3. Q3")
        print("4. Q4")
        q_choice = input("Enter quarter choice (1-4): ")
        
        if q_choice == '1':
            self.controller.change_quarter('Q1')
        elif q_choice == '2':
            self.controller.change_quarter('Q2')
        elif q_choice == '3':
            self.controller.change_quarter('Q3')
        elif q_choice == '4':
            self.controller.change_quarter('Q4')
        else:
            print("Invalid choice. Quarter not changed.")

    def _save_game(self):
        opponent = input("Enter opponent name: ")
        date_str = input("Enter date (YYYY-MM-DD, leave blank for today): ")
        
        try:
            if date_str:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date = datetime.now().date()
                
            self.controller.save_game(opponent, date)
            print("Game saved successfully!")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    def _view_saved_games(self):
        if not self.controller.saved_games:
            print("\nNo saved games yet.")
            return
            
        print("\nSaved Games:")
        for i, game in enumerate(self.controller.saved_games, 1):
            print(f"{i}. vs {game.opponent} on {game.date.strftime('%Y-%m-%d')} - "
                  f"{game.stats.total_kills} kills, {game.stats.total_stops} stops")
        
        choice = input("\nEnter game number to view details or any key to return: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(self.controller.saved_games):
                self._display_game_details(self.controller.saved_games[index])
        except ValueError:
            pass

    def _display_game_details(self, game):
        print(f"\nGame Details vs {game.opponent}")
        print(f"Date: {game.date.strftime('%Y-%m-%d')}")
        print(f"Q1 Kills: {game.stats.q1_kills}")
        print(f"Q2 Kills: {game.stats.q2_kills}")
        print(f"Q3 Kills: {game.stats.q3_kills}")
        print(f"Q4 Kills: {game.stats.q4_kills}")
        print(f"Total Kills: {game.stats.total_kills}")
        print(f"Total Stops: {game.stats.total_stops}")
        input("\nPress Enter to return...")
    # Add to ConsoleView class in kill_tracker_view.py
    def _display_menu(self):
        # ... (existing menu items)
        print("9. Save to File")
        print("10. Load from File")
        print("8. Exit")  # Make sure this is the last option

    def run(self):
        while True:
        # ... (existing choices)
            if choice == '9':
                self._save_to_file()
            elif choice == '10':
                self._load_from_file()
            elif choice == '8':
                print("Exiting...")
                break
        # ... (rest of existing code)

    def _save_to_file(self):
        filename = input("Enter filename (default: basketball_stats.txt): ").strip()
        if not filename:
            filename = "basketball_stats.txt"
    
        try:
            self.controller.save_to_file(filename)
            print(f"Game data saved to {filename}")
        except Exception as e:
            print(f"Failed to save file: {str(e)}")

    def _load_from_file(self):
        filename = input("Enter filename (default: basketball_stats.txt): ").strip()
        if not filename:
            filename = "basketball_stats.txt"
    
        if self.controller.load_from_file(filename):
            print(f"Game data loaded from {filename}")
        else:
            print("Failed to load file or file not found")