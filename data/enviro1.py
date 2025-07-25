import math
import random
import time
from datetime import datetime, timedelta
from typing import List, Tuple

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def temps(size: int = 31, low: float = -32.0, high: float = 105.0, inc: float = 0.01) -> list[float]:
    """
    generates a list of random temperatures, setting sample size,
    low, high of the bounds, and an increment threshold
    :param size:
    :param low:
    :param high:
    :param inc:
    :return:
    """
    return bounded_rand(size=size, low=low, high=high, threshold=inc, start=0)


def temp_time_series(size: int = 31, low: float = -32.0, high: float = 105.0, inc: float = 0.01) -> list[tuple[datetime, float]]:
    """
    same as temps() except this latches a timestamp to each sample
    :param size:
    :param low:
    :param high:
    :param inc:
    :return:
    """
    tmps = temps(size=size, low=low, high=high, inc=0.1)
    tt = []
    ts = datetime.now()
    for tmp in tmps:
        # get random adjustment to time delay
        dt = random.uniform(0.1, 1.0)
        # increment now() by random delay value
        ts += timedelta(seconds=dt)
        tt.append((ts, tmp))
        # no longer worth using, as this will create long runtimes
        # time.sleep(random.uniform(0.1, 1.0))

    return tt


def bounded_rand(size: int = 31, low: float = -1.0, high: float = 1.0, threshold: float = 0.01, start: float = None,
                 rng: random.Random = None) -> list[float]:
    """
    generate a fixed length list of floats within a range
    where the delta between item value <= threshold
    :param size: number of sample items
    :param low: lower bounds
    :param high: upper bounds
    :param threshold: max delta between values
    :param start: start value between bounds, if not provided select random within range
    :param rng: optional random instance (for reproducibility).
    :return: list of floats
    """
    if size <= 0:
        return []

    if low > high:
        raise ValueError("`low` must be less than `high`")
    if threshold <= 0:
        raise ValueError("threshold must have a value greater than 0")

    r = rng or random.Random()
    vals = []

    prev = start if start is not None else r.uniform(low, high)
    prev = max(low, min(high, prev))  # clamping
    vals.append(prev)

    for _ in range(size - 1):
        lo = max(low, prev - threshold)
        hi = min(high, prev + threshold)
        # if lo > hi (can happen if threshold is tiny an we're pinned at bounds), reuse prev value
        if lo > hi:
            nxt = prev
        else:
            nxt = r.uniform(lo, hi)
        vals.append(nxt)
        prev = nxt

    return vals


def main():
    t = temp_time_series()
    X = [ts for ts, _ in t]
    y = [temp for _, temp in t]

    # t = temps(size=100, inc=0.1, low=-20.0, high=100.0)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(X, y, '.-')

    # tell matplotlib how to format the x-axis
    locator = mdates.AutoDateLocator()
    # formatter = mdates.AutoDateFormatter(locator)
    formatter = mdates.DateFormatter('%H:%M:%S.%f')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # rotate time labels
    fig.autofmt_xdate()

    # plt.xticks(rotation=45)
    plt.title('random temps')
    plt.show()


if __name__ == "__main__":
    main()
