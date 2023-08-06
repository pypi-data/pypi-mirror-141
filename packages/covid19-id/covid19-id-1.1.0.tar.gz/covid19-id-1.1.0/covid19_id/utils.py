import cattr

try:
    import ujson as json
except ImportError:
    import json  # type: ignore[no-redef]
from datetime import date, datetime
from dateutil.parser import parse as parse_datetime
from typing import Any, Generic, TypeVar
from urllib.request import urlopen, Request

from . import __version__

VInt = TypeVar("VInt", bound=int)


class ValueInt(Generic[VInt]):
    pass


def get_headers():
    return {
        "Connection": "keep-alive",
        "User-Agent": f"pypi.org/project/covid19-id/{__version__}",
    }


def _get_data(url: str, to_json: bool = True) -> Any:
    data: Any = None
    req = Request(url=url, headers=get_headers())
    with urlopen(req) as response:
        data = response.read()
    if to_json:
        return json.loads(data)
    return data


def register_hooks():
    cattr.register_structure_hook(date, lambda d, t: parse_datetime(d).date())
    cattr.register_structure_hook(datetime, lambda d, t: parse_datetime(d))
    cattr.register_structure_hook(ValueInt, lambda d, t: d["value"])
