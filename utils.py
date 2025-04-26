from PIL import Image
from scipy import interpolate

# Table from https://stackoverflow.com/questions/11884544/setting-color-temperature-for-a-given-image-like-in-photoshop
_KELVIN_TABLE = {
    1000: (255,56,0),
    1500: (255,109,0),
    2000: (255,137,18),
    2500: (255,161,72),
    3000: (255,180,107),
    3500: (255,196,137),
    4000: (255,209,163),
    4500: (255,219,186),
    5000: (255,228,206),
    5500: (255,236,224),
    6000: (255,243,239),
    6500: (255,249,253),
    7000: (245,243,255),
    7500: (235,238,255),
    8000: (227,233,255),
    8500: (220,229,255),
    9000: (214,225,255),
    9500: (208,222,255),
    10000: (204,219,255)
}

_R_CH = interpolate.CubicSpline(list(_KELVIN_TABLE.keys()), [color[0] for color in _KELVIN_TABLE.values()])
_G_CH = interpolate.CubicSpline(list(_KELVIN_TABLE.keys()), [color[1] for color in _KELVIN_TABLE.values()])
_B_CH = interpolate.CubicSpline(list(_KELVIN_TABLE.keys()), [color[2] for color in _KELVIN_TABLE.values()])

def change_color_temperature(img: Image, temperature: int) -> Image:
    if temperature < 1000 or temperature > 10000:
        raise ValueError('Temperature must be between 1000K and 10000K')

    r = _R_CH(temperature)
    g = _G_CH(temperature)
    b = _B_CH(temperature)

    matrix = (r / 255.0, 0.0, 0.0, 0.0,
              0.0, g / 255.0, 0.0, 0.0,
              0.0, 0.0, b / 255.0, 0.0)
    return img.convert('RGB', matrix)

def rgb_to_brr(img: Image) -> Image:
    r, g, b = img.split()
    return Image.merge('RGB', (b, r, r))


def adjust_color(r:float, g:float, b:float, img: Image) -> Image:
    matrix = ( r, 0.0, 0.0, 0.0,
               0.0, g, 0.0, 0.0,
               0.0, 0.0, b, 0.0 )
    return img.convert('RGB', matrix)
