from typing import Any, Protocol


class Parser(Protocol):
    def parse(self, *args, **kwargs: dict[Any, Any]) -> Any: ...
