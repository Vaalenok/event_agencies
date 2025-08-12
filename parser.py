import aiohttp
import asyncio
import certifi
from fake_useragent import UserAgent
import logging
import ssl
from tenacity import retry, stop_after_attempt, RetryError


REQUESTS_PER_SECOND = 4
REQUEST_RETRIES = 5
TIMEOUT = 10

UA = UserAgent()


def get_headers(additional_headers: dict = None) -> dict:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": UA.random
    }

    if additional_headers:
        headers.update(additional_headers)

    return headers


class Queue:
    def __init__(self, max_concurrent_tasks: int):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.semaphore = asyncio.Semaphore(self.max_concurrent_tasks)
        self.loop = asyncio.get_running_loop()

    async def _worker(self, coro, *args, **kwargs):
        async with self.semaphore:
            return await coro(*args, **kwargs)

    def run_task(self, coro, *args, **kwargs):
        return self.loop.create_task(self._worker(coro, *args, **kwargs))


class ParserClient:
    def __init__(self):
        self.session = None

        self.queue = Queue(REQUESTS_PER_SECOND)

        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.ssl_context.options |= ssl.OP_LEGACY_SERVER_CONNECT

        self.insecure_ssl_context = ssl.create_default_context()
        self.insecure_ssl_context.check_hostname = False
        self.insecure_ssl_context.verify_mode = ssl.CERT_NONE

    @retry(stop=stop_after_attempt(REQUEST_RETRIES))
    async def parse_events(self, page: int):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as session:
            async with session.get(
                f"https://www.partyslate.com/api/find-vendors.json?category=planner&location=miami&page={page}",
                headers=get_headers(),
                ssl=self.ssl_context
            ) as response:
                return await response.json()

    async def try_parse_events(self, page: int):
        try:
            return await self.queue.run_task(self.parse_events, page)
        except RetryError as re:
            original_exception = re.last_attempt.exception()

            if not original_exception is None:
                original_exception = str(original_exception).strip()

            if not original_exception:
                original_exception = "Time limit exceeded"

            logging.error(f"Error parsing events: {original_exception}")
        except Exception as e:
            logging.error(f"Error parsing events: {e}")
            return None
