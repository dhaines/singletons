#!/usr/bin/env python

import drawSvg as draw
import math
import dcompose

fill_color = "none"
stroke_color = "black"


def append_layout(d, spec):
    button_group = draw.Group()
    skew = 4.5356 * spec[6]

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
        if spec[7]:
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


string_length = pitch_classes_per_octave * generator_x_unit / 2

y = -128
for i in range(1,16):
    x = 0
    length = string_length / i
    midpoint = length / 2
    deflection = (12 * string_length) / (64 * ((1 + math.sqrt(3)) / 2) * i ** (1/2))

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

    d.append(string)
    y -= deflection * 2


C4 = -200
D4 = 0
octave = 1200
M6 = 900
m3 = 300

layouts = [
    (
        16 * 2 * width,
        256 * (span - 1),
        board_type[0] - octave * span - board_type[1],
        board_type[0] + octave * span + board_type[1],
        -width,
        width,
        0,
        False
    )


    # Single/Striso Board Physical, Double, Triple/Striso Board Virtual, Imperial Concert Grand, Midmer-Losh Organ
    for span in [1, 2, 3, 4, 5]

    # Single, Double, or Quadruple degrees of 
    for width in [8, 15, 31]

    # Striso Board, DCompose, LegaC DCompose
    for board_type in [(D4, M6), (D4, 0), (C4, 0)]

]

# layouts = []

# All the notes in all the tunings
layouts.extend([
    (
        1536 + (640 if show_notes == False else 0),
        0 + 512 * skew[0],
        D4 - octave * 5,
        D4 + octave * 5,
        -31,
        31,
        skew[1],
        show_notes
    )
    for skew in [
        # 5TET (Major third = fourth; minor sixth = fifth)
        (3, math.log2(2 ** (1/5))/12),

        # Pythagorean (raise enharmonic equivalent diminished second by a Pythagorean Comma)
        (2, math.log2(3**12/2**19)/12),

        # 1/12 Comma Meantone (raise enharmonic equivalent diminished second by a schisma)
        (1, math.log2(32805/32768)),

        # Equal temperment
        (0, 0),

        # 1/6 Comma Meantone (lower enharmonic equivalent diminished second by a diaschisma)
        (-1, -math.log2(2048/2025)/12),

        # 31TET
        (-2, -math.log2(2 ** (1/31))/12),

        # 1/4 Comma Meantone (lower enharmonic equivalent diminished second by a diesis)
        (-3, -math.log2(128/125)/12),

        # 1/3 Comma Meantone (lower enharmonic equivalent diminished second by a greater diesis)
        (-4, -math.log2(648/625)/12),

        # 19TET
        (-5, -math.log2(2 ** (1/19))/12),
        
        # 7TET (accidentals = naturals)
        (-6, -math.log2(2 ** (1/7))/12),


    ]
    for show_notes in [True, False]
])

# Grand Piano
layouts.append((0, 0, C4 - octave * 3 - m3, C4 + octave * 4, -8, 8, 0, True))
layouts.append((0, 512, C4 - octave * 3 - m3, C4 + octave * 4, -8, 8, 0, False))

# Single Octave
layouts.extend((-512 + root * 4, 96 * math.log2(width + 1) - 96 * 2 , root, root + octave, -width, width, 0, False) for root in [C4,D4] for width in [8, 15, 31])
layouts.extend((-2048, 96 * math.log2(width + 1) - 96 * 2 , root - M6, root + octave + M6, -width, width, 0, False) for root in [D4] for width in [8, 15, 31])

for layout in layouts:
    print(layout)
    append_layout(d, layout)

d.saveSvg("out.svg")
