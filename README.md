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

## App Instructions 


## Challenges, Role of AI, Insights 

## Next Steps 




  



