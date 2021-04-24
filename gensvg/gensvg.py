#!/usr/bin/env python

import drawSvg as draw
import math
import dcompose

fill_color = "none"
stroke_color = "black"


def append_layout(d, spec):
    button_group = draw.Group()

    layout = dcompose.DCompose(8.5)
    layout.octave_start = 0.2
    layout.board_width = 160.0
    layout.board_height = 160.0
    layout.offset_x = 20.0
    layout.offset_y = 20.0
    layout.min_pitch = spec[2]
    layout.max_pitch = spec[3]
    # layout.min_note = -17
    # layout.max_note = 45
    layout.min_note = spec[4]
    layout.max_note = spec[5]

    buttons = layout.get_buttons()
    print(buttons)

    for button in buttons:
        button_group.append(
            draw.Circle(
                spec[0] + button.pos[0],
                spec[1] + button.pos[1],
                7.3,
                stroke=stroke_color,
                fill=fill_color,
                stroke_width=stroke_width,
            )
        )
        if spec[6]:
            button_group.append(
                draw.Text(
                    button.name,
                    4,
                    spec[0] + button.pos[0],
                    spec[1] + button.pos[1],
                    center=True,
                )
            )

    d.append(button_group)


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


string_length = 2 * pitch_classes_per_octave * generator_x_unit

y = -128
for i in [1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]:
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


C4 = -200
D4 = 0
octave = 1200
M6 = 900

layouts = [
    # Board
    (0, 0, D4 - octave - M6 , D4 + octave + M6, -8, 8, True),
    # D-D 1x1
    (200, 0, D4, D4 + octave, -8, 8, True),
    # C-C 1x1
    (400, 0, C4, C4 + octave, -8, 8, True),
    # D-D 2x1
    (200, 100, D4, D4 + octave * 2, -8, 8, True),
    # C-C 2x1
    (400, 100, C4, C4 + octave * 2, -8, 8, True),
    # D-D 2x2
    (0, 200, D4, D4 + octave * 2, -16, 16, True),
    # C-C 2x2
    (400, 200, C4, C4 + octave * 2, -16, 16, True),
    # D-D 4x2
    (0, 400, D4, D4 + octave * 4, -16, 16, True),
    # C-C 4x2
    (400, 400, C4, C4 + octave * 4, -16, 16, True),
    # D-D 4x4
    (200, 600, D4, D4 + octave * 4, -31, 31, True),
    # C-C 4x4
    (200, 800, C4, C4 + octave * 4, -31, 31, True),
    # D-D 8x4
    (200, 1200, D4, D4 + octave * 8, -31, 31, True),
    # C-C 8x4
    (200, 1600, C4, C4 + octave * 8, -31, 31, True),
    # D-D 10x4
    (200, 2000, D4, D4 + octave * 10, -31, 31, True),
    # Grand
    # (-1000, 1100 + 1200 * 7 + 10, -8, 8),
    # Grander
    # (-1000, 1100 + 1200 * 7 + 10, 0, 28),
    # Approx. 1'-64' Organ
    # (-1000, -1100 + 1200 * 10 + 100, 0, 28),
    # The Experimentalist
    # (-900 + 1200, 3300 + 1200, -8, 8),
]

layouts = [
    (x * 32, y * 300, root_note, root_note + octave * y, -x, x, print_names)
    for x in [8, 15, 31]
    for y in [1, 2, 4, 8, 10, 12]
    for root_note in [D4, C4]
    for print_names in [True]
]

# Striso Board
layouts.append((0, 0, D4 - octave - M6 , D4 + octave + M6, -8, 8, True))
# Grand Piano
layouts.append((48 * 32, 0, C4, C4 + octave * 7 + 4, -8, 8, True))
# Bosendorfer Piano
layouts.append((64 * 32, 0, C4, C4 + octave * 12, -8, 8, True))

for layout in layouts:
    print(layout)
    append_layout(d, layout)

d.saveSvg("out.svg")
