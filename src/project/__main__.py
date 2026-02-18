import structlog

from project.logging import configure_logging
from project.settings import get_settings
from project.game.engine import GameEngine


def main():
    # Load settings
    settings = get_settings()

    # Logging configuration (must be done before any logging is done)
    configure_logging(level=settings.log.level, format=settings.log.format)

    logger = structlog.get_logger(__name__)

    logger.info("Starting Crazy Pizza RL game")

    # Initialize game with seed
    game = GameEngine(seed=42)

    # Run game until someone wins
    winner_id = None
    max_turns = 1000  # Safety limit to prevent infinite loops

    while winner_id is None and game.turn_count < max_turns:
        winner_id = game.step()

    if winner_id is not None:
        logger.info(
            "Game completed",
            winner_id=winner_id,
            total_turns=game.turn_count,
        )
    else:
        logger.warning(
            "Game reached maximum turn limit without a winner",
            max_turns=max_turns,
        )


if __name__ == "__main__":
    main()
