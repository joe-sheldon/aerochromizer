import argparse, sys
from PIL import Image, ImageEnhance
from utils import adjust_color, rgb_to_brr, change_color_temperature


def generate_faux_aerochrome(
        img: Image,
        wb1: int,
        wb2: int,
        red: float,
        green: float,
        blue: float,
        contrast: float,
        saturation: float,
        brightness: float,
) -> Image:
    intermediate_1 = change_color_temperature(img, wb1)
    intermediate_2 = adjust_color(red, green, blue, intermediate_1)
    intermediate_3 = rgb_to_brr(intermediate_2)
    intermediate_4 = change_color_temperature(intermediate_3, wb2)
    intermediate_5 = ImageEnhance.Contrast(intermediate_4).enhance(contrast)
    intermediate_6 = ImageEnhance.Color(intermediate_5).enhance(saturation)
    final = ImageEnhance.Brightness(intermediate_6).enhance(brightness)
    return final

if __name__ == '__main__':
    APP_NAME = "Aerochromizer"
    DESCRIPTION = """Convert JPEGs taken from full-spectrum modified camera into aerochrome inspired colored images"""

    parser = argparse.ArgumentParser(prog=APP_NAME, description=DESCRIPTION)
    parser.add_argument("--image", help="File path of input image", required=True)
    parser.add_argument("--output", help="File path of output image", required=True)
    parser.add_argument("--wb1", help="Initial White Balance Temperature (1000 to 10000K)", default=5000)
    parser.add_argument("--wb2", help="Second White Balance Temperature (1000 to 10000K)", default=4500)
    parser.add_argument("--contrast", help="Contrast Adjustment Scale", default=1.8)
    parser.add_argument("--saturation", help="Saturation Adjustment Scale", default=1.8)
    parser.add_argument("--brightness", help="Brightness Adjustment Scale", default=0.75)
    parser.add_argument("--red", help="Red Adjustment Scale", default=1.0)
    parser.add_argument("--green", help="Green Adjustment Scale", default=0.5)
    parser.add_argument("--blue", help="Blue Adjustment Scale", default=1.0)
    args = parser.parse_args()

    aero_img = None
    kwargs = vars(args)
    input_fp = kwargs.pop("image")
    output_fp = kwargs.pop("output")

    try:
        original_img = Image.open(input_fp)
        aero_img = generate_faux_aerochrome(original_img, **kwargs)
    except IOError:
        print(f"Failed to find/open image '{input_fp}'")

    try:
        aero_img.save(output_fp)
    except IOError:
        print(f"Failed save image '{output_fp}'")

