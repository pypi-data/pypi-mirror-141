import sys
from typing import Callable, cast

vesion: Callable[[str], str]
if sys.version_info < (3, 8):
    from importlib_metadata import PackageNotFoundError, version

    version = cast(Callable[[str], str], version)
else:
    from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("di")
except PackageNotFoundError:
    __version__ = "0.0.0"


import di.api as api  # noqa: E402
from di.container import Container  # noqa: E402
from di.dependant import Dependant, JoinedDependant, Marker  # noqa: E402
from di.executors import (  # noqa: E402
    AsyncExecutor,
    ConcurrentAsyncExecutor,
    SyncExecutor,
)

__all__ = (
    "api",
    "Container",
    "Dependant",
    "JoinedDependant",
    "ConcurrentAsyncExecutor",
    "AsyncExecutor",
    "SyncExecutor",
    "Marker",
)
