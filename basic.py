from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Custom


class RGBWFixture:
    """
    Generic 4-channel RGBW fixture:
        ch 1 = R
        ch 2 = G
        ch 3 = B
        ch 4 = W
    """

    def __init__(self, controller, name="RGBW", start_channel=1):
        # num_channels=4 gives us 4 DMX channels
        self.fix = controller.add_fixture(
            Custom,
            name=name,
            channels=4,
            start_channel=start_channel,
        )

    def set_rgbw(self, r, g, b, w, fade_ms=0):
        self.fix.set_channel(0, max(0, min(255, r)))
        self.fix.set_channel(1, max(0, min(255, g)))
        self.fix.set_channel(2, max(0, min(255, b)))
        self.fix.set_channel(3, max(0, min(255, w)))

    def set_rgb(self, r, g, b, fade_ms=0):
        w, _ = self.fix.channels[4]["value"]
        self.set_rgbw(r, g, b, w, fade_ms)

    def set_white(self, w, fade_ms=0):
        r, _ = self.fix.channels[1]["value"]
        g, _ = self.fix.channels[2]["value"]
        b, _ = self.fix.channels[3]["value"]
        self.set_rgbw(r, g, b, w, fade_ms)


if __name__ == "__main__":
    # Example usage:
    dmx = OpenDMXController()
    # Example usage: fixture starting at DMX address 1
    rgbw = RGBWFixture(dmx, start_channel=1)

    # r g b w
    rgbw.set_rgbw(0, 0, 0, 255)

    # …keep the program alive so the DMX thread keeps running:
    # dmx.web_control()
    dmx.sleep_till_enter()
    dmx.close()
