# Number -> move name.
# We use numbers so the Player's input is simple to type.
CHOICE_NAMES = {
    1: "Rock",
    2: "Paper",
    3: "Scissors",
}

# How many rounds have been played so far.
TurnNum = 0

# Last move the Player played (1, 2, or 3).
# Used to detect streaks, like Rock-Rock-Rock (see SameChoiceStreak).
LastPlayerChoice = 0

# The move number the AI picked this round.
AIChoice = 0

# How many times in a row has the Player chosen the same move?
SameChoiceStreak = 0

# WEIGHTING IDEA (simple version):
# 1) Each move has an Influence score. We start all at 1.0 so the AI begins fair.
# 2) When the Player picks a move, that move's Influence goes up.
# 3) If the Player repeats the same move many times, we add a smaller amount each time.
# 4) We convert Influence into Weight percentages that add up to 100.
# 5) The AI uses counter-weights:
#    - The Player choosing "Rock" raises the weight (and the chance) of the AI choosing "Paper"
#    - The Player choosing "Paper" raises the weight (and the chance) of the AI choosing "Scissors"
#    - The Player choosing "Scissors" the weight (and the chance) of the raises AI choosing "Rock"

# Rock tracking.
# Influence is like a score used to build AI weights.
RockChoiceNum = 0 # How many times has the Player chosen Rock?
RockInfluence = 1.0
RockWeight = 100 / 3 # AI chooses Rock against the Player's Scissors

# Paper tracking.
PaperChoiceNum = 0 # How many times has the Player chosen Paper?
PaperInfluence = 1.0
PaperWeight = 100 / 3 # AI chooses Paper against the Player's Rock

# Scissors tracking.
ScissorsChoiceNum = 0 # How many times has the Player chosen Scissors?
ScissorsInfluence = 1.0
ScissorsWeight = 100 / 3 # AI chooses Scissors against the Player's Paper

# If set to "True", this shows how the AI makes its decisions.
ShowAIStats = False

# Show the current counts and the AI's chances.
def stats():
    # These numbers help us see what the AI has learned so far.
    if ShowAIStats == True:
        print(f"\n-  Stats After {TurnNum} Turn(s)  -")
        print(
                "\nRock Stats:\n"
                f"The Player Chose 'Rock' {RockChoiceNum} Times\n"
                f"- Rock's Influence: {RockInfluence}\n"
                f"- AI Choosing 'Paper' Chance (Weight): {PaperWeight}%\n"
            )
        print(
                "Paper Stats:\n"
                f"The Player Chose 'Paper' {PaperChoiceNum} Times\n"
                f"- Paper's Influence: {PaperInfluence}\n"
                f"- AI Choosing 'Scissors' Chance (Weight): {ScissorsWeight}%\n"
            )
        print(
                "Scissors Stats:\n"
                f"The Player Chose 'Scissors' {ScissorsChoiceNum} Times\n"
                f"- Scissors's Influence: {ScissorsInfluence}\n"
                f"- AI Choosing 'Rock' Chance (Weight): {RockWeight}%"
            )