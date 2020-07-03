# New event loop policy is installed before application imports,
# because otherwise third party dependencies will initialize default event loop
import uvloop

uvloop.install()

import functools  # noqa
import logging.config  # noqa
from typing import AsyncGenerator  # noqa

import aio_pika  # noqa
from aiohttp import web  # noqa

from application import settings  # noqa
from application.handlers.http import infrastructure  # noqa
from application.handlers.rabbit import consumers  # noqa

logger = logging.getLogger(__name__)


def add_routes(app: web.Application) -> None:
    app.router.add_get('/api/v1/healthcheck', infrastructure.check_health)


async def setup_rabbit(app: web.Application) -> AsyncGenerator[None, None]:
    conn: aio_pika.RobustConnection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_LOGIN,
        password=settings.RABBITMQ_PASSWORD,
        timeout=settings.RABBITMQ_DEFAULT_TIMEOUT,
    )
    logger.info('Connected to RabbitMQ')
    consumers_channel = await conn.channel()
    await consumers_channel.set_qos(settings.RABBITMQ_PREFETCH_COUNT)
    queue = await consumers_channel.declare_queue(
        'example_queue', durable=True, timeout=settings.RABBITMQ_DEFAULT_TIMEOUT,
    )
    # Messages consuming will begin before the processing of HTTP requests!
    await queue.consume(functools.partial(consumers.consume, app))
    logger.info('All queues and exchanges initialized. Beginning to consume messages.')
    app['mq'] = await conn.channel()

    yield

    await conn.close()


def create_app() -> web.Application:
    """Creates application with setup contexts"""

    app: web.Application = web.Application(
        middlewares=(
            web.normalize_path_middleware(remove_slash=True, append_slash=False),
        ),
    )
    add_routes(app)
    app.cleanup_ctx.append(setup_rabbit)

    return app


def main() -> None:
    app = create_app()
    logging.config.dictConfig(settings.LOGGING)
    web.run_app(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)


if __name__ == '__main__':
    main()
