from __future__ import annotations

import json
from codecs import open
from pathlib import Path
from typing import TYPE_CHECKING

from . import item_to_test_id

if TYPE_CHECKING:
    from typing import List

    from _pytest.config import Config
    from _pytest.python import Function
    from _pytest.runner import CallInfo

_faillist: List[str] = []


def pytest_runtest_makereport(item: Function, call: CallInfo[None]) -> None:
    if call.when == "call" and call.excinfo:
        _faillist.append(item_to_test_id(item))


def pytest_unconfigure(config: Config) -> None:
    with open(str(Path(config.rootpath, "xfails.list")), "w", encoding="UTF-8") as f:
        json.dump(_faillist, f, indent=4)
