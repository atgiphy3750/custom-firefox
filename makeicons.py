from cairosvg import svg2png
from PIL import Image
import sys
import io

def simpleicons2png(name: str, size: int = 512):
    print(f"getting {name} from simpleicons...")
    url = f"https://simpleicons.org/icons/{name}.svg"
    print(f"{name} recieved.")
    try:
        buffer = svg2png(url=url,
                output_height=size,
                output_width=size)
        print(f"{name} converted to buffer")
        return buffer
    except Exception as e:
        print(f"cannot convert {name}. error: {e}")
        return False


def remove_alpha(buffer, name: str):
    image = Image.open(io.BytesIO(buffer)).convert("RGBA")
    bg = Image.new("RGBA", image.size, (255, 255, 255))
    result = Image.alpha_composite(bg, image)
    result.save(f"./icons/{name}.png", "PNG")
    print(f"removed alpha and saved {name}.png.")


def main():
    if len(sys.argv) > 1:
        svgnames = sys.argv[1:]
        for svgname in svgnames:
            buffer = simpleicons2png(svgname)
            if buffer:
                remove_alpha(buffer, svgname)

    else:
        print("no name given. abort.")


if __name__ == "__main__":
    main()
