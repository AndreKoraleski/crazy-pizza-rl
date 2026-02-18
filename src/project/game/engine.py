from random import Random

import structlog

from project.game.agent import Agent
from project.game.board import generate_board
from project.game.condition import generate_conditions
from project.game.queue import generate_action_queue

from project.game.constants import (
    NUMBER_OF_PLAYERS,
    NUMBER_OF_INGREDIENTS,
    MOVEMENT_DICE_COUNT,
    MOVEMENT_DICE_SIDES,
    INGREDIENT_PREFIX,
    CHOOSE_ANY_INGREDIENT_TILE_NAME,
    QUEUED_RANDOM_ACTION_TILE_NAME,
    LOSE_ALL_INGREDIENTS_TILE_NAME,
)

logger = structlog.get_logger(__name__)


class GameEngine:
    """
    Core game engine class.
    """

    def __init__(self, seed: int | None = None) -> None:
        """
        Initialize the game engine.

        Args:
            seed (int | None):
                Seed for deterministic randomness.
                If None, randomness will be non-deterministic.
        """

        logger.debug("Initializing game engine", seed=seed)

        # RNG used for all game randomness
        self.rng = Random(seed)

        # Generate deterministic components using derived seeds
        board_seed = seed + 1 if seed is not None else None
        queue_seed = seed + 2 if seed is not None else None
        condition_seed = seed + 3 if seed is not None else None

        self.board = generate_board(board_seed)
        self.action_queue = generate_action_queue(queue_seed)
        conditions = generate_conditions(condition_seed)

        # Create agents with empty starting state
        self.agents = [
            Agent(agent_id=i, condition=conditions[i], state=0)
            for i in range(NUMBER_OF_PLAYERS)
        ]

        # Log each agent's winning condition
        for agent in self.agents:
            logger.info(
                "Agent created",
                agent_id=agent.id,
                needs=[
                    i
                    for i in range(NUMBER_OF_INGREDIENTS)
                    if agent.condition & (1 << i)
                ],
                total_needed=agent.condition.bit_count(),
            )

        # Shared board pointer (global position)
        self.board_position = 0

        # Turn tracking
        self.current_agent_index = 0
        self.turn_count = 0

        logger.info(
            "Game engine initialized",
            board_size=len(self.board),
            queue_size=len(self.action_queue),
            num_agents=len(self.agents),
        )

    # =============================================================================
    # Movement logic
    # =============================================================================

    def roll_movement_dice(self) -> int:
        """
        Roll the movement dice.

        Returns:
            int: Total number of steps to move.
        """

        total = 0

        for _ in range(MOVEMENT_DICE_COUNT):
            total += self.rng.randint(1, MOVEMENT_DICE_SIDES)

        logger.debug("Movement dice rolled", total=total)

        return total

    def advance_board(self, steps: int) -> str:
        """
        Advance the shared board position.

        Args:
            steps (int): Number of steps to move forward.

        Returns:
            str: Tile name landed on.
        """

        old_position = self.board_position

        self.board_position = (self.board_position + steps) % len(self.board)

        tile = self.board[self.board_position]

        logger.debug(
            "Board advanced",
            old_position=old_position,
            new_position=self.board_position,
            tile=tile,
        )

        return tile

    # =============================================================================
    # Action queue handling
    # =============================================================================

    def pop_action(self) -> str:
        """
        Pop the next action from the queue.

        If queue is empty, regenerate it.

        Returns:
            str: Action string.
        """

        if not self.action_queue:

            # Replenish queue
            new_seed = self.rng.randint(0, 2**31 - 1)
            self.action_queue = generate_action_queue(new_seed)

            logger.debug("Action queue replenished", seed=new_seed)

        action = self.action_queue.pop(0)

        logger.debug("Action popped", action=action)

        return action

    # =============================================================================
    # Mask computation
    # =============================================================================

    def compute_choose_mask(self, agent: Agent) -> int:
        """
        Compute valid choose mask.

        Only ingredients still needed are valid.

        Args:
            agent (Agent): Agent for which to compute the mask

        Returns:
            int: Bitmask
        """

        return agent.needed_mask

    def compute_lose_mask(self, agent: Agent) -> int:
        """
        Compute valid lose mask.

        Only owned AND needed ingredients can be lost.

        Args:
            agent (Agent): Agent for which to compute the mask

        Returns:
            int: Bitmask
        """

        return agent.state & agent.needed_mask

    def compute_steal_mask(self, agent: Agent) -> int:
        """
        Compute valid steal mask.

        Only ingredients owned by others AND needed by agent.

        Args:
            agent (Agent): Agent for which to compute the mask

        Returns:
            int: Bitmask
        """

        other_owned = 0

        for other in self.agents:

            if other.id != agent.id:
                other_owned |= other.state

        return other_owned & agent.needed_mask

    # =============================================================================
    # Bit selection
    # =============================================================================

    def select_random_bits(self, mask: int, count: int) -> int:
        """
        Randomly select bits from a mask.

        Args:
            mask (int): Valid bitmask
            count (int): Number of bits to select

        Returns:
            int: Selected mask
        """

        available = [bit for bit in range(NUMBER_OF_INGREDIENTS) if mask & (1 << bit)]

        selected_bits = self.rng.sample(available, count)

        result = 0

        for bit in selected_bits:
            result |= 1 << bit

        return result

    # =============================================================================
    # Resolution helpers
    # =============================================================================

    def auto_resolve_choose(self, agent: Agent, mask: int, amount: int) -> None:
        """
        Resolve choose action automatically or randomly.

        Args:
            agent (Agent): Choosing agent
            mask (int): Valid ingredients to choose
            amount (int): Number of ingredients to choose
        """

        count = mask.bit_count()

        if count == 0:
            return

        if count <= amount:
            agent.choose(mask)
            return

        selected = self.select_random_bits(mask, amount)

        agent.choose(selected)

    def auto_resolve_lose(self, agent: Agent, mask: int, amount: int) -> None:
        """
        Resolve lose action automatically or randomly.

        Args:
            agent (Agent): Losing agent
            mask (int): Valid ingredients to lose
            amount (int): Number of ingredients to lose
        """

        count = mask.bit_count()

        if count == 0:
            return

        if count <= amount:
            agent.lose(mask)
            return

        selected = self.select_random_bits(mask, amount)

        agent.lose(selected)

    def auto_resolve_steal(self, agent: Agent, amount: int) -> None:
        """
        Resolve steal action automatically or randomly.

        Args:
            agent (Agent): Stealing agent
            amount (int): Number of ingredients to steal
        """

        mask = self.compute_steal_mask(agent)

        count = mask.bit_count()

        if count == 0:
            return

        if count <= amount:
            for other in self.agents:
                if other.id != agent.id:
                    agent.steal_from(other, mask)
            return

        selected = self.select_random_bits(mask, amount)

        for other in self.agents:
            if other.id != agent.id:
                agent.steal_from(other, selected)

    # =============================================================================
    # Tile resolution
    # =============================================================================

    def resolve_tile(self, agent: Agent, tile: str) -> None:
        """
        Resolve tile effect.

        Args:
            agent (Agent): Agent landing on tile
            tile (str): Tile name
        """

        logger.debug("Resolving tile", agent_id=agent.id, tile=tile)

        if tile.startswith(INGREDIENT_PREFIX):

            ingredient_id = int(tile[len(INGREDIENT_PREFIX) :])

            mask = 1 << ingredient_id

            if mask & agent.needed_mask:
                agent.choose(mask)

        elif tile == CHOOSE_ANY_INGREDIENT_TILE_NAME:

            mask = self.compute_choose_mask(agent)

            self.auto_resolve_choose(agent, mask, 2)

        elif tile == QUEUED_RANDOM_ACTION_TILE_NAME:

            action = self.pop_action()

            self.resolve_action(agent, action)

        elif tile == LOSE_ALL_INGREDIENTS_TILE_NAME:

            agent.lose(agent.state)

    def resolve_action(self, agent: Agent, action: str) -> None:
        """
        Resolve action queue entry.

        Args:
            agent (Agent): Agent affected by the action
            action (str): Action string
        """
        logger.info(
            "Resolving action from card",
            agent_id=agent.id,
            action=action,
        )

        logger.debug("Resolving action", agent_id=agent.id, action=action)

        if action.startswith("choose"):

            amount = int(action[len("choose") :])

            mask = self.compute_choose_mask(agent)

            self.auto_resolve_choose(agent, mask, amount)

        elif action.startswith("lose"):

            if action == "loseall":

                agent.lose(agent.state)

            else:

                amount = int(action[len("lose") :])

                mask = self.compute_lose_mask(agent)

                self.auto_resolve_lose(agent, mask, amount)

        elif action.startswith("steal"):

            amount = int(action[len("steal") :])

            self.auto_resolve_steal(agent, amount)

    # =============================================================================
    # Game step
    # =============================================================================

    def step(self) -> int | None:
        """
        Execute one turn.

        Returns:
            int | None:
                Winning agent ID, or None if no winner yet.
        """

        agent = self.agents[self.current_agent_index]

        logger.info(
            "Turn started",
            turn=self.turn_count,
            agent_id=agent.id,
        )

        movement = self.roll_movement_dice()

        tile = self.advance_board(movement)

        logger.info(
            "Agent landed on tile",
            agent_id=agent.id,
            movement=movement,
            position=self.board_position,
            tile=tile,
        )

        self.resolve_tile(agent, tile)

        # Check win condition
        if agent.has_won:

            logger.info(
                "Agent won",
                agent_id=agent.id,
                turn=self.turn_count,
            )

            return agent.id

        # Advance turn
        self.current_agent_index = (self.current_agent_index + 1) % NUMBER_OF_PLAYERS

        self.turn_count += 1

        return None
