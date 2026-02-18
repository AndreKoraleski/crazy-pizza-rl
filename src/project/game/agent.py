import structlog

logger = structlog.get_logger(__name__)


class Agent:
    """
    Represents a player in the game with a unique condition and current state.

    The agent's goal is to match their state to their condition by collecting ingredients.
    Both condition and state are represented as bitmasks where each bit represents an ingredient.
    """

    def __init__(self, agent_id: int, condition: int, state: int):
        """
        Initializes an agent with a unique ID, winning condition, and starting state.

        Args:
            agent_id (int): Unique identifier for the agent.
            condition (int): Bitmask representing the ingredients needed to win.
            state (int): Bitmask representing the ingredients currently held.
        """
        self.id = agent_id
        self.condition = condition
        self.state = state
        logger.debug(
            "Agent initialized",
            agent_id=agent_id,
            condition=bin(condition),
            state=bin(state),
        )

    @property
    def needed_mask(self) -> int:
        """
        Returns a bitmask of ingredients still needed to win.

        Returns:
            int: Bitmask where each set bit represents a needed ingredient.
        """
        return self.condition ^ self.state

    @property
    def needed_count(self) -> int:
        """
        Returns the number of ingredients still needed to win.

        Returns:
            int: Count of ingredients needed.
        """
        return self.needed_mask.bit_count()

    @property
    def has_won(self) -> bool:
        """
        Checks if the agent has collected all required ingredients.

        Returns:
            bool: True if the agent has won, False otherwise.
        """
        return self.condition == self.state

    def choose(self, mask: int) -> None:
        """
        Adds ingredients to the agent's state.

        Args:
            mask (int): Bitmask of ingredients to add.
        """
        old_state = self.state
        self.state |= mask

        if mask != 0:
            logger.info(
                "Agent gained ingredients",
                agent_id=self.id,
                gained=[i for i in range(10) if mask & (1 << i)],
                state=[i for i in range(10) if self.state & (1 << i)],
                still_needed=self.needed_count,
            )

        logger.debug(
            "Agent chose ingredients",
            agent_id=self.id,
            mask=bin(mask),
            old_state=bin(old_state),
            new_state=bin(self.state),
        )

    def lose(self, mask: int) -> None:
        """
        Removes ingredients from the agent's state.

        Args:
            mask (int): Bitmask of ingredients to remove.
        """
        old_state = self.state
        self.state &= ~mask

        if mask != 0:
            logger.info(
                "Agent lost ingredients",
                agent_id=self.id,
                lost=[i for i in range(10) if mask & (1 << i)],
                state=[i for i in range(10) if self.state & (1 << i)],
                still_needed=self.needed_count,
            )

        logger.debug(
            "Agent lost ingredients",
            agent_id=self.id,
            mask=bin(mask),
            old_state=bin(old_state),
            new_state=bin(self.state),
        )

    def steal_from(self, target: "Agent", mask: int) -> None:
        """
        Steals ingredients from another agent.

        Only ingredients that the target actually has and match the mask are stolen.

        Args:
            target (Agent): The agent to steal from.
            mask (int): Bitmask indicating which ingredients can be stolen.
        """
        # Only steal ingredients the target actually has
        stolen = target.state & mask
        old_target_state = target.state
        old_self_state = self.state
        target.state &= ~stolen
        self.state |= stolen

        if stolen != 0:
            logger.info(
                "Agent stole ingredients",
                thief_id=self.id,
                target_id=target.id,
                stolen=[i for i in range(10) if stolen & (1 << i)],
                thief_state=[i for i in range(10) if self.state & (1 << i)],
                target_state=[i for i in range(10) if target.state & (1 << i)],
            )

        logger.debug(
            "Agent stole from another agent",
            thief_id=self.id,
            target_id=target.id,
            mask=bin(mask),
            stolen=bin(stolen),
            thief_old_state=bin(old_self_state),
            thief_new_state=bin(self.state),
            target_old_state=bin(old_target_state),
            target_new_state=bin(target.state),
        )
