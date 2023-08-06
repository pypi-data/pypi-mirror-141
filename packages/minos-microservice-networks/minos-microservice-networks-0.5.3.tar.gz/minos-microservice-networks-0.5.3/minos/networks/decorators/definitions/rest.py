from abc import (
    ABC,
)
from typing import (
    Final,
    Iterable,
)

from .abc import (
    EnrouteDecorator,
)
from .kinds import (
    EnrouteDecoratorKind,
)


class RestEnrouteDecorator(EnrouteDecorator, ABC):
    """Rest Enroute class"""

    def __init__(self, url: str, method: str):
        self.url = url
        self.method = method

    def __iter__(self) -> Iterable:
        yield from (
            self.url,
            self.method,
        )


class RestCommandEnrouteDecorator(RestEnrouteDecorator):
    """Rest Command Enroute class"""

    KIND: Final[EnrouteDecoratorKind] = EnrouteDecoratorKind.Command


class RestQueryEnrouteDecorator(RestEnrouteDecorator):
    """Rest Query Enroute class"""

    KIND: Final[EnrouteDecoratorKind] = EnrouteDecoratorKind.Query
