import logging
from typing import MutableMapping

import aio_pika

logger = logging.getLogger(__name__)


async def consume(_: MutableMapping, message: aio_pika.IncomingMessage) -> None:
    """Example consumer"""
    async with message.process(ignore_processed=True):
        print(message.body.decode(), flush=True)
