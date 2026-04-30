from microbit import display, button_a, button_b, sleep
import random

CHOICE_NAMES = {1: "Rock", 2: "Paper", 3: "Scissors"} # See README.md (1)

# See README.md (2)
RoundNum = 0
LastPlayerMove = 0
AIMove = 0
SameMoveStreak = 1

PlayerWins = 0
AIWins = 0
Draws = 0

# See README.md (3)
RockMoveNum = 0
RockInfluence = 1.0
RockWeight = 100 / 3

PaperMoveNum = 0
PaperInfluence = 1.0
PaperWeight = 100 / 3

ScissorsMoveNum = 0
ScissorsInfluence = 1.0
ScissorsWeight = 100 / 3

ShowAIStats = False


# See README.md (5)
def stats():
    print("\n-  Stats After", RoundNum, "Round(s)  -")
    print(
            "\nRock Stats:\n"
            "The Player Chose 'Rock'", RockMoveNum, "Times\n"
            "- Rock's Influence:", RockInfluence, "\n"
            "- Chance (Weight) of AI Choosing 'Paper':", PaperWeight, "%\n"
        )
    print(
            "Paper Stats:\n"
            "The Player Chose 'Paper'", PaperMoveNum, "Times\n"
            "- Paper's Influence:", PaperInfluence , "\n"
            "- Chance (Weight) of AI Choosing 'Scissors':", ScissorsWeight, "%\n"
        )
    print(
            "Scissors Stats:\n"
            "The Player Chose 'Scissors'", ScissorsMoveNum, " Times\n"
            "- Scissors's Influence:", ScissorsInfluence, "\n"
            "- Chance (Weight) of AI Choosing 'Rock':", RockWeight, "%\n"
        )


# See README.md (6)
def AIDecision(force_random=False):
    global AIMove
    
    # See README.md (6-1)
    if force_random:
        AIMove = random.randint(1, 3)
        return AIMove

    # See README.md (6-2)
    weighted_choices = {1: RockWeight, 2: PaperWeight, 3: ScissorsWeight}
    highest_weight = max(weighted_choices.values())
    best_choices = [choice for choice, weight in weighted_choices.items() if weight == highest_weight]
    if len(best_choices) == 1:
        AI = best_choices[0]
    else:
        # See README.md (6-3)
        idx = random.randint(0, len(best_choices) - 1)
        AI = best_choices[idx]

    AIMove = AI
    return AIMove


def _weight_calc(player_choice, damping=True): # STUDENTS COULD CHANGE THIS FUNCTION AND SEE HOW THE WAY THE AI PLAYS CHANGES
    global RockInfluence, RockWeight
    global PaperInfluence, PaperWeight
    global ScissorsInfluence, ScissorsWeight
    
    # See README.md (7-3a)
    if damping==True:
        streak_damping = 1 / (((SameMoveStreak - 1) * 0.5) + 1)
    else:
        streak_damping = 1
    
    # See README.md (7-3b)
    if player_choice == 1:
        RockInfluence += streak_damping
    elif player_choice == 2:
        PaperInfluence += streak_damping
    elif player_choice == 3:
        ScissorsInfluence += streak_damping
    
    # See README.md (7-4a)
    total_influence = RockInfluence + PaperInfluence + ScissorsInfluence
    if total_influence == 0:
        total_influence = 1
    
    # See README.md (7-4b)
    RockWeight = (ScissorsInfluence / total_influence) * 100
    PaperWeight = (RockInfluence / total_influence) * 100
    ScissorsWeight = (PaperInfluence / total_influence) * 100

    # See README.md (7-4c)
    globals()['RockWeight'] = RockWeight
    globals()['PaperWeight'] = PaperWeight
    globals()['ScissorsWeight'] = ScissorsWeight


