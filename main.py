import numpy as np
import matplotlib.pyplot as plt
import math
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from IPython.display import clear_output


def midpoint_circle(img, xc, yc, r, value=0):
    x = 0
    y = r
    p = 1 - r

    while x <= y:
        points = [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x)
        ]

        for px, py in points:
            if 0 <= px < img.shape[1] and 0 <= py < img.shape[0]:
                img[py, px] = value

        if p < 0:
            p = p + 2 * x + 3
        else:
            p = p + 2 * (x - y) + 5
            y = y - 1

        x = x + 1


def bresenham_line(img, x1, y1, x2, y2, value=0):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    error = dx - dy

    while True:
        if 0 <= x1 < img.shape[1] and 0 <= y1 < img.shape[0]:
            img[y1, x1] = value

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * error

        if e2 > -dy:
            error -= dy
            x1 += sx

        if e2 < dx:
            error += dx
            y1 += sy


def prepare_clock_canvas(size=700):
    # Bangladesh time
    now = datetime.now(ZoneInfo("Asia/Dhaka"))

    # Day / Night Mode
    current_hour = now.hour
    if 6 <= current_hour < 18:
        background_color = "white"
        clock_color = "black"
        number_color = "black"
    else:
        background_color = "black"
        clock_color = "white"
        number_color = "white"

    background_value = 255 if background_color == "white" else 0
    img = np.ones((size, size), dtype=np.uint8) * background_value

    line_value = 0 if background_color == "white" else 255

    return img, now, number_color, line_value, background_color

            