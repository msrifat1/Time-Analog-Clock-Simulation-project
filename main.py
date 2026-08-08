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

def calculate_clock_hands_and_frame(img, now, line_value, size=700):
    xc = size // 2
    yc = size // 2
    radius = 250

    # Draw Outer & Inner Circles
    midpoint_circle(img, xc, yc, radius, line_value)
    midpoint_circle(img, xc, yc, 8, line_value)

    # Draw Hour Marks
    for hour_mark in range(12):
        angle = math.radians(hour_mark * 30)
        x1 = xc + int(215 * math.sin(angle))
        y1 = yc - int(215 * math.cos(angle))
        x2 = xc + int(235 * math.sin(angle))
        y2 = yc - int(235 * math.cos(angle))
        bresenham_line(img, x1, y1, x2, y2, line_value)

    # Calculate Time & Angles
    hour = now.hour % 12
    minute = now.minute
    second = now.second

    hour_angle = hour * 30 + minute * 0.5
    minute_angle = minute * 6 + second * 0.1
    second_angle = second * 6

    # Calculate Endpoints
    hour_x = xc + int(140 * math.sin(math.radians(hour_angle)))
    hour_y = yc - int(140 * math.cos(math.radians(hour_angle)))

    minute_x = xc + int(190 * math.sin(math.radians(minute_angle)))
    minute_y = yc - int(190 * math.cos(math.radians(minute_angle)))

    second_x = xc + int(220 * math.sin(math.radians(second_angle)))
    second_y = yc - int(220 * math.cos(math.radians(second_angle)))

    return xc, yc, (hour_x, hour_y), (minute_x, minute_y), (second_x, second_y)

def render_clock(img, now, number_color, background_color, xc, yc, hour_pos, minute_pos, second_pos, size=700):
    plt.figure(figsize=(9, 9))
    plt.imshow(img, cmap="gray", origin="upper")

    # Draw Numbers 1-12
    for number in range(1, 13):
        angle = math.radians(number * 30)
        x = xc + int(185 * math.sin(angle))
        y = yc - int(185 * math.cos(angle))
        plt.text(x, y, str(number), fontsize=18, fontweight="bold", color=number_color, ha="center", va="center")

    # Draw Hands
    plt.plot([xc, hour_pos[0]], [yc, hour_pos[1]], linewidth=8, color="black" if background_color == "white" else "white")
    plt.plot([xc, minute_pos[0]], [yc, minute_pos[1]], linewidth=5, color="blue")
    plt.plot([xc, second_pos[0]], [yc, second_pos[1]], linewidth=2, color="red")
    plt.scatter(xc, yc, s=100, color="red")

    # Text Display
    date_text = now.strftime("%A, %d %B %Y")
    digital_time = now.strftime("%I:%M:%S %p")

    plt.text(xc, yc + 285, date_text, fontsize=15, color=number_color, ha="center", fontweight="bold")
    plt.text(xc, yc + 315, digital_time, fontsize=16, color=number_color, ha="center", fontweight="bold")
    plt.title("Real-Time Analog Clock\nBangladesh Standard Time (UTC+6)", fontsize=18, color=number_color, pad=20)

    plt.xlim(50, size - 50)
    plt.ylim(size - 50, 50)
    plt.axis("off")
    plt.show()
