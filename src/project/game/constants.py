# =============================================================================
# Movement
# =============================================================================

MOVEMENT_DICE_COUNT: int = 1
MOVEMENT_DICE_SIDES: int = 6

# =============================================================================
# Players and ingredients
# =============================================================================

NUMBER_OF_PLAYERS: int = 6
NUMBER_OF_INGREDIENTS: int = 10
INGREDIENTS_PER_PLAYER: int = 5
NUMBER_OF_COPIES_PER_INGREDIENT: int = (
    NUMBER_OF_PLAYERS * INGREDIENTS_PER_PLAYER // NUMBER_OF_INGREDIENTS
)

# =============================================================================
# Board tiles
# =============================================================================

TILES_PER_INGREDIENT: int = 2  # 2 * NUMBER_OF_INGREDIENTS = 20
INGREDIENT_PREFIX: str = "ingredient"

CHOOSE_ANY_INGREDIENT_TILES: int = 2
CHOOSE_ANY_INGREDIENT_TILE_NAME: str = "chef"

QUEUED_RANDOM_ACTION_TILES: int = 12
QUEUED_RANDOM_ACTION_TILE_NAME: str = "card"

LOSE_ALL_INGREDIENTS_TILES: int = 1
LOSE_ALL_INGREDIENTS_TILE_NAME: str = "loseall"

# =============================================================================
# Action queue composition
# =============================================================================

ACTION_QUEUE_LOSE_ONE_AMOUNT: int = 8
ACTION_QUEUE_LOSE_TWO_AMOUNT: int = 2
ACTION_QUEUE_LOSE_ALL_AMOUNT: int = 1
ACTION_QUEUE_LOSE_PREFIX: str = "lose"

ACTION_QUEUE_CHOOSE_ONE_AMOUNT: int = 7
ACTION_QUEUE_CHOOSE_TWO_AMOUNT: int = 2
ACTION_QUEUE_CHOOSE_PREFIX: str = "choose"

ACTION_QUEUE_STEAL_ONE_AMOUNT: int = 3
ACTION_QUEUE_STEAL_TWO_AMOUNT: int = 1
ACTION_QUEUE_STEAL_PREFIX: str = "steal"


# =============================================================================
# Derived constants
# =============================================================================

TOTAL_ACTION_QUEUE_SIZE: int = (
    ACTION_QUEUE_LOSE_ONE_AMOUNT
    + ACTION_QUEUE_LOSE_TWO_AMOUNT
    + ACTION_QUEUE_LOSE_ALL_AMOUNT
    + ACTION_QUEUE_CHOOSE_ONE_AMOUNT
    + ACTION_QUEUE_CHOOSE_TWO_AMOUNT
    + ACTION_QUEUE_STEAL_ONE_AMOUNT
    + ACTION_QUEUE_STEAL_TWO_AMOUNT
)

TOTAL_BOARD_SIZE: int = (
    NUMBER_OF_INGREDIENTS * TILES_PER_INGREDIENT
    + CHOOSE_ANY_INGREDIENT_TILES
    + QUEUED_RANDOM_ACTION_TILES
    + LOSE_ALL_INGREDIENTS_TILES
)
