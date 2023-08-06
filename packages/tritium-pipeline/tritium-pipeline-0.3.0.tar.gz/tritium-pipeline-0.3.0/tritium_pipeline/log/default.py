from typing import TextIO
from pathlib import Path
from logging import Logger, FileHandler, Formatter, getLogger, INFO, StreamHandler
from tritium_pipeline.algebra.types.log import LogWriter, LogEntry, Out


def create_default_logger(filename: str | Path | TextIO, name: str | None = None) -> LogWriter:
    logger: Logger = getLogger(name if name else 'tritium_pipeline')
    handler: FileHandler | StreamHandler = FileHandler(filename) if isinstance(filename, (str, Path)) else StreamHandler(filename)
    formatter: Formatter = Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler.setLevel(INFO)
    logger.setLevel(INFO)

    def write_log(entry: LogEntry[Out], **metadata) -> LogEntry[Out]:
        logger.info(entry.prepare(**metadata))
        return entry

    return write_log
