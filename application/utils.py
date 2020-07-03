import datetime
import functools


@functools.singledispatch
def to_serializable(arg) -> str:
    """Generic method to make passed argument serializable in json"""
    return str(arg)


@to_serializable.register
def prepare_datetime(arg: datetime.date) -> str:
    """Make datetime serializable in json"""
    return arg.isoformat()
