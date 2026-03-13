import time
import config

config.ShowAIStats = True # Change to "True" to show how the AI makes its decisions!

# Work out who won this round.
def round_result(player_choice, ai_choice):
    # Same move means no winner.
    if player_choice == ai_choice:
        return "Draw"

    # These are the three winning combinations for the Player.
    # If one matches, the Player wins.
    if (
        (player_choice == 1 and ai_choice == 3)
        or (player_choice == 2 and ai_choice == 1)
        or (player_choice == 3 and ai_choice == 2)
    ):
        return "Win"

    # If it was not a draw and not the Player's win, the Player lost.
    return "Lost"


# Says "Rock, Paper, Scissors" to the player.
def countdown(seconds):
    sequence = ["Rock", "Paper", "Scissors"]

    # Split the total time equally across the three words.
    step_delay = seconds / len(sequence)

    print()
    for word in sequence:
        print(f"{word}...")
        time.sleep(step_delay)


# Main game loop.
def main():
    while True:
        config.stats() # Show the stats!
        
        print(f"\n------------------")
        print(f"\n(Turn {config.TurnNum + 1})")

        # Ask for input until we get a number.
        try:
            player_choice = int(input("\nEnter 1 for Rock, 2 for Paper, 3 for Scissors: "))
        except ValueError:
            print("\nPlease enter a number: 1, 2, or 3.")
            continue

        # Make sure the number is one of our three valid choices.
        if player_choice not in config.CHOICE_NAMES:
            print("\nPlease enter 1, 2, or 3.")
            continue

        # Build suspense, then let the AI decide.
        countdown(seconds=2)
        
        from ai_package import ai
        ai_choice = ai.decider(player_choice)
        
        result = round_result(player_choice, ai_choice)

        # Show round summary in one sentence.
        print(f"\nYou chose: {config.CHOICE_NAMES[player_choice]}, the AI chose: {config.CHOICE_NAMES[ai_choice]}. You {result}!")

if __name__ == "__main__":
    main()