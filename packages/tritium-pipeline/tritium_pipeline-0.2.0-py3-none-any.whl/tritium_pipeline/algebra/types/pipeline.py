from typing import Generic, Callable, Iterable
from pydantic import BaseModel
from tritium_pipeline.algebra.types.log import In, Out, Intermediate, LogWriter, no_log, LogEntry
from tritium_pipeline.algebra.types.processor import connect_processors, Processor, create_processor, source_processor


class Pipeline(BaseModel, Generic[In, Out]):
    write_log: LogWriter
    processor: Processor[In, Out]
    pipe: list[str]

    class Config:
        arbitrary_types_allowed: bool = True

    def attach_process(
        self,
        endpoint: Processor[Out, Intermediate],
        name: str | None = None
    ) -> 'Pipeline[Out, Intermediate]':
        return Pipeline(
            write_log=self.write_log, processor=connect_processors(self.processor, endpoint),
            pipe=self.pipe + [name if name else endpoint.__name__]
        )

    def attach(self, endpoint: Callable[[Out], Iterable[Intermediate]], name: str) -> 'Pipeline[Out, Intermediate]':
        return self.attach_process(create_processor(endpoint, name), name)

    def feed(self, item: In) -> Iterable[Out | Exception]:
        return (
            entry.data for entry in self.processor(LogEntry.from_value(item), self.write_log)
        )

    def inject(self, items: Iterable[In]) -> Iterable[Out | Exception]:
        for item in items:
            for result in self.processor(LogEntry.from_value(item), self.write_log):
                yield result.data


def create_pipeline(write_log: LogWriter = no_log) -> Pipeline[In, In]:
   return Pipeline(write_log=write_log, processor=source_processor, pipe=['_source'])



