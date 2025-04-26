# Aerochromizer
Converts photos taken through a "Full Spectrum" modified camera into aerochrome styled photos. 

## To Install
This has been tested with Python 3.13. You'll want to install the requirements in requirements.txt before attempting to
run the script. 

## To Use
Simply run the script:
````
python aerochromizer.py --image [path to input jpeg] --output [path to output jpeg]
````

If you find the default values for some of the adjustments not to your liking, feel free to experiment. These can be 
changed at runtime easily. For a full list of variables, see below:

````
Aerochromizer [-h] --image IMAGE --output OUTPUT [--wb1 WB1] [--wb2 WB2] [--contrast CONTRAST] [--saturation SATURATION] [--brightness BRIGHTNESS] [--red RED] [--green GREEN] [--blue BLUE]
````

## Operation
1. Assume photo is taken white balanced to something approximately white (such as concrete).
2. White balance is changed to 'wb1' (in Kelvin) via table found [here](https://stackoverflow.com/questions/11884544/setting-color-temperature-for-a-given-image-like-in-photoshop)
3. Colors are adjusted according to scales in inputs 'red', 'green', 'blue'
4. Color channel swapped -- RGB to BRR
5. White balance is yet again changed, this time to 'wb2' (in Kelvin)
6. Contrast, Color, Brightness scales are modified per inputs 'contrast', 'saturation', 'brigtness'
7. File is saved to disk to path specified in 'output'