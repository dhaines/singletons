#!/usr/bin/env python

import drawSvg as draw
import math

fill_color = "none"
stroke_color = "black"


def group_of_octaves(
    x: float,
    y: float,
    x_unit: float,
    octave_height: float,
    octaves: int = 1,
    circles: int = 1,
    pitches: int = 12,
    generator: int = 7,
    skew: float = 0,
) -> draw.Group:

    octave_coordinates = [
        (
            circle * pitches + pitch * generator % pitches,
            octave + pitch / pitches
        )
        for octave in range(octaves)
        for circle in range(circles)
        for pitch in range(pitches)
    ]
    keys = draw.Group()

    # A guess, but it looks right.
    skew *= pitches ** 2

    for coordinates in octave_coordinates:
        # print(coordinates)
        print((coordinates[0], coordinates[1] + coordinates[0] * skew))
        keys.append(
            draw.Circle(
                x + coordinates[0] * x_unit,
                y + coordinates[1] * octave_height + coordinates[0] * skew,
                key_radius,
                stroke=stroke_color,
                fill=fill_color,
                stroke_width=stroke_width,
            )
        )

    return keys


pixels_per_mm = 96 / 25.4
pixels_per_m = pixels_per_mm * 1000
pixels_per_point = 96 / 72

pitch_classes_per_octave = 12
generator = 7

stroke_width = 1 * pixels_per_point
key_radius = (7.3 * pixels_per_mm) - stroke_width / 2
generator_x_unit = 8.5 * pixels_per_mm
octave_height = 38.553 * pixels_per_mm

d = draw.Drawing(
    2 ** (1 / 4) * pixels_per_m,
    1 / (2 ** (1 / 4)) * pixels_per_m,
    origin="center",
    displayInline=False,
)

# 12-TET
d.append(group_of_octaves(0, 0, generator_x_unit, octave_height, 13, 13, pitch_classes_per_octave, generator, math.log2(1)))

# Pythagorean
d.append(group_of_octaves(0, 0, generator_x_unit, octave_height, 13, 13, pitch_classes_per_octave, generator, math.log2(3**12/2**19) / 12))

# 1/4 comma meantone
d.append(group_of_octaves(0, 0, generator_x_unit, octave_height, 13, 13, pitch_classes_per_octave, generator, -(math.log2(3**4/((2**4)*5)) / 4)))


string_length = 2 * pitch_classes_per_octave * generator_x_unit

y = -64
for i in [1, 2, 3, 5, 7, 11]:
    x = 0
    length = string_length / i
    midpoint = length / 2
    deflection = (string_length / i) ** 0.5 / 2

    string = draw.Group()

    for j in range(i):
        p = draw.Path(stroke_width=stroke_width, stroke=stroke_color, fill=fill_color)
        for k in list(range(4)):
            p.M(x, y)
            p.q(midpoint, k * deflection, length, 0)
            p.M(x + length, y)
            p.q(-midpoint, -k * deflection, -length, 0)
        string.append(p)
        x += length

    # d.append(string)
    y -= deflection * 4

d.saveSvg("out.svg")
