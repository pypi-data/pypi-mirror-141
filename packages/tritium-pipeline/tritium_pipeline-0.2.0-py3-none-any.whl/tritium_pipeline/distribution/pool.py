from typing import Iterable
from functools import partial
from toolz import comp
from multiprocessing.pool import ThreadPool, Pool
from tritium_pipeline.algebra.types.processor import JobDistribution, In, Out, FixedProcessor, LogEntry, Processor, LogWriter


class ThreadPoolDistribution(JobDistribution[In, Out]):
    def __init__(self, pool: ThreadPool):
        self.pool: ThreadPool = pool

    def map(
        self,
        processor: Processor[In, Out],
        jobs: Iterable[LogEntry[In]],
        write_log: LogWriter
    ) -> Iterable[LogEntry[Out]]:
        for results in self.pool.imap_unordered(partial(processor, write_log=write_log), jobs, 1):
            for result in results:
                yield result


class ProcessPoolDistribution(JobDistribution[In, Out]):
    def __init__(self, pool: Pool):
        self.pool: Pool = pool

    def map(
        self,
        processor: Processor[In, Out],
        jobs: Iterable[LogEntry[In]],
        write_log: LogWriter
    ) -> Iterable[LogEntry[Out]]:
        return [
            result
            for results in self.pool.imap_unordered(comp(list, partial(processor, write_log=write_log)), jobs, 1)
            for result in results
        ]


def create_thread_pool_distribution(pool: ThreadPool | int) -> ThreadPoolDistribution:
    return ThreadPoolDistribution(pool if isinstance(pool, ThreadPool) else ThreadPool(pool))


def create_process_pool_distribution(pool: Pool | int) -> ProcessPoolDistribution:
    return ProcessPoolDistribution(pool if isinstance(pool, Pool) else Pool(pool))
