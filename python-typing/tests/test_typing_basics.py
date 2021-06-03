import logging
import sys
from typing import Optional, Generic

import attr
from pydantic import BaseModel

logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("parso").setLevel(logging.WARNING)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def test_basic_show_a():
    # show basic typing hints in python
    pass


def test_show_attrs_validation():
    @attr.s(auto_attribs=True)
    class Dataclass:
        a: str = attr.ib()
        b: int = attr.ib()

    inst = Dataclass("asasa", 5)


def test_pydantic():
    class Dataclass(BaseModel):
        a: str
        b: int

    Dataclass(a="a", b=5)
    Dataclass(b="a", a=5)


def some_foo(a: Optional[str], b: int) -> str:
    pass
