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