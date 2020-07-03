import logging

from aiohttp import web

logger = logging.getLogger(__name__)


async def check_health(_: web.Request) -> web.Response:
    """Check freezes"""
    return web.HTTPOk()
