# microbits-rock-paper-scissors - Comments and educational explanations

Simple instructions to install and run the project (Windows-focused).

This project contains a desktop and a micro:bit version of Rock-Paper-Scissors. The micro:bit program is `microbit.py` and is flashed to the board as a `.hex` file.

This file contains the original comments extracted from the in-device program so you can use them when teaching. Keep this file in the project repository rather than flashing it to the micro:bit.

The following project and its documentation assumes that you have a basic understanding of python and its fundementals.

## Install Instructions:

1) Install Python

- Install Python 3.8 or newer from https://python.org. During install, enable "Add Python to PATH" if offered.

2) Open PowerShell in this project folder

- In File Explorer, open the project folder, then Shift+Right-Click → "Open PowerShell window here".

3) (Optional but recommended) Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4) Install the project dependencies

The project uses `pyproject.toml` to declare dependencies and packaging metadata.

Using `pyproject.toml` with pip:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .    # install in editable/development mode
```

This installs the tools the project needs (`uflash`, `pyserial`, etc.). If you prefer not to install in "editable" mode, use `python -m pip install .` instead.

If you use a packaging tool such as `poetry` or `flit`, follow their normal workflows; the dependencies in `pyproject.toml` will be respected by those tools.

5) Flash the correct firmware to the micro:bit

Follow [these instructions](https://microbit.org/get-started/user-guide/firmware/).

6) Flash the project to the micro:bit

Two common ways to create / install the `.hex` file are shown below.

- Direct flash to the attached micro:bit (uflash will build and flash):

```powershell
python -m uflash microbit.py
```

This attempts to build a `.hex` and immediately flash it to the connected device.

- Create a `.hex` file without auto-flashing (useful if auto-flash fails or you need to copy the file manually):

```powershell
python -m uflash microbit.py .
```

This writes `microbit.hex` (or similar) into the current folder; you can then copy that `.hex` onto the MICROBIT drive manually.

7) Open the serial monitor to see game stats (optional)

- Find the COM port for your micro:bit in Windows Device Manager (it appears as a USB Serial Device). You can also list ports from Python:

```powershell
python -m serial.tools.list_ports
```

- Start a simple serial terminal (replace `COM3` with your port):

```powershell
python -m serial.tools.miniterm COM3 115200
```

Press `Ctrl+]` to exit the miniterm session.

Note: serial ports are exclusive on Windows - only one program can open the same COM port at once. Close `miniterm` before running the visualiser, or run the visualiser instead of `miniterm`.

## Quick troubleshooting
- If flashing fails with a permission or DAPLink error, try re-plugging the board and ensure no file explorer window is copying a `.hex` file to the MICROBIT drive.
- If button presses do not register during display scrolling, reflash and run the serial monitor to capture any errors.

## Files of interest
- `microbit.py` - the single-file program flashed to the micro:bit.
- `docs/` - educational comments and explanations (kept out of the flashed file to save memory).
- `pyproject.toml` - lists the project dependencies.

If you want, I can add step-by-step screenshots for non-technical users. Let me know.

## Comments:

#### (1) Player Moves

Number -> move name.
We use numbers for Player input so it's easy to type/choose on the micro:bit.
- `1` = Rock
- `2` = Paper
- `3` = Scissors


#### (2) Core variables

- `RoundNum`: How many rounds have been played so far.
- `LastPlayerMove`: Last move the Player played (`1`, `2`, or `3`). Used to detect streaks.
- `AIMove`: The move the AI picked this round.
- `SameMoveStreak`: How many times the Player has chosen the same move in a row.
- `PlayerWins`: How many times the Player has won.
- `AIWins`: How many times the AI has won.
- `Draws`: How many times the round has resulted in a draw.


#### (3) Tracking variables

- `RockMoveNum`, `PaperMoveNum`, `ScissorsMoveNum`: How many times the Player chose each move.
- `RockInfluence`, `PaperInfluence`, `ScissorsInfluence`: The influence scores used to calculate AI weights.
- `RockWeight`, `PaperWeight`, `ScissorsWeight`: AI move weights calculated from the influences.


#### (4) Game loop and UI (on the micro:bit)

If you open the serial console on the host you'll also see printed Player moves, AI moves, and the scoreboard.

**(4-1)** Displays a simple scoreboard.

**(4-2)** Displays a UI for the game in the serial console. The micro:bit shows a short prompt telling the Player which buttons do which move:
  - Button A = Rock
  - Button B = Paper
  - Buttons A+B = Scissors

**(4-3)** The Player makes their move here.

**(4-4)** The AI makes its move here. It makes its move based on the weight of the *previous* round.

**(4-5)** Influences and Weights are updated here, ready to be used by the AI in the next round.

**(4-6)** After both the Player and AI make their moves, the micro:bit shows a short countdown: R, P, S.

**(4-7)** The micro:bit shows the round result on the LED display ("You Win!", "You Lose!", or "A Draw!").


#### (5) Stats and Display (on the host)

- `ShowAIStats`: when `True` the device prints helpful numbers to the host serial console so you can see what the AI "thinks". This does not display when `False`.
- `stats()` prints counts and weights; for teaching, you can open a serial terminal and watch how these numbers change after each round.


#### (6) AI decision logic

**(6-1)** On the first round the AI picks entirely at random so the game starts fair.
**(6-2)** After that, the AI looks at the three weights and picks one of the moves with the highest weight.
**(6-3)** If multiple moves tie for highest weight, the AI picks randomly between those tied moves.

##### Influence and Weighting (simple version)

  - Each move has an `Influence` score. We start all influences at `1.0` so the AI begins fair.
  - When the Player picks a move, that move's `Influence` goes up.
  - If the Player repeats the same move many times, we add a smaller amount each time (so spamming is less powerful).
  - We convert `Influence` into `Weight` percentages that add up to 100.
  - The AI uses counter-weights:
    - The Player choosing `Rock` raises the weight (and the chance) of the AI choosing `Paper`.
    - The Player choosing `Paper` raises the weight (and the chance) of the AI choosing `Scissors`.
    - The Player choosing `Scissors` raises the weight (and the chance) of the AI choosing `Rock`.

See (7) for an in-depth guide as to how this works.

#### (7) Learning from the Player (Influence and Weighting)

**(7-1)** When the Player chooses a move, we increase that move's `MoveNum` variable by `1`. For example, picking `Rock` increases `RockMoveNum` by `1`.

**(7-2)** If the Player repeats the same move many times, it can cause something called weight poisoning.

Weight poisoning is when the AI's internal "preferences" are manipulated so it always favors one move, usually because it was repeatedly fed the same input (intentionally or accidentally). The result is a predictable, unfair, or broken opponent. A simple analogy for this is teaching a child to play by only showing them “rock” over and over - they'll learn to always expect rock. That one-sided training “poisons” their judgment. To combat this, when the Player repeats the same move many times (for example, `Rock`), we reduce how much the Player's move affects the AI's weights.
  - **(7-2a)** If the Player repeats the same move many times, `SameMoveStreak` increases by `1`.

  - **(7-2b)** If the Player doesn't repeat the same move many times, `SameMoveStreak` stays at `1` and `LastPlayerMove` gets updated to the move the Player currently made.

**(7-3)** Here is where each move's `Influence` is calculated. We do this to calculate the weight of each move for the AI to use to make a decision.
  - **(7-3a)** We calculate the actual damping value (`streak_damping`) by:
    1) Subtracting `1` from `SameMoveStreak` (because `SameMoveStreak` is `1` if the Player hasn't repeated moves, so we reset this to `0` for the calculation)
    2) Multiplying it by `0.5`
    3) Adding `1` to `SameMoveStreak` (because if `SameMoveStreak` is `0`, the calculation doesn't work)
    4) Dividing `1` by this value.

  - **(7-3b)** We increase the influence score of the Player's chosen move by adding the calculated `streak_damping` variable the it. For example, picking `Rock` increases `RockInfluence` by the value of `streak_damping`.

**(7-4)**  Here is where each move's `Weight` is calculated. We do this so that the AI's moves are biased to counter the Player's most likely moves.
  - **(7-4a)** We calculate the total influence value (`total_influence`) by adding together all the move's influence values (`total_influence` = `RockInfluence` + `PaperInfluence` + `ScissorsInfluence`). If this results in `0`, `total_influence` is set to `1`.

  - **(7-4b)** Once we have `total_influence`, each move's `weight` is calculated using the opposing / "winning" move's influence value, divided by the value of `total_influence`. For example `Rock` beats `Scissors`, so `RockWeight` is calculate by dividing `ScissorsInfluence` by `total_influence`, and multiplying it by `100` to get a percentage. We do this so that the values of all the weights sum to 100%.
    
  - **(7-4c)** Here we update the original values of `RockWeight`, `PaperWeight` and `ScissorsWeight` with the new ones we just calculated so they can be used in the next round.

**See `examples.md` for more visual examples of how this works.**


#### Teaching Tips:

- Use the serial monitor to show the stats to learners; ask them to predict which move the AI will pick next.
- Let students try simple strategies (e.g., always Rock) and watch how the AI adapts over a few rounds.
- Explain influence vs weight with a simple analogy - jars and a spinner:
  - Imagine three jars of marbles labelled `Rock`, `Paper`, and `Scissors`. Each marble is one unit of "influence" for that move.
  - Each time the player picks a move we add marbles to that move's jar. If the player repeats the same move, we add fewer marbles so a single jar can't dominate too fast.
  - A jar gains more "weight" the more marbles it has.
  - To pick a move the AI spins a wheel with 3 slices for `Rock`, `Paper`, and `Scissors`. Each slice's size comes from the jars:
    - `Rock`'s slice size on the wheel is based on the "weight" (number of marbles) of the `Scissors` jar.
    - `Paper`'s slice size on the wheel is based on the "weight" (number of marbles) of the `Rock` jar.
    - `Scissors`'s slice size on the wheel is based on the "weight" (number of marbles) of the `Paper` jar.

Refer to `ai_explaination_simple.md` and `ai_explaination_in_depth.md` respectively for a simple and in-depth guide to how the AI works.

#### Notes for instructors

- Keeping comments in this file keeps the on-device program small, which helps avoid memory errors on older micro:bit firmware.
- You can print or display this file to learners and keep the running micro:bit program clean and fast.