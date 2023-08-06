from typing import Iterable, TextIO
from tritium_pipeline.algebra.types.log import LogEntry, In


def has_failed(entry: LogEntry[In]) -> bool:
    return entry.failed


def get_failed_items(log: Iterable[LogEntry[In]]) -> Iterable[LogEntry[In]]:
    return filter(has_failed, log)


def get_repeat_candidates(log: Iterable[LogEntry[In]]) -> Iterable[LogEntry[In]]:
    parent_ids: set[str] = {entry.parent_id for entry in get_failed_items(log)}
