#!/usr/bin/env python

import drawSvg as draw

fill_color = "none"
stroke_color = "black"


def group_of_octaves(
    x: float,
    y: float,
    generator_x_increment: float,
    octave_height: float,
    octaves: int = 1,
    circles: int = 1,
    divisions: int = 12,
    generator: int = 7,
    skew: float = 1,
) -> draw.Group:

    octave_coordinates = [
        # add in circles of fifts and octaves
        (
            circle * divisions_of_octave * generator_x_increment + key[0],
            octave * octave_height + key[1],
        )
        for octave in range(octaves)
        for circle in range(circles)
        for key in zip(
            [
                (((generator * (i + (divisions / 2))) % (divisions)))
                * generator_x_increment
                for i in range(divisions)
            ],
            [j * (octave_height / divisions) for j in range(divisions)],
        )
    ]
    notes = draw.Group()

    for coordinates in octave_coordinates:
        print(coordinates)
        notes.append(
            draw.Circle(
                x + coordinates[0],
                y + coordinates[1],
                key_radius,
                stroke=stroke_color,
                fill=fill_color,
                stroke_width=stroke_width,
            )
        )

    return notes


pixels_per_mm = 96 / 25.4
pixels_per_m = pixels_per_mm * 1000
pixels_per_point = 96 / 72

divisions_of_octave = 12
generator = 7

stroke_width = 1 * pixels_per_point
key_radius = (7.3 * pixels_per_mm) - stroke_width / 2
generator_x_unit = 8.5 * pixels_per_mm
octave_height = 38.553 * pixels_per_mm

string_length = 2 * divisions_of_octave * generator_x_unit

d = draw.Drawing(
    2 ** (1 / 4) * pixels_per_m,
    1 / (2 ** (1 / 4)) * pixels_per_m,
    origin="center",
    displayInline=False,
)

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

    d.append(string)
    y -= deflection * 4


d.append(group_of_octaves(0, 0, generator_x_unit, octave_height, 3, 3))

# d.append(group_of_octaves(0, 0, generator_x_unit, octave_height, 3, 3, 12, 7))
# d.append(group_of_octaves(0, -768, generator_x_unit, octave_height, 3, 3, 12, 7, 1.1))
# d.append(group_of_octaves(0, -1440, generator_x_unit, octave_height, 3, 3, 12, 7, -1.1))

d.saveSvg("out.svg")
