from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import string

def render_text_to_image(char, font_path, size):
    img = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size)
    w, h = draw.textsize(char, font=font)
    draw.text(((size - w) // 2, (size - h) // 2), char, fill=255, font=font)
    return np.array(img)

def get_contours(image_array):
    contours, _ = cv2.findContours(image_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

def contours_to_relative_points(contours):
    all_points = np.vstack(contours).squeeze()
    center_x = np.mean(all_points[:, 0])
    center_y = np.mean(all_points[:, 1])
    relative_points = []
    for contour in contours:
        points = contour.reshape(-1, 2)
        rel_pts = [(round(float(x - center_x), 4), round(float(y - center_y), 4)) for x, y in points]
        relative_points.append(rel_pts)
    return relative_points

def scale_points(points_list, scale):
    scaled = []
    for contour in points_list:
        scaled_contour = [(round(x * scale, 4), round(y * scale, 4)) for x, y in contour]
        scaled.append(scaled_contour)
    return scaled

def points_to_custom_format(points_list):
    s = ""
    for contour in points_list:
        for x, y in contour:
            s += f"[{x}:{y}]"
    s += ","
    return s

font_path = "C:/Windows/Fonts/arial.ttf"  # 環境に合わせて変更
font_size = 100
scale = 1 / font_size

lower_digits = string.ascii_lowercase + string.digits
symbols = r"""!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
upper_symbols = string.ascii_uppercase + symbols

def process_chars(chars, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for c in chars:
            img = render_text_to_image(c, font_path, font_size)
            contours = get_contours(img)
            if not contours:
                f.write("\n")
                continue
            rel_points = contours_to_relative_points(contours)
            scaled_points = scale_points(rel_points, scale)
            formatted = points_to_custom_format(scaled_points)
            f.write(formatted + "\n")

process_chars(lower_digits, "lower_digit.txt")
process_chars(upper_symbols, "upper_symbol.txt")

print("全データのテキストファイル作成が完了しました！")
