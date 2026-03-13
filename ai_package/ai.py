import random
import config

# Pick the AI's move.
# On the first round, we force a fair random pick (1 in 3).
# After that, we use the move(s) with the highest weight.
def AIDecision(force_random=False):
    # First round: do not use learning yet.
    # Pick a completely random move so everyone starts fairly.
    if force_random:
        config.AIChoice = random.randint(1, 3)
        return config.AIChoice

    # Put the three weights in one place so we can compare them.
    weighted_choices = {
        1: config.RockWeight,
        2: config.PaperWeight,
        3: config.ScissorsWeight,
    }

    # Find the biggest weight.
    highest_weight = max(weighted_choices.values())

    # Collect every move tied for biggest weight.
    # This means if two moves are equal-best, both are kept.
    best_choices = [
        choice for choice, weight in weighted_choices.items()
        if weight == highest_weight
    ]

    # Pick one from the best options.
    # If there is a tie, this randomly chooses between tied moves.
    config.AIChoice = random.choice(best_choices)

    return config.AIChoice


# Learn from the Player's latest move, then return the AI's move.
def decider(player_choice):
    # Turn 0 in code is Turn 1 on screen.
    # We keep the first turn fully random so the game starts fair.
    is_first_turn = config.TurnNum == 0

    config.TurnNum += 1

    # Count what the Player picked this turn.
    # These totals are useful for showing stats.
    if player_choice == 1:
        config.RockChoiceNum += 1
    elif player_choice == 2:
        config.PaperChoiceNum += 1
    elif player_choice == 3:
        config.ScissorsChoiceNum += 1

    # Track streaks so repeating the same move has smaller effect over time.
    # Example: "Rock", "Rock", "Rock" builds a streak of 3.
    if player_choice == config.LastPlayerChoice:
        config.SameChoiceStreak += 1
    else:
        config.LastPlayerChoice = player_choice
        config.SameChoiceStreak = 1

    # Bigger streak -> smaller extra learning from that repeated choice.
    # This helps stop easy "spamming" tricks.
    streak_damping = 1 / (1 + (config.SameChoiceStreak - 1) * 0.5)

    # Example extra learning for repeated same move:
    # streak 1 -> +1.00, streak 2 -> +0.67, streak 3 -> +0.50, streak 4 -> +0.40
    
    # Add the damped learning to the move the Player just played.
    if player_choice == 1:
        config.RockInfluence += streak_damping
    elif player_choice == 2:
        config.PaperInfluence += streak_damping
    elif player_choice == 3:
        config.ScissorsInfluence += streak_damping

    # Turn influence scores into percentages (weights) that add up to 100.
    total_influence = config.RockInfluence + config.PaperInfluence + config.ScissorsInfluence
    
    config.RockWeight = (config.ScissorsInfluence / total_influence) * 100 # The AI's "Rock" should counter the Player's "Scissors".
    
    config.PaperWeight = (config.RockInfluence / total_influence) * 100 # The AI's "Paper" should counter the Player's "Rock".
    
    config.ScissorsWeight = (config.PaperInfluence / total_influence) * 100 # The AI's "Scissors" should counter the Player's "Paper".
    
    # Worked example:
    # if influences are Rock=3, Paper=1, Scissors=2 then total=6.
    # The AI's "Paper" weight = "Rock" influence / total = 3/6 = 50%.
    # The AI's "Scissors" weight = "Paper" influence / total = 1/6 = 16.7%.
    # The AI's "Rock" weight = "Scissors" influence / total = 2/6 = 33.3%.
    
    return AIDecision(force_random=is_first_turn)