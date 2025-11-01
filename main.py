import asyncio
import sys
import termios
import tty
from contextlib import contextmanager

MAP: dict[str, str] = {"a": "aa", "b": "bb", "c": "cc"}


def stuff(value: str) -> None:
    print(f"stuff({value})")


@contextmanager
def _raw_mode(stream):
    fileno = stream.fileno()
    old_attrs = termios.tcgetattr(fileno)
    try:
        tty.setcbreak(fileno)
        yield
    finally:
        termios.tcsetattr(fileno, termios.TCSADRAIN, old_attrs)


def _listen_for_keys() -> None:
    if not sys.stdin.isatty():
        raise RuntimeError("stdin must be a TTY to capture key presses directly.")
    with _raw_mode(sys.stdin):
        print("Listening for keys (a, b, c). Press Ctrl+C to exit.")
        while True:
            char = sys.stdin.read(1)
            if not char:
                continue
            key = char.lower()
            if key in MAP:
                stuff(MAP[key])


def main():
    try:
        _listen_for_keys()
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()
