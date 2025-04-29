<p align="center">
  <img src="https://github.com/user-attachments/assets/2085dbaf-740b-4e6f-845b-8fb5862bee64" width="300" height="200">
</p>

# Kill Tracker Final Project

## Project Overview

For my final project, I created an app designed to be used in basketball games to help coaches track defensive performance. Specifically, it tracks **kills**—which, in basketball terms, are defined as **three consecutive defensive stops**.

At Huntington Women's Basketball, our goal was to reach **10 kills per game**. Previously, we tracked this using paper, which was often messy and required manually counting defensive stops. This app simplifies the process by:

- Automatically tracking stops and kills in real time.
- Activating a "kill" once three consecutive stops are recorded.
- Displaying kills per quarter.
- Providing a game summary with total stops and kills after saving.

This app is intended for basketball coaches at all levels who want an organized way to monitor defensive effiency during games.

## Design & Architecture

I wanted this app to be very simple. When I first created the app, I was looking for ways to just track the kills. I had everything in one container tracking the amount of kills. As I continued, I realized that I wanted to split it up by quarters to make it easier and I wanted only 3 simple buttons to be able to add stops, add a kill, or reset because they scored. 

To build this app, I used a traditional MVC format. For the model, I had game_stats.py which is where the game data and logic is stored. The classes that are in this file are SavedGame and GameStats. For the view, I used kill_tracker_view.py. The controller is what coordinates the logic and updates the model. The main class that is used in here is KillTrackerController. 


classDiagram
    %% Model Classes
    class GameStats {
        +q1_kills: int
        +q2_kills: int
        +q3_kills: int
        +q4_kills: int
        +total_stops: int
        +is_kill_active: bool
        +consecutive_stops: int
        +total_kills() int
        +add_stop()
        +add_kill(quarter)
        +reset_stops()
        +reset_all()
    }

    class SavedGame {
        +opponent: str
        +date: datetime
        +stats: GameStats
    }

    %% Controller Class
    class KillTrackerController {
        -_game_stats: GameStats
        -_current_quarter: str
        -_saved_games: list[SavedGame]
        +game_stats() GameStats
        +current_quarter() str
        +is_kill_active() bool
        +consecutive_stops() int
        +saved_games() list[SavedGame]
        +change_quarter(quarter)
        +add_stop()
        +add_kill()
        +reset_stops()
        +reset_all()
        +save_game(opponent, date)
        +save_to_file(filename)
        +load_from_file(filename)
    }

    %% View Classes
    class KillTrackerView {
        -root: tk.Tk
        -controller: KillTrackerController
        +create_widgets()
        +update_display()
        +on_quarter_change()
        +add_stop()
        +add_kill()
        +reset_stops()
        +save_game()
        +view_saved_games()
        +save_to_file()
        +load_from_file()
    }

    class ConsoleView {
        -controller: KillTrackerController
        +run()
        +_display_menu()
        +_change_quarter()
        +_save_game()
        +_view_saved_games()
        +_save_to_file()
        +_load_from_file()
    }

    class GameHistoryScreen {
        +display(game)
    }

    %% Relationships
    KillTrackerController --> GameStats: Manages
    KillTrackerController --> SavedGame: Stores
    KillTrackerView --> KillTrackerController: Uses
    ConsoleView --> KillTrackerController: Uses
    GameHistoryScreen --> SavedGame: Displays

    note for KillTrackerController "Mediates between Views and Model\nHandles all business logic\nManages game state persistence"
    note for GameStats "Core game state\nTracks kills and stops\nManages kill activation logic"
    note for KillTrackerView "GUI Interface\nTkinter implementation\nDelegates actions to controller"
    note for ConsoleView "Text Interface\nConsole implementation\nAlternative to GUI"
## App Instructions 


## Challenges, Role of AI, Insights 

## Next Steps 




  



