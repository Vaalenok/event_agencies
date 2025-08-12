import asyncio
from colorlog import ColoredFormatter
import logging
import sys


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red"
    }
)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


async def main():
    from handler import get_companies
    from parser import ParserClient

    parser = ParserClient()

    response = await parser.try_parse_events(1)
    companies = get_companies(response)

    print(companies)


if __name__ == "__main__":
    try:
        logging.info("Script started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script stopped")
