"""Center the generated koi in a wide blue pond for a full-width README image."""
import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageSequence


BACKGROUND = "#1E5AA8"
POND_WIDTH = 1600


def flatten(image):
    rgba = image.convert("RGBA")
    background = Image.new("RGBA", (max(POND_WIDTH, rgba.width), rgba.height), BACKGROUND)
    background.alpha_composite(rgba, dest=((background.width - rgba.width) // 2, 0))
    return background.convert("RGB")


def add_background(directory):
    frames, durations = [], []
    with Image.open(directory / "koi.gif") as animation:
        loop = animation.info.get("loop", 0)
        for frame in ImageSequence.Iterator(animation):
            durations.append(frame.info["duration"])
            opaque = flatten(frame).quantize(colors=256, dither=Image.Dither.NONE)
            opaque.info.clear()
            frames.append(opaque)
    gif = BytesIO()
    frames[0].save(gif, format="GIF", save_all=True, append_images=frames[1:],
                   duration=durations, loop=loop, disposal=1, optimize=False)
    png = BytesIO()
    with Image.open(directory / "koi.png") as still:
        flatten(still).save(png, format="PNG")
    for name, content in (("koi.gif", gif), ("koi.png", png)):
        path = directory / name
        temporary = path.with_name(name + ".tmp")
        temporary.write_bytes(content.getvalue())
        temporary.replace(path)
    print(f"Applied {BACKGROUND} background to {len(frames)} GIF frames and PNG")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    add_background(parser.parse_args().directory)
