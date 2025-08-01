import csv
from datetime import datetime
from pathlib import Path

from odds.rand.enviro import temp_time_trending


def temp_trend_to_csv(p: Path, iterations: int = 10, **kwargs):
    with open(p, 'a', newline='') as fh:
        writer = csv.writer(fh)
        # write header
        writer.writerow(['run', 'timestamp', 'temperature'])
        for i in range(iterations):
            series = temp_time_trending(**kwargs)
            for ts, temp in series:
                writer.writerow([i + 1, ts.isoformat(), temp])

            fh.flush()

    print(f"wrote data to {p.__str__()}.")


def main():
    temp_trend_to_csv(
        Path.home().joinpath('.databox', f'enviro2_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'),
        iterations=100,
        size=50,
        low=-20.0,
        high=40.0,
        delta=0.05,
        trend_per_sec=0.002
    )


if __name__ == "__main__":
    main()
