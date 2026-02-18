# Crazy Pizza RL

A reinforcement learning project exploring optimal strategies for the board game "Crazy Pizzeria" (also known as "Pizzaria Maluca"). This implementation uses a randomized setup to investigate how conscious decision-making based on board state and rival positions affects win rates.

## About the Game

### Overview
Crazy Pizza is a race-style board game where 6 players compete to be the first to complete their pizza by collecting all required ingredients.

### Game Objective
Each player is assigned a unique pizza slice requiring **5 specific ingredients** from a pool of **10 possible ingredients**. The first player to collect all 5 of their required ingredients wins the game.

### Key Differences from the Original
- **Randomized Ingredients**: In the physical game, pizza slices have fixed ingredient combinations. This implementation randomizes the ingredient assignments for each player to create more varied gameplay scenarios.
- **Randomized Board**: The board layout is procedurally generated rather than using a fixed configuration, adding additional strategic complexity.
- **Shared Game Piece**: Instead of individual player tokens, all players share a common game piece that moves around the circular board. This creates an interesting strategic dimension as players must consider the board state left for the next players and up until it's their turn again.

## Game Mechanics

### Setup
1. **6 Players** are assigned unique pizza slices, each requiring 5 ingredients from a pool of 10 total ingredients
2. Players are ordered 0-5 (representing youngest to oldest in the physical game)
3. A **circular board** with 35 tiles is generated, containing:
   - **Ingredient tiles** (20): Two tiles for each of the 10 ingredient types
   - **Chef tiles** (2): Wildcard spaces where players choose any needed ingredient
   - **Lose All tiles** (1): Players lose all collected ingredients
   - **Card tiles** (12): Draw a luck/misfortune card
4. A shared game piece starts at a random position on the board

### Turn Structure
On each turn, a player:
1. **Rolls a six-sided die** (1-6)
2. **Moves the shared game piece** clockwise by the rolled amount
3. **Resolves the tile** where the piece lands:

#### Tile Types

**Ingredient Tiles**
- If the ingredient matches one of the player's needed ingredients, they collect it
- If they already have it or don't need it, nothing happens

**Chef Tiles**
- Player chooses any ingredient they still need
- Acts as a wildcard space

**Lose All Tiles**
- Player loses all ingredients they have collected
- Must start collecting from scratch

**Card Tiles (Luck/Misfortune)**
- Player draws a random card from the action queue, simulated like a stack of cards instead of independent random draws.
- Possible card effects:
  - **Lose X ingredients**: Remove 1 or 2 of their choice, or all ingredients from their collection
  - **Gain X ingredients**: Choose 1 or 2 needed ingredients to add
  - **Steal X ingredients**: Take 1 or 2 ingredients from any number of other players (if they have ingredients you need)
- Even if the card effect is a non-choice or can only be partially completed (like Lose 2 when having only one), it still takes effect

### Winning Condition
The first player to collect all 5 of their required ingredients immediately wins the game.

## Research Goals

This implementation aims to explore:

1. **Strategic Decision-Making**: Can AI agents learn to make better choices (when selecting ingredients from Chef tiles or Card actions) based on:
   - Current board state and upcoming tiles
   - Opponents' progress and ingredient collections
   - Distance to needed ingredients

2. **Shared Pointer Dynamics**: How does having a shared game piece (vs. individual player tokens) affect optimal strategy?
   - Players must consider not just their own position, but what different possibilities there are for when their turn comes around

3. **Balancing Randomness vs. Skill**: With significant randomness from dice rolls and card draws, how much can intelligent play improve win rates?

## Project Structure

```
src/project/
├── game/
│   ├── agent.py          # Player agent implementation
│   ├── board.py          # Circular board with tiles
│   ├── condition.py      # Ingredient assignment algorithm
│   ├── constants.py      # Game configuration constants
│   ├── engine.py         # Main game engine and logic
│   └── queue.py          # Action card queue
├── logging/
│   ├── logger.py         # Logging configuration
│   ├── renderer.py       # Game state visualization
│   └── types.py          # Logging type definitions
└── settings/
    ├── base/             # Base settings infrastructure
    └── model/            # Settings models
```

## Running the Game

```bash
# Install dependencies
pip install -e .

# Run a single game
python -m project
```

## Technical Details

### Ingredient Distribution
The ingredient assignment algorithm uses backtracking to ensure:
- Each player gets exactly 5 unique ingredients
- Each ingredient appears exactly 3 times across all players (balanced distribution)
- All combinations are unique
- Generation is deterministic when using a fixed seed

Average generation time: **~1.28 ms** (780 generations/second). Beware of greater parameters.

### Board Generation
- 35 tiles arranged in a circle
- Deterministic tile distribution based on constants
- Tiles are shuffled for randomization while maintaining balance

### Card Queue
The action card deck contains 24 cards:
- **Lose cards** (11): 8× lose 1, 2× lose 2, 1× lose all
- **Gain cards** (9): 7× choose 1, 2× choose 2  
- **Steal cards** (4): 3× steal 1, 1× steal 2
