<!-- This file is generated from resource.toml. Edit resource.toml and run ./jr readme. -->

# Shared material

Tools used by several challenges. Challenges include them in their output, in a folder named after the tool (e.g. `decoder/`). This file is generated from each tool's `resource.toml`.

## Image editor

- `beeldbewerker/` (generated)

Web page to view and edit an image: brightness, contrast, colour channels, invert and more. Handy for information hidden in images. Works offline in the browser, in Dutch and English. A default image can be built in, so it is loaded right away.

Usage: Build with `./jr shared build beeldbewerker --set afbeelding=path/to/image.png` (options `afbeelding` and `taal`). The image is then part of `beeldbewerker/index.html` itself, so the page also works from disk without internet. Other images are opened by a participant with 'Open image' or by dropping them on the page; with a web server `index.html#afbeelding=qr.png` also works. The 'Default image' button reloads the built-in image.

## Decoder

- `decoder/` (static)

Web page to encode and decode messages: Base64, hexadecimal, binary, morse, ROT-N and XOR, with several steps in a row. Works offline in the browser, in Dutch and English.

Usage: Open `decoder/index.html` in a browser. The setup (input and steps) is kept in the URL after `#`, so a facilitator can share a ready-made link. Example: `index.html#t=en&i=PXIXA&s=rot:3`.

## Cheat sheet

- `spiekbrief/` (generated)

Printable cheat sheet (PDF) on binary, hexadecimal, Base64, ROT-N, XOR and morse, with examples that the generator computes itself.

Usage: Build with `./jr shared build spiekbrief` (option `--set taal=en`). Challenges that use encoding include the cheat sheet in their output.
