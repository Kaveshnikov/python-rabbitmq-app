import json

import aio_pika
import aiormq
import pamqp
import pytest
from aiohttp import test_utils
from aioresponses import aioresponses
from asynctest import mock

from application import app, settings, utils


async def setup_rabbit_mock(application):
    application['mq'] = mock.create_autospec(aio_pika.RobustChannel)
    yield


@pytest.fixture
async def cli(mocker):
    mocker.patch('application.app.setup_rabbit', new=setup_rabbit_mock)
    application = app.create_app()

    async with test_utils.TestClient(test_utils.TestServer(application)) as client:
        yield client


def message_factory(data, routing_key='example_key', reply_to='example_queue', correlation_id='qwe'):
    return aio_pika.IncomingMessage(
        aiormq.types.DeliveredMessage(
            delivery=pamqp.specification.Basic.Deliver(
                routing_key=routing_key,
                delivery_tag=1,
            ),
            header=pamqp.ContentHeader(
                properties=pamqp.specification.Basic.Properties(reply_to=reply_to, correlation_id=correlation_id),
            ),
            body=json.dumps(data, default=utils.to_serializable).encode(),
            channel='1',
        ),
    )


@pytest.fixture
def aioresponses_mock():
    with aioresponses(passthrough=[f'http://127.0.0.1:{settings.SERVER_PORT}']) as aio_mock:
        yield aio_mock
