# The MIT License (MIT)
#
# Copyright (c) 2019 Limor Fried for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`rect`
================================================================================

Various common shapes for use with displayio - Rectangle shape!


* Author(s): Limor Fried

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes.git"


class RoundRect(displayio.TileGrid):
    """A round-corner rectangle, top left corner is (x, y) and size of width, height.
    r is the radius of the rounded corner. Stroke is used for the outline, and will
    not change outer bound size set by width and height. Fill can be a hex value
    for the color or None for transparent. Outline can be a hex value for the color
    or None for no outline."""
    def __init__(self, x, y, width, height, r, *, fill=None, outline=None, stroke=1): # pylint: disable=too-many-arguments
        self._palette = displayio.Palette(3)
        self._palette.make_transparent(0)
        self._bitmap = displayio.Bitmap(width, height, 3)

        if fill is not None:
            for i in range(0, width):   # draw the center chunk
                for j in range(r, height-r):   # draw the center chunk
                    self._bitmap[i, j] = 2
            self._helper(r, r, r, color=2, fill=True,
                         x_offset=width-2*r-1, y_offset=height-2*r-1)
            self._palette[2] = fill
        else:
            self._palette.make_transparent(2)

        if outline is not None:
            self._palette[1] = outline
            # draw flat sides
            for w in range(r, width-r):
                for line in range(stroke):
                    self._bitmap[w, line] = 1
                    self._bitmap[w, height-line-1] = 1
            for _h in range(r, height-r):
                for line in range(stroke):
                    self._bitmap[line, _h] = 1
                    self._bitmap[width-line-1, _h] = 1
            # draw round corners
            self._helper(r, r, r, color=1, stroke=stroke,
                         x_offset=width-2*r-1, y_offset=height-2*r-1)

        super().__init__(self._bitmap, pixel_shader=self._palette, position=(x, y))


    # pylint: disable=invalid-name, too-many-locals, too-many-branches
    def _helper(self, x0, y0, r, *, color, x_offset=0, y_offset=0,
                stroke=1, cornerflags=0xF, fill=False):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            if cornerflags & 0x8:
                if fill:
                    for w in range(x0-y, x0+y+x_offset):
                        self._bitmap[w, y0+x+y_offset] = color
                    for w in range(x0-x, x0+x+x_offset):
                        self._bitmap[w, y0+y+y_offset] = color
                else:
                    for line in range(stroke):
                        self._bitmap[x0-y+line, y0+x+y_offset] = color
                        self._bitmap[x0-x, y0+y+y_offset-line] = color
            if cornerflags & 0x1:
                if fill:
                    for w in range(x0-y, x0+y+x_offset):
                        self._bitmap[w, y0-x] = color
                    for w in range(x0-x, x0+x+x_offset):
                        self._bitmap[w, y0-y] = color
                else:
                    for line in range(stroke):
                        self._bitmap[x0-y+line, y0-x] = color
                        self._bitmap[x0-x, y0-y+line] = color
            if cornerflags & 0x4:
                for line in range(stroke):
                    self._bitmap[x0+x+x_offset, y0+y+y_offset-line] = color
                    self._bitmap[x0+y+x_offset-line, y0+x+y_offset] = color
            if cornerflags & 0x2:
                for line in range(stroke):
                    self._bitmap[x0+x+x_offset, y0-y+line] = color
                    self._bitmap[x0+y+x_offset-line, y0-x] = color
    # pylint: enable=invalid-name, too-many-locals, too-many-branches

    @property
    def fill(self):
        return self._palette[2]

    @fill.setter
    def fill(self, color):
        if color is None:
            self._palette.make_transparent(2)
        else:
            self._palette[2] = color

    @property
    def outline(self):
        return self._palette[1]

    @outline.setter
    def outline(self, color):
        if color is None:
            self._palette.make_transparent(1)
        else:
            self._palette[1] = color


    @property
    def x(self):
        """The x coordinate of the position"""
        return self.position[0]

    @x.setter
    def x(self, x):
        self.position = (x, self.position[1])

    @property
    def y(self):
        """The y coordinate of the position"""
        return self.position[1]

    @y.setter
    def y(self, y):
        self.position = (self.position[0], y)
