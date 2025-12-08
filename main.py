import asyncio
import sys
import termios
import tty
from contextlib import contextmanager

from PyDMXControl.controllers import OpenDMXController

from basic import RGBWFixture

dmx = OpenDMXController()
rgbw = RGBWFixture(dmx, start_channel=1)
dmx.web_control()

MAP: dict[str, tuple[int, int, int, int]] = {
    "r": (255, 0, 0, 0),
    "g": (0, 255, 0, 0),
    "b": (0, 0, 255, 0),
    "w": (0, 0, 0, 255),
}


def stuff(color: tuple[int, int, int, int]) -> None:
    rgbw.set_rgbw(*color)
    print(f"Set color to R:{color[0]} G:{color[1]} B:{color[2]} W:{color[3]}")


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
