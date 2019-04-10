import os
import random

import arabic_reshaper
from PIL.ImageDraw import Draw
from bidi.algorithm import get_display
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
DEFAULT_FONT = os.path.join(DATA_DIR, 'xbn.TTF')


def image(text, font_size=26, width=160, height=60):
    font = ImageFont.truetype(DEFAULT_FONT, font_size)
    background = random_color(238, 255)
    color = random_color(10, 200, random.randint(220, 255))

    captcha_image = Image.new('RGB', (width, height), background)
    reshaped_text = arabic_reshaper.reshape(text)  # correct its shape
    bidi_text = get_display(reshaped_text)  # correct its direction

    draw = ImageDraw.Draw(captcha_image)
    draw.text((30, 10), bidi_text, (0, 0, 0), font=font)

    captcha_image = create_noise_curve(captcha_image, color)
    captcha_image = create_noise_dots(captcha_image, color)

    return captcha_image


def create_noise_curve(rgb_image, color):
    w, h = rgb_image.size
    x1 = random.randint(0, int(w / 5))
    x2 = random.randint(w - int(w / 5), w)
    y1 = random.randint(int(h / 5), h - int(h / 5))
    y2 = random.randint(y1, h - int(h / 5))
    points = [x1, y1, x2, y2]
    end = random.randint(160, 200)
    start = random.randint(0, 20)
    Draw(rgb_image).arc(points, start, end, fill=color)
    return rgb_image


def create_noise_dots(rgb_image, color, width=3, number=30):
    draw = Draw(rgb_image)
    w, h = rgb_image.size
    while number:
        x1 = random.randint(0, w)
        y1 = random.randint(0, h)
        draw.line(((x1, y1), (x1 - 1, y1 - 1)), fill=color, width=width)
        number -= 1
    return rgb_image


def random_color(start, end, opacity=None):
    red = random.randint(start, end)
    green = random.randint(start, end)
    blue = random.randint(start, end)
    if opacity is None:
        return red, green, blue
    return red, green, blue, opacity
