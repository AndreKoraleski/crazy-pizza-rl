from random import Random

import structlog

from project.game.constants import (
    ACTION_QUEUE_CHOOSE_ONE_AMOUNT,
    ACTION_QUEUE_CHOOSE_TWO_AMOUNT,
    ACTION_QUEUE_CHOOSE_PREFIX,
    ACTION_QUEUE_LOSE_ALL_AMOUNT,
    ACTION_QUEUE_LOSE_ONE_AMOUNT,
    ACTION_QUEUE_LOSE_PREFIX,
    ACTION_QUEUE_LOSE_TWO_AMOUNT,
    ACTION_QUEUE_STEAL_ONE_AMOUNT,
    ACTION_QUEUE_STEAL_PREFIX,
    ACTION_QUEUE_STEAL_TWO_AMOUNT,
    TOTAL_ACTION_QUEUE_SIZE,
)

logger = structlog.get_logger(__name__)


def generate_action_queue(random_number_generator_seed: int | None) -> list[str]:
    """
    Generates a shuffled action queue based on constants.

    Args:
        random_number_generator_seed (int | None): The seed to use for the random number generator. If None, a random seed is used.

    Returns:
        list[str]: A shuffled list of action queue tiles.
    """
    logger.debug(
        "Generating action queue",
        seed=random_number_generator_seed,
        total_size=TOTAL_ACTION_QUEUE_SIZE,
    )
    rng = Random(random_number_generator_seed)

    lose_1 = f"{ACTION_QUEUE_LOSE_PREFIX}1"
    lose_2 = f"{ACTION_QUEUE_LOSE_PREFIX}2"
    lose_all = f"{ACTION_QUEUE_LOSE_PREFIX}all"

    choose_1 = f"{ACTION_QUEUE_CHOOSE_PREFIX}1"
    choose_2 = f"{ACTION_QUEUE_CHOOSE_PREFIX}2"

    steal_1 = f"{ACTION_QUEUE_STEAL_PREFIX}1"
    steal_2 = f"{ACTION_QUEUE_STEAL_PREFIX}2"

    action_queue = []

    action_queue.extend([lose_1] * ACTION_QUEUE_LOSE_ONE_AMOUNT)
    action_queue.extend([lose_2] * ACTION_QUEUE_LOSE_TWO_AMOUNT)
    action_queue.extend([lose_all] * ACTION_QUEUE_LOSE_ALL_AMOUNT)

    action_queue.extend([choose_1] * ACTION_QUEUE_CHOOSE_ONE_AMOUNT)
    action_queue.extend([choose_2] * ACTION_QUEUE_CHOOSE_TWO_AMOUNT)

    action_queue.extend([steal_1] * ACTION_QUEUE_STEAL_ONE_AMOUNT)
    action_queue.extend([steal_2] * ACTION_QUEUE_STEAL_TWO_AMOUNT)

    assert (
        len(action_queue) == TOTAL_ACTION_QUEUE_SIZE
    ), f"Expected action queue size {TOTAL_ACTION_QUEUE_SIZE}, but got {len(action_queue)}"

    rng.shuffle(action_queue)

    logger.debug(
        "Action queue generated successfully",
        queue_size=len(action_queue),
        lose_actions=ACTION_QUEUE_LOSE_ONE_AMOUNT
        + ACTION_QUEUE_LOSE_TWO_AMOUNT
        + ACTION_QUEUE_LOSE_ALL_AMOUNT,
        choose_actions=ACTION_QUEUE_CHOOSE_ONE_AMOUNT + ACTION_QUEUE_CHOOSE_TWO_AMOUNT,
        steal_actions=ACTION_QUEUE_STEAL_ONE_AMOUNT + ACTION_QUEUE_STEAL_TWO_AMOUNT,
    )

    return action_queue
