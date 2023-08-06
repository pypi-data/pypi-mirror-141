from json import loads
from os.path import exists
from typing import Iterable, TextIO
from io import StringIO
from tritium_pipeline.algebra.types.log import LogEntry, In


def has_failed(entry: LogEntry[In]) -> bool:
    return entry.failed


def get_failed_items(log: Iterable[LogEntry[In]]) -> Iterable[LogEntry[In]]:
    return filter(has_failed, log)


def _get_stream(filename_or_stream: str | TextIO | StringIO, encoding: str | None = None) -> TextIO:
    if isinstance(filename_or_stream, str):
        return StringIO() if not exists(filename_or_stream) else open(filename_or_stream, encoding=encoding)
    if isinstance(filename_or_stream, StringIO):
        return StringIO(filename_or_stream.getvalue())
    else:
        return filename_or_stream


def read_log(filename_or_stream: str | TextIO, encoding: str | None = 'utf-8') -> Iterable[LogEntry[In]]:
    if isinstance(filename_or_stream, str) and not exists(filename_or_stream):
        return ()
    with _get_stream(filename_or_stream, encoding) as src:
        while True:
            line: str = src.readline()
            if not line:
                break
            else:
                yield LogEntry(**loads(line.strip()))
