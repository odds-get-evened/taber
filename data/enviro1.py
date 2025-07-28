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


def temp_time_trending(size: int = 31, low: float = -1.0, high: float = 1.0, delta: float = 0.01,
                       trend_per_sec: float = 0.001, trend_dir: int = 0) -> List[Tuple[datetime, float]]:
    """
    similar to temps, but latches timestamp to each sample, with varying time deltas.
    allows for trending a noisy sample series, which can be either, downward, random,
    or upward trending.
    :param size:
    :param low:
    :param high:
    :param delta:
    :param trend_per_sec: how long a trend will last
    :param trend_dir: {'downward': -1, 'random (default)': 0, 'upward': 1}
    :return:
    """
    # generate noisy base series
    noise_series = bounded_rand(size=size, low=low, high=high, threshold=delta)

    # decide overall trend direction
    if trend_dir == 0:
        sign = random.choice([-1, 1])
    elif trend_dir in (-1, 1):
        sign = trend_dir
    else:
        raise ValueError('must be -1, 0, or 1')
    print(f"trend {sign}")

    ts_now = datetime.now()
    res = []
    elapsed = 0.0       # total seconds elapsed

    for temp in noise_series:
        # advance time by a small delta
        time_delta = random.uniform(0.1, 1.0)
        ts_now += timedelta(seconds=time_delta)
        elapsed += time_delta

        # apply signed drift
        temp_trend = temp + sign * trend_per_sec * elapsed
        res.append((ts_now, temp_trend))

    return res


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
    t2 = temp_time_trending(size=256, low=-20.0, high=105.0, trend_per_sec=0.005)
    X2 = [ts for ts, _ in t2]
    y2 = [temp for _, temp in t2]
    print(t2)

    # t = temps(size=100, inc=0.1, low=-20.0, high=100.0)
    fig, ax = plt.subplots(figsize=(9, 4))
    # ax.plot(X1, y1, linestyle='solid', label='temps')
    ax2 = ax.twinx()
    ax2.plot(X2, y2, linestyle='dotted', label='trending temps')

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
