from typing import Any, Callable, List, Tuple, Generic, TypeVar
from math import floor
from utils.reprandom import rr
import pandas as pd

T = TypeVar("T")


class Job(Generic[T]):
    def __init__(
        self,
        fun: Callable[..., T],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._fun = fun
        self._args = args
        self._kwargs = kwargs

    def run(self) -> T:
        return self._fun(*self._args, **self._kwargs)


class RandomizedExecutor(Generic[T]):
    def __init__(self, repetitions: int = 1):
        self._jobs: List[Tuple[str, Job[T]]] = []
        self._results: List[Tuple[str, T]] = []
        self._repetitions: int = repetitions
        self._resultsDict: dict = {}
    def add(self, key: str, job: Job[T]):
        lKey=[]
        for _ in range(self._repetitions):
            self._jobs.append((key, job))
            lKey.append(key)
        lKey=list(set(lKey))
        keys=list(self._resultsDict.keys())
        for key in lKey:
            if(key not in keys):
                self._resultsDict.update({key:[]})
    def exec_all(self, verbose: bool = True) -> None:
        cur_progress = 0
        max_progress = len(self._jobs)
        rr.shuffle(self._jobs)
        for key, job in self._jobs:
            result = job.run()
            self._results.append((key, result))
            self._resultsDict[key].append(result)
            cur_progress += 1
            percent = cur_progress / max_progress * 100
            if verbose:
                print(f"\r{floor(percent)}%" + 10 * " ", end="")
        if verbose:
            print()
    def get_results(self, key: str) -> List[T]:
        results: List[T] = []
        for key2, result in self._results:
            if key == key2:
                results.append(result)
        return results

    def get_df(self)->pd.DataFrame:
        return pd.DataFrame(self._resultsDict)
