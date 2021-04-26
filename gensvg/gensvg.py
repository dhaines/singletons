#!/usr/bin/env python

import drawSvg as draw
import math
import dcompose

fill_color = "none"
stroke_color = "black"


def append_layout(d, spec):
    button_group = draw.Group()
    skew = spec[6]

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

    min_x = min([button.pos[0] for button in buttons])
    min_y = min([button.pos[1] for button in buttons])
    max_x = max([button.pos[0] for button in buttons])
    max_y = max([button.pos[1] for button in buttons])

    for button in buttons:
        button.pos[0] -= (min_x + max_x) / 2
        button.pos[1] -= min_y

    for button in buttons:
        button_group.append(
            draw.Circle(
                spec[0] + button.pos[0],
                spec[1] + button.pos[1] + skew * button.pos[0],
                7.3,
                stroke=stroke_color,
                fill=fill_color,
                stroke_width=stroke_width,
            )
        )
        button_group.append(
            draw.Text(
                button.name,
                4,
                spec[0] + button.pos[0],
                spec[1] + button.pos[1] + skew * button.pos[0],
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
for i in [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]:
    x = 0
    length = string_length / i
    midpoint = length / 2
    deflection = (12 * (string_length / i)) ** 0.5
    deflection = (12 * string_length) ** 0.5 / i

    string = draw.Group()

    for j in range(i):
        p = draw.Path(stroke_width=stroke_width, stroke=stroke_color, fill=fill_color)
        for k in range(12):
            p.M(x, y)
            p.q(midpoint, deflection * math.sin(k * math.pi / 2 / 12), length, 0)
            p.M(x + length, y)
            p.q(-midpoint, -deflection * math.sin(k * math.pi / 2 / 12), -length, 0)
        string.append(p)
        x += length

    # d.append(string)
    y -= deflection * 2


C4 = -200
D4 = 0
octave = 1200
M6 = 900
m3 = 300

layouts = [
    (
        16 * 2 * width,
        256 * span,
        board_type[0] - octave * span - board_type[1],
        board_type[0] + octave * span + board_type[1],
        -width,
        width,
        math.log2(skew),
    )
    for span in [1, 2, 4, 5]
    for width in [8, 15, 31]
    for board_type in [(D4, M6), (D4, 0), (C4, 0)]
    for skew in [1]
]

layouts = []

layouts.extend([
    (
        16 * 2 * width,
        128,
        board_type[0] - octave * span - board_type[1],
        board_type[0] + octave * span + board_type[1],
        -width,
        width,
        math.log2(skew),
    )
    for span in [0,1]
    for width in [8, 15, 31]
    for board_type in [(D4, M6), (D4, 0), (C4, 0)]
    for skew in [1]
])

# Striso Board
# layouts.append((0, 0, D4 - octave - M6, D4 + octave + M6, -8, 8, math.log2(1)))
# Grand Striso
# layouts.append((-8 * 32, 0, D4 - octave * 4 - M6, D4 + octave * 4 + M6, -8, 8, math.log2(1)))
# Grander Striso
# layouts.append((-16 * 32, 0, D4 - octave * 4 - M6, D4 + octave * 4 + M6, -15, 15, math.log2(1)))
# layouts.append((-16 * 32, 0, D4 - octave * 4 - M6, D4 + octave * 4 + M6, -15, 15, math.log2(2/1)/12))
# "Research" Striso
# layouts.append((-32 * 32, 0, D4 - octave * 5 - M6, D4 + octave * 5 + M6, -31, 31, math.log2(1)))
# 97-Key Piano
# layouts.append((56 * 32, 0, C4 - octave *  4, C4 + octave * 4, -8, 8, math.log2(1)))
# 1'-64' Organ
# layouts.append((64 * 32, 0, C4 - octave *  5, C4 + octave * 5, -8, 8, math.log2(1)))

# Grand Piano
layouts.append((48 * 32, 0, C4 - octave * 3 - m3, C4 + octave * 4, -8, 8, math.log2(1)))

for layout in layouts:
    print(layout)
    append_layout(d, layout)

d.saveSvg("out.svg")
