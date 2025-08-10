type TimestampMsWindow = tuple[int, int]


def split_time_window(
    window: TimestampMsWindow,
) -> tuple[TimestampMsWindow, TimestampMsWindow]:
    if window[0] >= window[1]:
        raise ValueError(
            "The first timestamp of the tuple must be earlier than the second timestamp."
        )

    if window[1] - window[0] < 3:
        raise ValueError("The difference between two timestamps must be at least 3 ms.")

    start = window[0]
    mid = (window[0] + window[1]) // 2
    end = window[1]

    return (start, mid), (mid + 1, end)
