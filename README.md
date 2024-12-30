<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px;">
  <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
    <img 
      src="./img/README/colorfy-logo_256x256.png" 
      alt="Colorfy Logo" 
      width="100" 
      style="position: relative; top: -10px; left: -10px;">
    <div>
      <h1 style="margin: 0;">Colorfy</h1>
      <div>
        <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
        <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
        <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
        <img src="https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0" alt="macOS">
        <img src="https://img.shields.io/badge/GitBook-%23000000.svg?style=for-the-badge&logo=gitbook&logoColor=white" alt="GitBook">
      </div>
    </div>
  </div>

  <div style="text-align: center;">
    <p><strong>Colorfy</strong> is a Python library for text-formatting in the console. You can use it on Unix-based systems, such as Linux and macOS, and on Windows.</p>
  </div>
</div>

---

## Installation

- **`pip install colorfy`**
- Download the file called **colorfy** from **include** folder.

---

## :warning: Warning :warning:
:warning: Warning: Some features could not be used in Windows, for example Windows does not support Stylist's features such as **BOLD** style.
:warning: Info: To enable Stylist's features in **Windows Console** you have to **initialize colorfy**:
```python
from colorfy import Colorfy

Colorfy.init()
```

I have been using **Alpine Linux**, for showcase, so I **did not use** colorfy initialization


---

## Features

-   **Color support**: Use HEX color codes or RGBA tuples to apply colors to text.
-   **Pre-defined color palettes**: Includes basic colors and themed palettes (e.g., Catppuccin, Dracula and Solarized themes).
-   **Text styling**: Bold, italic, underline and strikethrough.


---


### Showcase

#### Custom colors

```python
from colorfy import Colorfy

#applying HEX color
some_color = Colorfy("#FF5733")
print(some_color.apply(“Some color | example 1 ” + some_color.get_hex())

#applying color using RGBA
another_color = Colorfy((255, 200, 0, 255))
print(another_color.apply("Some color | example 2 " + some_color.get_hex())
```
![img_example1](./img/CODESNIP/img_example1.jpg)

#### Stylist

```python
from colorfy import Stylist, Palette

print(Stylist.BOLD + "Hello world" + Stylist.RESET)
print(Stylist.ITALIC + "Hello World" + Stylist.RESET)
print(Stylist.STRIKETHROUGHT + "Hello world" + Stylist.RESET)
print(Stylist.UNDLINE + "Hello World" + Stylist.RESET)
# I called it .SWAP cuz it swaps "apply" func's target layer to bg
print(Stylist.SWAP + Colorfy(Palette.RED).apply("Hello World") + Stylist.RESET)
```
![img_example2](./img/CODESNIP/img_example2.jpg)

#### Palette

```python
from colorfy import Colorfy, Palette

print(Colorfy(Palette.Catppuccin.Latte.TEAL).apply("██ # TEAL"))
print(Colorfy(Palette.Catppuccin.Latte.SKY).apply("██ # SKY"))
print(Colorfy(Palette.Catppuccin.Latte.SAPPHIRE).apply("██ # SAPPHIRE"))
```
![img_example3](./img/CODESNIP/img_example3.jpg)

---

## TODO
- [ ] Refactor some parts
- [ ] Add EMOJI class to print emojis in Console
- [ ] Add gradient functions same as in venaxyt/fade library, but also make it flexible, so you can create your own fade colors
- [ ] Add GitBook documentation

--- 
### P.S.
If you have any questions or ideas for this library, feel free to ask. My discord: **antisssocial_**




