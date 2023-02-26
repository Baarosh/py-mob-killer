import cv2 as cv
import yaml


def load_yaml_document(path):
    with open(path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Failed to load yaml document. Traceback: {exc}")


def dump_yaml_document(data, path):
    with open(path, "w") as stream:
        try:
            yaml.safe_dump(data, stream)
        except yaml.YAMLError as exc:
            print(f"Failed to dump yaml document. Traceback: {exc}")


def draw_rectangles(image, rectangles):
    for x, y, width, height in rectangles:
        top_left = (x, y)
        bottom_right = (x + width, y + height)
        cv.rectangle(image, top_left, bottom_right, (255, 0, 255), 4)


def get_center_points(rectangles):
    points = []
    for x, y, width, height in rectangles:
        center_x = x + int(width / 2)
        center_y = y + int(height / 2)
        points.append((center_y, center_x))
    return tuple(points)


def show_image(window_name, image):
    cv.imshow(window_name, image)
