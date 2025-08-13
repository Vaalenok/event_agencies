import asyncio
from colorlog import ColoredFormatter
import logging
import sys

from parser import ParserClient


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


parser = ParserClient()


async def main():
    from handler import find_companies, get_company_info, get_persons_info, get_persons_links

    parse_tasks = [parser.parse_events(page) for page in range(1, 6)]
    raw_pages = await asyncio.gather(*parse_tasks)

    find_tasks = [asyncio.to_thread(find_companies, page) for page in raw_pages]
    incomplete_companies = await asyncio.gather(*find_tasks)
    incomplete_companies = [company for sublist in incomplete_companies for company in sublist]

    find_info_tasks = [parser.parse_company_info(company.slug) for company in incomplete_companies]
    info_htmls = await asyncio.gather(*find_info_tasks)

    add_company_info_tasks = [
        asyncio.to_thread(get_company_info, html, company)
            for html, company in zip(info_htmls, incomplete_companies)
    ]
    companies = await asyncio.gather(*add_company_info_tasks)

    add_person_info_tasks = [
        asyncio.to_thread(get_persons_info, html, company) for html, company in zip(info_htmls, companies)
    ]
    companies = await asyncio.gather(*add_person_info_tasks)

    add_person_links_tasks = [get_persons_links(company) for company in companies]
    companies = await asyncio.gather(*add_person_links_tasks)




if __name__ == "__main__":
    try:
        logging.info("Script started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script stopped")
