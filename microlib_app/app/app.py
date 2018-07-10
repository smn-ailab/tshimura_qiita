from datetime import datetime

from mtools.clock_util.local_time import get_local_time


def show_time() -> None:
    print(get_local_time('Asia/Tokyo'))


if __name__ == "__main__":
    print(get_local_time('Asia/Tokyo'))
