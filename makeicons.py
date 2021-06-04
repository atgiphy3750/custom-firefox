from cairosvg import svg2png
from PIL import Image, ImageOps
import numpy as np
import sys
import io


def simpleicons2image(name: str, size: int = 512):
    print(f"getting {name} from simpleicons...")
    url = f"https://simpleicons.org/icons/{name}.svg"
    print(f"{name} recieved.")
    try:
        buffer = svg2png(url=url,
                         output_height=size,
                         output_width=size)
        image = Image.open(io.BytesIO(buffer)).convert("RGBA")
        print(f"{name} converted to Image")
        return image
    except Exception as e:
        print(f"cannot convert {name}. error: {e}")
        return False


def image_color(image, color):
    data = np.array(image)
    r, g, b, a = data.T
    area = (r == 255) & (g == 255) & (b == 255)
    data[..., :-1][area.T] = color
    result = Image.fromarray(data)
    return result


def image_invert(image) -> Image:
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb_image = Image.merge('RGB', (r, g, b))

        inverted_image = ImageOps.invert(rgb_image)

        r2, g2, b2 = inverted_image.split()

        inverted = Image.merge('RGBA', (r2, g2, b2, a))
    else:
        inverted = ImageOps.invert(image)
    return inverted


def image_bg(image, name: str, color):
    bg = Image.new("RGBA", image.size, color)
    result = Image.alpha_composite(bg, image)
    return result


def rainmeterpng(name, color):
    image = simpleicons2image(name)
    if image:
        image_main_shape = image_color(image, color)
        image_main = image_bg(image_main_shape, name, "#ffffff00")

        image_over_shape = image_color(image, "#ffffff00")
        image_over = image_bg(image_over_shape, name, color)

        image_main.save(f"./icons/{name}.png", "PNG")
        image_over.save(f"./icons/{name}_over.png", "PNG")
        print(f"Saved {name}.png with given background color.")


def simpleicons2png(names):
    for name in names:
        buffer = simpleicons2image(name)
        if buffer:
            image_bg(buffer, name, "#ffffffff")


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
            print("""
            firefox, discord
            """)
    else:
        print("no name given. abort.")


if __name__ == "__main__":
    main()
