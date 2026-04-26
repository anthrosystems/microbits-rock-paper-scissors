# AI Explaination: Player plays Rock x3, then Paper (In-depth)

**For both examples, we start with all influences equal:**

- `RockInfluence = 1.0`
- `PaperInfluence = 1.0`
- `ScissorsInfluence = 1.0`

## Scenario 1 - Not using damping:

**Step 1 - Player picks `Rock` (first time):**

- `RockInfluence` increases by `1` → `RockInfluence = 2.0`
- Total influence (`total_influence`) = `RockInfluence + PaperInfluence + ScissorsInfluence` = `2.0 + 1.0 + 1.0 = 4.0`
- Weights:
  - `RockWeight` = `ScissorsInfluence / total_influence` = `1 / 4` = `25%`
  - `PaperWeight` = `RockInfluence / total_influence` = `2 / 4` = `50%`
  - `ScissorsWeight` = `PaperInfluence / total_influence` = `1 / 4` = `25%`

**Step 2 - Player picks `Rock` again (second time):**

- `RockInfluence` increases by `1` → `RockInfluence = 3.0`
- `total_influence` = `RockInfluence + PaperInfluence + ScissorsInfluence` = `3.0 + 1.0 + 1.0 = 5.0`
- Weights:
  - `RockWeight` = `ScissorsInfluence / total_influence` = `1 / 5` = `20%`
  - `PaperWeight` = `RockInfluence / total_influence` = `3 / 5` = `60%`
  - `ScissorsWeight` = `PaperInfluence / total_influence` = `1 / 5` = `20%`

**Step 3 - Player picks `Rock` a third time:**

- `RockInfluence` increases by `1` → `RockInfluence = 4.0`
- `total_influence` = `RockInfluence + PaperInfluence + ScissorsInfluence` = `4.0 + 1.0 + 1.0 = 6.0`
- Weights:
  - `RockWeight` = `ScissorsInfluence / total_influence` = `1 / 6` ≈ `16.67%`
  - `PaperWeight` = `RockInfluence / total_influence` = `4 / 6` ≈ `66.67%`
  - `ScissorsWeight` = `PaperInfluence / total_influence` = `1 / 6` ≈ `16.67%`

**Step 4 - Player picks `Paper`:**

- `PaperInfluence` increases by `1` → `PaperInfluence = 2.0`
- `total_influence` = `RockInfluence + PaperInfluence + ScissorsInfluence` = `4.0 + 2.0 + 1.0 = 7.0`
- Weights:
  - `RockWeight` = `ScissorsInfluence / total_influence` = `1 / 7` ≈ `14.29%`
  - `PaperWeight` = `RockInfluence / total_influence` = `4 / 7` ≈ `57.14%`
  - `ScissorsWeight` = `PaperInfluence / total_influence` = `2 / 7` ≈ `28.57%`

**Result:**

Step | Move | Influences (Rock, Paper, Scissors) | Total Influence | Weights (Rock, Paper, Scissors)
---|---|---|---|---
1 | Rock | (2.0, 1.0, 1.0) | 4.0 | (25.00%, 50.00%, 25.00%)
2 | Rock | (3.0, 1.0, 1.0) | 5.0 | (20.00%, 60.00%, 20.00%)
3 | Rock | (4.0, 1.0, 1.0) | 6.0 | (16.67%, 66.67%, 16.67%)
4 | Paper | (4.0, 2.0, 1.0) | 7.0 | (14.29%, 57.14%, 28.57%)

**Analysis:** After Step 3 the AI strongly favours Paper (`≈66.7%`); after Step 4 the weights shift to still favour Paper (`≈57.1%`).

**Next scenario:** Now compare the same sequence using damping to see how we reduce the effect repeated moves have on weights.

## Scenario 2 - Using damping:

**Step 1 - Player picks `Rock` (first time):**

- `SameMoveStreak = 1`
- `streak_damping` = `1 / (((SameMoveStreak - 1) * 0.5) + 1)` = `1.0`
- `RockInfluence` increases by `streak_damping` (`1.0`) → `RockInfluence = 2.0`
- Total influence (`total_influence`) = `RockInfluence + PaperInfluence + ScissorsInfluence` = `2.0 + 1.0 + 1.0` = `4.0`
- Weights:
  - `RockWeight` = `ScissorsInfluence / total_influence` = `1 / 4` = `25%`
  - `PaperWeight` = `RockInfluence / total_influence` = `2 / 4` = `50%`
  - `ScissorsWeight` = `PaperInfluence / total_influence` = `1 / 4` = `25%`

**Step 2 - Player picks `Rock` again (second time):**

