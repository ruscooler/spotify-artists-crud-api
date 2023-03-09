import datetime
import logging
from functools import lru_cache
from urllib.parse import urlencode

from rich.console import Console
from rich.logging import RichHandler

console = Console(color_system="256", width=200, style="blue")


@lru_cache
def get_logger(module_name):
    logger = logging.getLogger(module_name)
    handler = RichHandler(
        rich_tracebacks=True, console=console, tracebacks_show_locals=True
    )
    handler.setFormatter(
        logging.Formatter("[ %(threadName)s:%(funcName)s:%(lineno)d ] - %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)
    return logger


def prepare_query_param_for_spotify_api(query: dict, search_type: str = 'artist', offset=0, limit=20) -> str:
    query = " ".join([f"{k}:{v}" for k, v in query.items()])
    return urlencode({"q": query, "type": search_type.lower(), "offset": offset, "limit": limit})


def current_datetime():
    return datetime.datetime.utcnow()