# See README.md (7)
def _update_weights(player_choice):
    global RoundNum, LastPlayerMove, SameMoveStreak
    global RockMoveNum, PaperMoveNum, ScissorsMoveNum
    
    RoundNum += 1

    # See README.md (7-1)
    if player_choice == 1:
        RockMoveNum += 1
    elif player_choice == 2:
        PaperMoveNum += 1
    elif player_choice == 3:
        ScissorsMoveNum += 1

    if player_choice == LastPlayerMove: # See README.md (7-2a)
        SameMoveStreak += 1
    else:
        # See README.md (7-2b)
        LastPlayerMove = player_choice
        SameMoveStreak = 1

    _weight_calc(player_choice, damping=True)


PROMPTS = ("A=R", "B=P", "A+B=S")
# helper: manual scroll + poll (avoid wait=False rendering issues)
def _poll_buttons_debounced():
    if button_a.is_pressed() and button_b.is_pressed():
        while button_a.is_pressed() or button_b.is_pressed():
            sleep(100)
        display.clear()
        return 3
    if button_a.is_pressed():
        while button_a.is_pressed():
            sleep(100)
        display.clear()
        return 1
    if button_b.is_pressed():
        while button_b.is_pressed():
            sleep(100)
        display.clear()
        return 2
    return None


def _manual_scroll_and_poll(msg, char_delay=300, poll_interval=50):
    """Show message one character at a time and poll buttons between frames.

    Returns 1/2/3 if a button combo is detected, otherwise None.
    """
    padding = "     "
    text = msg + padding
    for ch in text:
        display.show(ch)
        elapsed = 0
        while elapsed < char_delay:
            choice = _poll_buttons_debounced()
            if choice is not None:
                return choice
            sleep(poll_interval)
            elapsed += poll_interval
    return None


# See README.md (4)
def main():
    global PlayerWins, AIWins, Draws, ShowAIStats
    ShowAIStats = True
    
    seconds = 1.2

    while True:
        print()
        print("----------------------------------------")
        
        if ShowAIStats == True:
            stats()
        
        # See README.md (4-1)
        print("===== Scoreboard =====")
        print("Player Wins:", PlayerWins, " AI Wins:", AIWins, " Draws:", Draws)
        print("Total Rounds:", RoundNum)

        # See README.md (4-2)
        print()
        print("---------- (Round", RoundNum + 1, ") ----------")
        display.scroll("Round " + str(RoundNum + 1), delay=100)

        print("\nWaiting for player input: A=Rock, B=Paper, A+B=Scissors")
        
        # See README.md (4-3)
        player_choice = None
        while True:
            for msg in PROMPTS:
                choice = _manual_scroll_and_poll(msg)
                if choice is not None:
                    player_choice = choice
                    break
            if player_choice is not None:
                break
        
        # See README.md (4-4)
        is_first_turn = RoundNum == 0
        ai_choice = AIDecision(force_random=is_first_turn)
        
        # See README.md (4-5)
        _update_weights(player_choice)
        
        # See README.md (4-6)
        sequence = ["R", "P", "S"]
        step_delay = int((seconds / len(sequence)) * 1000)
        for word in sequence:
            display.show(word)
            sleep(step_delay)
        display.clear()
        
        # See README.md (4-7)
        result = None
        print()
        print("Player chose:", CHOICE_NAMES[player_choice])
        print("AI chose:", CHOICE_NAMES[ai_choice])

        if player_choice == ai_choice:
            result = "Draw"
            Draws += 1
            display.scroll("A Draw!", delay=120)
        elif ((player_choice == 1 and ai_choice == 3) or (player_choice == 2 and ai_choice == 1) or (player_choice == 3 and ai_choice == 2)):
            result = "Win"
            PlayerWins += 1
            display.scroll("You Win!", delay=120)
        else:
            result = "Loss"
            AIWins += 1
            display.scroll("You Lose!", delay=120)
        
        print("Result:", result)
        
        sleep(1000)


if __name__ == "__main__":
    main()