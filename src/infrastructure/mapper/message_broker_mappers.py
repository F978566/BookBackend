from dataclasses import asdict
from typing import Any

import orjson

from src.domain.common.event.event import Event


def map_event_to_broker_message(event: Event) -> bytes:
    return orjson.dumps(event)


def map_event_to_json(event: Event) -> dict[str, Any]:
    return asdict(event) # type: ignore
