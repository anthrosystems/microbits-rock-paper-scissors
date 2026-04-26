# AI Explaination: Player plays Rock x3, then Paper (Simple)

Analogy - jars and a spinner:

- Imagine three jars of marbles labelled `Rock`, `Paper`, and `Scissors`. Each marble is one unit of "influence" for that move.
- Each time the player picks a move we add marbles to that move's jar. If the player repeats the same move, we add fewer marbles so a single jar can't dominate too fast.
- A jar gains more "weight" the more marbles it has.
- To pick a move the AI spins a wheel with 3 slices for `Rock`, `Paper`, and `Scissors`. Each slice's size comes from the jars:
    - `Rock`'s slice size on the wheel is based on the "weight" (number of marbles) of the `Scissors` jar.
    - `Paper`'s slice size on the wheel is based on the "weight" (number of marbles) of the `Rock` jar.
    - `Scissors`'s slice size on the wheel is based on the "weight" (number of marbles) of the `Paper` jar.

For both examples we start with the same initial marbles (influence):

- `RockInfluence = 1.0`
- `PaperInfluence = 1.0`
- `ScissorsInfluence = 1.0`

Total influence is:

`total = RockInfluence + PaperInfluence + ScissorsInfluence`

Weights (what the spinner uses) are:

- `RockWeight = ScissorsInfluence / total`
- `PaperWeight = RockInfluence / total`
- `ScissorsWeight = PaperInfluence / total`

Damping formula (we'll be needing this in **Scenario 2**):

`streak_damping = 1 / (((SameMoveStreak - 1) * 0.5) + 1)`

How to compute each step (plain words):

- If the move is the same as the previous move, `marbles_to_add = streak_damping`. Otherwise, `marbles_to_add = 1`.
- `NewInfluence = OldInfluence + marbles_to_add`.
- Recompute `total` and then the three weights above.

This short block is the only algebra you need - the tables below show the numeric results when we plug in the numbers.

## Scenario 1 - No damping (add 1 marble every time)

Step | Move | Influences (Rock, Paper, Scissors) | Total | Weights (Rock, Paper, Scissors)
---|---|---:|---:|---
1 | Rock | (2.0, 1.0, 1.0) | 4.0 | (25.00%, 50.00%, 25.00%)
2 | Rock | (3.0, 1.0, 1.0) | 5.0 | (20.00%, 60.00%, 20.00%)
3 | Rock | (4.0, 1.0, 1.0) | 6.0 | (16.67%, 66.67%, 16.67%)
4 | Paper | (4.0, 2.0, 1.0) | 7.0 | (14.29%, 57.14%, 28.57%)

## Scenario 2 - With damping (add fewer marbles on repeats)

Step | Move | SameMoveStreak | Influences (Rock, Paper, Scissors) | Total | Weights (Rock, Paper, Scissors)
---|---|---:|---:|---:|---
1 | Rock | 1 | (2.0000, 1.0000, 1.0000) | 4.0000 | (25.00%, 50.00%, 25.00%)
2 | Rock | 2 | (2.6667, 1.0000, 1.0000) | 4.6667 | (21.43%, 57.14%, 21.43%)
3 | Rock | 3 | (3.1667, 1.0000, 1.0000) | 5.1667 | (19.35%, 61.29%, 19.35%)
4 | Paper | 1 | (3.1667, 2.0000, 1.0000) | 6.1667 | (16.21%, 51.35%, 32.43%)

### Selected step arithmetic (plugging numbers into the short rules)

Step 2 (player repeats `Rock`):

- `SameMoveStreak = 2`
- `streak_damping = 1 / (((2 - 1) * 0.5) + 1) = 1 / (0.5 + 1) = 1 / 1.5 ≈ 0.6666667`
- `marbles_to_add = 0.6666667`
- `RockInfluence = 1.0 + 0.6666667 = 2.6666667`
- `total = 2.6666667 + 1.0 + 1.0 = 4.6666667`
- `RockWeight = 1.0 / 4.6666667 ≈ 21.43%`
- `PaperWeight = 2.6666667 / 4.6666667 ≈ 57.14%`

Step 3 (player repeats `Rock` again):

- `SameMoveStreak = 3`
- `streak_damping = 1 / (((3 - 1) * 0.5) + 1) = 1 / (1.0 + 1) = 1 / 2 = 0.5`
- `marbles_to_add = 0.5`
- `RockInfluence = 2.6666667 + 0.5 = 3.1666667`
- `total = 3.1666667 + 1.0 + 1.0 = 5.1666667`
- `RockWeight = 1.0 / 5.1666667 ≈ 19.35%`
- `PaperWeight = 3.1666667 / 5.1666667 ≈ 61.29%`

These few numeric steps show exactly how the short rules map to the numbers in the tables. Use the compact formula block above when teaching the concept, and the tables to show the results.