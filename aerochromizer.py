import argparse
import os

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
    DESCRIPTION = """Convert JPEGs taken from full-spectrum modified camera into aerochrome inspired colored images. If input dir is supplied, output will be saved in a folder named 'aerochromed' inside it."""

    parser = argparse.ArgumentParser(prog=APP_NAME, description=DESCRIPTION)
    parser.add_argument("--input", help="File path of input image / dir [REQUIRED]", required=True)
    parser.add_argument("--output", help="File path of output image / dir", required=True)
    parser.add_argument("--wb1", help="Initial White Balance Temperature (1000 to 10000K) [default 5000]", default=5000)
    parser.add_argument("--wb2", help="Second White Balance Temperature (1000 to 10000K) [default 4500]", default=4500)
    parser.add_argument("--contrast", help="Contrast Adjustment Scale [default 1.8]", default=1.8)
    parser.add_argument("--saturation", help="Saturation Adjustment Scale [default 1.8]", default=1.8)
    parser.add_argument("--brightness", help="Brightness Adjustment Scale [default 0.75]", default=0.75)
    parser.add_argument("--red", help="Red Adjustment Scale [default 1.0]", default=1.0)
    parser.add_argument("--green", help="Green Adjustment Scale [default 0.5]", default=0.5)
    parser.add_argument("--blue", help="Blue Adjustment Scale [default 1.0]", default=1.0)
    args = parser.parse_args()

    aero_img = None
    kwargs = vars(args)
    input_path = kwargs.pop("input")
    output_path = kwargs.pop("output")

    is_input_path_dir = os.path.isdir(input_path)
    is_output_path_dir = os.path.isdir(output_path)

    # Single File
    if is_input_path_dir:
        if not is_output_path_dir:
            raise RuntimeError(f"Output path must be a directory if input path is a directory!")

        files = os.listdir(input_path)
        print("Found {} files in {}".format(len(files), input_path))
        for i, file in enumerate(files):
            if os.path.isfile(os.path.join(input_path, file)):
                try:
                    original_file_path = os.path.join(input_path, file)
                    output_file_path = os.path.join(output_path, f"aero_{file}")

                    original_img = Image.open(original_file_path)
                    aero_img = generate_faux_aerochrome(original_img, **kwargs)

                    try:
                        aero_img.save(output_file_path)
                        print(f"[{(i+1):03} / {len(files)}] Aerochromized {original_file_path} --> {output_file_path}")
                    except IOError:
                        print(f"Failed saving image '{output_file_path}'")

                except IOError:
                    print(f"Failed to find/open image '{input_path}'")

    else:
        if is_output_path_dir:
            raise RuntimeError(f"Output path must be a file if input path is a single file!")

        try:
            original_img = Image.open(input_path)
            aero_img = generate_faux_aerochrome(original_img, **kwargs)
        except IOError:
            print(f"Failed to find/open image '{input_path}'")

        try:
            aero_img.save(output_path)
        except IOError:
            print(f"Failed saving image '{output_path}'")

