from typing import TypeVar, Generic, Callable, TypeAlias, Protocol,runtime_checkable
from datetime import datetime
from uuid import uuid4
from toolz import comp
from pydantic import BaseModel, Field


In = TypeVar('In')
Out = TypeVar('Out')
Intermediate = TypeVar('Intermediate')


class LogEntry(BaseModel, Generic[Out]):
    uuid: str = Field(default_factory=comp(str, uuid4))
    parent_id: str | None = None
    data: Out | Exception | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, str | int | bool | float] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed: bool = True

    def follow_up(self, item: In | Exception) -> 'LogEntry[In]':
        return LogEntry(
            parent_id=self.uuid,
            data=item,
            metadata={'error_type': type(item).__name__} if isinstance(item, Exception) else dict()
        )

    @property
    def failed(self) -> bool:
        return 'error_type' in self.metadata

    @property
    def forward_to(self) -> str | None:
        return self.metadata.get('forward_to')

    @classmethod
    def from_value(cls, value: In) -> 'LogEntry[In]':
        return LogEntry(data=value)

    def prepare(self, **metadata) -> str:
        copy: LogEntry = self.copy()
        if isinstance(copy.data, Exception):
            copy.data = str(copy.data)
        copy.metadata.update(metadata)
        return copy.json(ensure_ascii=False)


@runtime_checkable
class LogWriter(Protocol[Out]):
    def __call__(self, entry: LogEntry[Out], **metadata) -> LogEntry[Out]: ...


def no_log(entry: LogEntry[Out], **metadata) -> LogEntry[Out]:
    return entry.copy(update=dict(metadata=metadata))
