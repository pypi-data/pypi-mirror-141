from functools import wraps, partial
from typing import Callable, Iterable, Protocol, runtime_checkable
from tritium_pipeline.algebra.types.log import In, Out, LogEntry, Intermediate, LogWriter, no_log


@runtime_checkable
class Processor(Protocol[In, Out]):
    def __call__(self, value: LogEntry[In | Exception], write_log: LogWriter | None = None) -> Iterable[LogEntry[Out]]:
        ...


@runtime_checkable
class FixedProcessor(Protocol[In, Out]):
    def __call__(self, value: LogEntry[In | Exception]) -> Iterable[LogEntry[Out]]:
        ...


@runtime_checkable
class JobDistribution(Protocol[In, Out]):
    def map(
        self,
        processor: Processor[In, Out],
        jobs: Iterable[LogEntry[In]],
        write_log: LogWriter
    ) -> Iterable[LogEntry[Out]]:
        for job in jobs:
            for result in processor(job, write_log):
                yield result


class SerialDistribution(JobDistribution[In, Out]):
    pass


def create_processor(func: Callable[[In], Iterable[Out]], name: str | None = None) -> Processor[In, Out]:
    @wraps(func)
    def process(value: LogEntry[In | Exception], write_log: LogWriter = no_log) -> Iterable[LogEntry[Out]]:
        if (target := value.forward_to) and target != name:
            return value,
        if isinstance(value.data, Exception):
            return ()
        try:
            for result in func(value.data):
                try:
                    yield write_log(
                        value.follow_up(result),
                        processor=name
                    )
                except Exception as error:
                    yield write_log(value.follow_up(error), input_data=result, error=True, processor=name)
        except Exception as error:
            yield write_log(value.follow_up(error), error=True, processor=name)
    return process


def as_processor(name: str | None = None) -> Callable[[Callable[[In], Iterable[Out]]], Processor[In, Out]]:
    def wrapper(func: Callable[[In], Iterable[Out]]) -> Processor[In, Out]:
        return create_processor(func, name)
    return wrapper


def connect_processors(
    source: Processor[In, Intermediate],
    sink: Processor[Intermediate, Out],
    distribution: JobDistribution[Intermediate, Out] = SerialDistribution()
) -> Processor[In, Out]:
    def channel(value: LogEntry[In], write_log: LogWriter = no_log) -> Iterable[LogEntry[Out]]:
        return distribution.map(sink, source(value, write_log), write_log)
    return channel


@as_processor('_source')
def source_processor(value: In) -> Iterable[In]:
    yield value
