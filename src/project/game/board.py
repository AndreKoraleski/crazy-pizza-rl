from random import Random

import structlog

from project.game.constants import (
    NUMBER_OF_INGREDIENTS,
    TILES_PER_INGREDIENT,
    INGREDIENT_PREFIX,
    CHOOSE_ANY_INGREDIENT_TILES,
    CHOOSE_ANY_INGREDIENT_TILE_NAME,
    QUEUED_RANDOM_ACTION_TILES,
    QUEUED_RANDOM_ACTION_TILE_NAME,
    LOSE_ALL_INGREDIENTS_TILES,
    LOSE_ALL_INGREDIENTS_TILE_NAME,
    TOTAL_BOARD_SIZE,
)

logger = structlog.get_logger(__name__)


def generate_board(random_number_generator_seed: int | None) -> list[str]:
    """
    Generates a shuffled board based on constants.

    Args:
        random_number_generator_seed (int | None): The seed to use for the random number generator. If None, a random seed is used.

    Returns:
        list[str]: A shuffled list of board tiles.
    """
    logger.debug(
        "Generating board",
        seed=random_number_generator_seed,
        total_size=TOTAL_BOARD_SIZE,
    )
    rng = Random(random_number_generator_seed)
    board = []

    for i in range(NUMBER_OF_INGREDIENTS):
        tile_name = f"{INGREDIENT_PREFIX}{i}"
        board.extend([tile_name] * TILES_PER_INGREDIENT)

    board.extend([CHOOSE_ANY_INGREDIENT_TILE_NAME] * CHOOSE_ANY_INGREDIENT_TILES)
    board.extend([QUEUED_RANDOM_ACTION_TILE_NAME] * QUEUED_RANDOM_ACTION_TILES)
    board.extend([LOSE_ALL_INGREDIENTS_TILE_NAME] * LOSE_ALL_INGREDIENTS_TILES)

    assert (
        len(board) == TOTAL_BOARD_SIZE
    ), f"Expected board size {TOTAL_BOARD_SIZE}, but got {len(board)}"

    rng.shuffle(board)

    logger.debug(
        "Board generated successfully",
        board_size=len(board),
        ingredient_tiles=NUMBER_OF_INGREDIENTS * TILES_PER_INGREDIENT,
        special_tiles=CHOOSE_ANY_INGREDIENT_TILES
        + QUEUED_RANDOM_ACTION_TILES
        + LOSE_ALL_INGREDIENTS_TILES,
    )

    return board
