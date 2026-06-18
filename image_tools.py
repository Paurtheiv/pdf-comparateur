from pdf2image import convert_from_path, convert_from_bytes
from PIL import ImageChops, ImageDraw

def convert_pdf_to_images(pdf_input, dpi=300):
    if isinstance(pdf_input, bytes):
        return convert_from_bytes(pdf_input, dpi=dpi)
    elif isinstance(pdf_input, str):
        return convert_from_path(pdf_input, dpi=dpi)
    else:
        raise TypeError("pdf_input doit être un chemin (str) ou bytes")

def get_diff_boxes(image1, image2, threshold=10, min_area=100, margin=20):
    diff = ImageChops.difference(image1.convert("RGB"), image2.convert("RGB")).convert("L")
    diff = diff.point(lambda p: 255 if p > threshold else 0)

    diff_pixels = diff.load()
    width, height = diff.size

    visited = set()
    boxes = []

    for y in range(height):
        for x in range(width):
            if diff_pixels[x, y] == 255 and (x, y) not in visited:
                stack = [(x, y)]
                min_x, min_y, max_x, max_y = x, y, x, y

                while stack:
                    px, py = stack.pop()
                    if (0 <= px < width and 0 <= py < height and
                        diff_pixels[px, py] == 255 and (px, py) not in visited):
                        visited.add((px, py))
                        min_x = min(min_x, px)
                        min_y = min(min_y, py)
                        max_x = max(max_x, px)
                        max_y = max(max_y, py)

                        for nx in range(px-1, px+2):
                            for ny in range(py-1, py+2):
                                stack.append((nx, ny))

                area = (max_x - min_x) * (max_y - min_y)
                if area >= min_area:
                    min_x = max(min_x - margin, 0)
                    min_y = max(min_y - margin, 0)
                    max_x = min(max_x + margin, width)
                    max_y = min(max_y + margin, height)
                    boxes.append((min_x, min_y, max_x, max_y))

    return boxes

def draw_diff_boxes(image, boxes, outline_color="red", outline_width=3):
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)
    for box in boxes:
        draw.rectangle(box, outline=outline_color, width=outline_width)
    return img_copy
