# Contributing to Open Thaana

Thank you for wanting to help. This is a free font and contributions of all
kinds are welcome.

## Reporting a problem

Open an issue and include:

- The character or word that renders wrongly, as text (not only a screenshot)
  so it can be copied and tested.
- A screenshot showing the problem.
- The application, operating system and font version.

Things worth reporting:

- A fili sitting wrongly over its consonant.
- Letters that collide or sit too far apart.
- A glyph that looks wrong at small sizes.
- Any character in U+0780-U+07B1 that renders as a blank or a box.

## Requesting a missing glyph

This font covers the Thaana block only. If you need Latin letters, digits or
punctuation, say what you need and what you are using the font for.

## Submitting a change

1. Fork the repository and branch from `main`.
2. Edit the **source**, not the compiled fonts: open `sources/*.ufo` in
   Glyphs, RoboFont, FontForge or any UFO-capable editor.
3. Rebuild with `python build.py` so `fonts/` matches the source.
4. Add a line to `FONTLOG.txt` describing what you changed.
5. Add yourself to `CONTRIBUTORS.txt`.
6. Open a pull request explaining what changed and why.

## Design notes

A few things to keep in mind when editing Thaana outlines:

- **The fili must keep a zero advance width.** They are combining marks; if
  one gains a width it will push the next letter along instead of sitting
  over its consonant.
- **Keep the GPOS anchors sensible.** Each consonant carries an anchor at
  the centre of its ink, and each fili one at the centre of its own.
- **Mind the vertical extremes.** Fili reach high above the letters and
  ibifili and eebeefili hang well below the baseline. Check that ascender,
  descender and the OS/2 win values still cover everything after an edit.
- **Counters must wind opposite to their outer contour**, or they fill in.

## Licensing of contributions

By contributing you agree that your work is released under the same licence
as the font (see the LICENCE section of the README). Add yourself to
`CONTRIBUTORS.txt` rather than `AUTHORS.txt` unless you are contributing a
substantial body of original design work.
