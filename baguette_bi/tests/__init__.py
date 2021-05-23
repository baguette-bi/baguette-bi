import time
from typing import Callable


def wait_for(predicate: Callable, timeout: float, interval: float = 1.0):
    exc = None
    start = time.time()
    while time.time() - start < timeout:
        try:
            res = predicate()
            if res:
                return res
        except Exception as e:
            exc = e
        time.sleep(interval)
    if exc:
        raise exc
    else:
        raise TimeoutError("Condition not achieved")
