from cairosvg import svg2png
from PIL import Image, ImageOps
import sys
import io
import pathlib

SIZE = 128
RATIO = 0.6


def simpleicons2image(name: str, size: int = SIZE):
    print(f"getting {name} from simpleicons...")
    url = f"https://simpleicons.org/icons/{name}.svg"
    print(f"{name} recieved.")
    try:
        buffer = svg2png(url=url, output_height=size, output_width=size)
        image = Image.open(io.BytesIO(buffer)).convert("RGBA")
        print(f"{name} converted to Image")
        return image
    except Exception as e:
        print(f"cannot convert {name}. error: {e}")
        return False


def image_color(shape, color_front, color_back):
    mask = shape.convert("L")
    front = Image.new("RGBA", shape.size, color_front)
    back = Image.new("RGBA", shape.size, color_back)
    result = Image.composite(front, back, mask)

    return result


def image_bg(image, color):
    bg = Image.new("RGBA", (SIZE, SIZE), color)
    side = int(SIZE * RATIO)
    pos = SIZE // 2 - side // 2
    bg.paste(image, (pos, pos), image)

    return bg


def image_invert(image):
    if image.mode == "RGBA":
        r, g, b, a = image.split()
        rgb_image = Image.merge("RGB", (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        result = Image.merge("RGBA", (r2, g2, b2, a))
    else:
        result = ImageOps.invert(image)
    return result


def rainmeterpng(name, color):
    shape = simpleicons2image(name)
    if shape:
        shape_resized = ImageOps.scale(shape, RATIO, Image.LANCZOS)

        mask_uninverted = image_bg(shape_resized, "#ffffffff")
        mask = image_invert(mask_uninverted)

        image_main = image_color(mask, "#ffffffff", color)
        image_over = image_color(mask, color, "#ffffffff")

        pathlib.Path(f"./icons/{name}").mkdir(exist_ok=True)

        image_main.save(f"./icons/{name}/{name}.png", "PNG")
        image_over.save(f"./icons/{name}/{name}_over.png", "PNG")
        print(f"Saved {name}.png and {name}_over.png with given background color.")


def simpleicons2png(names):
    for name in names:
        buffer = simpleicons2image(name)
        if buffer:
            image_bg(buffer, "#ffffffff")


def main():
    if len(sys.argv) > 2:
        type = sys.argv[1]
        names = sys.argv[2:]
        print(names)
        if type == "firefox":
            simpleicons2png(names)
        elif type == "rainmeter":
            rainmeterpng(names[0], names[1])
        elif type == "-h" or type == "--help":
            print(
                """
            firefox, discord
            """
            )
    else:
        print("no name given. abort.")


if __name__ == "__main__":
    main()
