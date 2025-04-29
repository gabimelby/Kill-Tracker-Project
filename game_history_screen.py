class GameHistoryScreen:
    @staticmethod
    def display(game):
        print(f"\nGame vs {game.opponent}")
        print(f"Date: {game.date.strftime('%Y-%m-%d')}")
        print(f"Q1 Kills: {game.stats.q1_kills}")
        print(f"Q2 Kills: {game.stats.q2_kills}")
        print(f"Q3 Kills: {game.stats.q3_kills}")
        print(f"Q4 Kills: {game.stats.q4_kills}")
        print("-" * 20)
        print(f"Total Kills: {game.stats.total_kills}")
        print(f"Total Stops: {game.stats.total_stops}")
        input("\nPress Enter to return...")