#!/usr/bin/env python

import drawSvg as draw

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

fill_color = "none"
stroke_color = "black"

d = draw.Drawing(2 ** (1 / 4) * pixels_per_m, 1 / (2 ** (1 / 4)) * pixels_per_m, origin="center", displayInline=False)

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


notes = draw.Group()

octave_coordinates = list(
    zip(
        [
            (((generator * (i + (divisions_of_octave / 2))) % (divisions_of_octave)))
            * generator_x_unit
            for i in range(divisions_of_octave)
        ],
        [
            j * (octave_height / divisions_of_octave)
            for j in range(divisions_of_octave + 1)
        ],
    )
)

y = 0
for octave in range(12):
    x = 0
    for circle in range(12):
        for coordinates in octave_coordinates:
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
        x += divisions_of_octave * generator_x_unit
    y += octave_height

d.append(notes)

d.saveSvg("out.svg")
