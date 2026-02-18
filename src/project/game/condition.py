from itertools import combinations
from random import Random

import structlog

from project.game.constants import (
    NUMBER_OF_PLAYERS,
    NUMBER_OF_INGREDIENTS,
    INGREDIENTS_PER_PLAYER,
    NUMBER_OF_COPIES_PER_INGREDIENT,
)

logger = structlog.get_logger(__name__)


def generate_conditions(seed: int | None) -> list[int]:
    """
    Generates a list of unique conditions for each player based on the number of ingredients and copies.

    Each player gets exactly INGREDIENTS_PER_PLAYER unique ingredients.
    Distribution aims to be balanced across all ingredients.

    Args:
        seed (int | None): The seed to use for the random number generator. If None, a random seed is used.

    Returns:
        list[int]: A list of unique conditions for each player, where each condition is represented as a bitmask of ingredients.
    """
    logger.debug(
        "Generating conditions",
        seed=seed,
        num_players=NUMBER_OF_PLAYERS,
        num_ingredients=NUMBER_OF_INGREDIENTS,
    )

    rng = Random(seed)

    required_slots = NUMBER_OF_INGREDIENTS * NUMBER_OF_COPIES_PER_INGREDIENT
    total_slots = NUMBER_OF_PLAYERS * INGREDIENTS_PER_PLAYER

    if required_slots != total_slots:
        raise ValueError(
            "Infeasible configuration: total ingredient slots must equal total player ingredient slots"
        )

    remaining = [NUMBER_OF_COPIES_PER_INGREDIENT] * NUMBER_OF_INGREDIENTS

    all_masks = []

    for combo in combinations(range(NUMBER_OF_INGREDIENTS), INGREDIENTS_PER_PLAYER):
        mask = 0
        for i in combo:
            mask |= 1 << i
        all_masks.append(mask)

    rng.shuffle(all_masks)

    solution = []

    def mask_is_feasible(mask: int) -> bool:
        """
        Checks if a given mask is feasible based on the remaining ingredient copies.

        Args:
            mask (int): The bitmask representing the ingredients for a player.
        Returns:
            bool: True if the mask is feasible, False otherwise.
        """
        for ingredient in range(NUMBER_OF_INGREDIENTS):
            if mask & (1 << ingredient):
                if remaining[ingredient] <= 0:
                    return False
        return True

    def apply_mask(mask: int, delta: int) -> None:
        """
        Applies a mask to the remaining ingredient copies, either adding or removing based on the delta.

        Args:
            mask (int): The bitmask representing the ingredients for a player.
            delta (int): The value to add (positive) or subtract (negative) from the remaining copies.
        """
        for ingredient in range(NUMBER_OF_INGREDIENTS):
            if mask & (1 << ingredient):
                remaining[ingredient] += delta

    def backtrack(player_index: int) -> bool:
        """
        Backtracking function to assign conditions to players while ensuring feasibility.

        Args:
            player_index (int): The index of the current player being assigned a condition.
        
        Returns:
            bool: True if a valid assignment is found, False otherwise.
        """
        if player_index == NUMBER_OF_PLAYERS:
            return True

        for mask in all_masks:
            if mask in solution:
                continue

            if not mask_is_feasible(mask):
                continue

            solution.append(mask)
            apply_mask(mask, -1)

            if backtrack(player_index + 1):
                return True

            apply_mask(mask, 1)
            solution.pop()

        return False

    success = backtrack(0)

    if not success:
        raise ValueError("Failed to generate conditions with the given configuration")

    logger.debug("Generated conditions successfully", conditions=solution)

    return solution