- `SameMoveStreak = 2`
- `streak_damping` = `1 / (((SameMoveStreak - 1) * 0.5) + 1)` = `1 / 1.5` ≈ `0.6667`
- `RockInfluence` increases by `streak_damping` (`0.6667`) → `RockInfluence ≈ 2.6667`
- `total_influence` = `RockInfluence + PaperInfluence + ScissorsInfluence` ≈ `2.6667 + 1 + 1` ≈ `4.6667`
- Weights:
  - `RockWeight` = `ScissorsInfluence / total_influence` ≈ `1 / 4.6667` ≈ `21.4%`
  - `PaperWeight` = `RockInfluence / total_influence` ≈ `2.6667 / 4.6667` ≈ `57.1%`
  - `ScissorsWeight` = `PaperInfluence / total_influence` ≈ `1 / 4.6667` ≈ `21.4%`

**Step 3 - Player picks `Rock` a third time:**

- `SameMoveStreak = 3`
- `streak_damping` = `1 / (((SameMoveStreak - 1) * 0.5) + 1)` = `1 / 2` = `0.5`
- `RockInfluence` increases by `streak_damping` (`0.5`) → `RockInfluence ≈ 3.1667`
- `total_influence` = `RockInfluence + PaperInfluence + ScissorsInfluence` ≈ `3.1667 + 1 + 1` ≈ `5.1667`
- Weights:
  - `RockWeight` = `ScissorsInfluence / total_influence` ≈ `1 / 5.1667` ≈ `19.35%`
  - `PaperWeight` = `RockInfluence / total_influence` ≈ `3.1667 / 5.1667` ≈ `61.29%`
  - `ScissorsWeight` = `PaperInfluence / total_influence` ≈ `1 / 5.1667` ≈ `19.35%`

**Step 4 - Player picks `Paper`:**

- `SameMoveStreak = 1` (`SameMoveStreak` resets to `1` as `Paper` is a different move to `Rock`)
- `streak_damping` = `1 / (((SameMoveStreak - 1) * 0.5) + 1)` = `1.0`
- `PaperInfluence` increases by `streak_damping` (`1.0`) → `PaperInfluence = 2.0`
- `total_influence` = `RockInfluence + PaperInfluence + ScissorsInfluence` ≈ `3.1667 + 2 + 1` ≈ `6.1667`
- Weights:
  - `RockWeight` = `ScissorsInfluence / total_influence` ≈ `1 / 6.1667` ≈ `16.21%`
  - `PaperWeight` = `RockInfluence / total_influence` ≈ `3.1667 / 6.1667` ≈ `51.35%`
  - `ScissorsWeight` = `PaperInfluence / total_influence` ≈ `2 / 6.1667` ≈ `32.43%`

**Result:**

Step | Move | SameMoveStreak | Influences (Rock, Paper, Scissors) | Total Influence | Weights (Rock, Paper, Scissors)
---|---|---|---|---|---
1 | Rock | 1 | (2.0000, 1.0000, 1.0000) | 4.0000 | (25.00%, 50.00%, 25.00%)
2 | Rock | 2 | (2.6667, 1.0000, 1.0000) | 4.6667 | (21.43%, 57.14%, 21.43%)
3 | Rock | 3 | (3.1667, 1.0000, 1.0000) | 5.1667 | (19.35%, 61.29%, 19.35%)
4 | Paper | 1 | (3.1667, 2.0000, 1.0000) | 6.1667 | (16.21%, 51.35%, 32.43%)

**Analysis:** With damping the AI still favours Paper after step 3 (`≈61.3%`), but the jump is smaller than without damping (`≈51.35%`) and the AI can recover faster when the player switches moves.

Step | Damping? | Move | Weights (Rock, Paper, Scissors)
---|---|---|---
3 | No | Rock | (16.67%, 66.67%, 16.67%)
3 | Yes | Rock | (19.35%, 61.29%, 19.35%)
4 | No | Paper | (14.29%, 57.14%, 28.57%)
4 | Yes | Paper | (16.21%, 51.35%, 32.43%)

The damping reduces how quickly `RockInfluence` grows on repeated picks, preventing instant "weight poisoning" (while still adapting reasonably), allowing for the AI to have a higher chance to pick `Rock` when the player switches to picking `Paper`.

## Quick takeaway
Use this worked example to show learners how the AI's internal numbers change and how that affects its choices.

Analogy - jars and a spinner:
- Imagine three jars of marbles labelled `Rock`, `Paper`, and `Scissors`. Each marble represents influence for that move.
- The AI chooses by spinning a wheel divided into three slices. Each slice's size is set from the jar of the move it would beat (e.g., the `Scissors` slice size comes from `Paper`'s jar).
- So when `PaperInfluence` goes up (more marbles in the Paper jar), the spinner gives a larger slice to `Scissors`, making the AI more likely to pick `Scissors`.

## Key teaching points:
- Adding influence increases the total, so other moves' percentage shares shrink unless they also gain influence.
- Damping reduces how many marbles are added on repeated plays, preventing one jar from quickly dominating (avoids "weight poisoning").
- Show the serial stats alongside the game and ask learners to predict the spinner outcome before it runs.