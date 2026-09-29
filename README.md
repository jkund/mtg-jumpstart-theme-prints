# mtg-jumpstart-theme-prints

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jkund/mtg-jumpstart-theme-prints/blob/main/MtG_JumpStart_Themes_Print_Generator.ipynb)

A Python tool and Google Colab notebook to convert side-by-side exports from [BurgerTokens](https://burgertokens.com/pages/jumpstart-theme-card-builder) into print-ready, double-sided PDFs.

BurgerTokens beautifully exports pack art and decklists side-by-side into a single file. This tool automatically crops and separates each image, standardizes the card sizing (2.5" × 3.5"), and organizes mirrored pairs for double-sided printing.

---

## Features

* **Automatic crop & split:** Detects the outer border of the front card, extracts both faces, and removes outer canvas padding.
* **Column mirroring:** Reverse column order on the back pages (`[1, 2, 3]` → `[3, 2, 1]`) so decklists align with the correct art.
* **MTG dimensions:** Scales images to 2.5" × 3.5" at 300 DPI, centered on an 8.5" × 11" with 0.5" side and 0.25" top/bottom margins.
* **Cutting guides:** Places subtle 0.5 pt dashed cut lines around each slot for straight cuts.
* **Workflow options:** Run directly in your browser using Google Colab or locally via command-line Python.

---

## Usage

### Method 1: Google Colab (No Installation)

1. Click the **Open In Colab** badge at the top of this page.
2. Run the notebook cell (`Shift + Enter`).
3. When prompted, upload your BurgerTokens generated images (PNG or JPG).
4. Change the example insert naming (e.g., DECK_NAME_1) to match image filenames
5. The notebook will process the files, build the PDF, and trigger an automatic download.

### Method 2: Local Python

1. Clone repository:
 ```bash
   git clone https://github.com/jkund/mtg-jumpstart-theme-prints.git
   cd mtg-jumpstart-theme-prints
   ```
2. Install dependencies:
   ```bash
   pip install pillow reportlab
   ```

3. Place BurgerTokens generated image files into the _raw_inputs/_ folder.

4. Change the example insert naming (e.g., DECK_NAME_1) to match image filenames

5. Run the script:
   ```bash
    python generate_sheets.py
   ```

Compiled PDF will be saved to your working directory.

---

## Print Settings
To ensure the fronts and backs line up when printing two-sided:
* Paper size: US Letter (8.5" × 11")
* Scale: 100% / Actual Size (do not use "Fit to Printable Area" or "Shrink to Fit")
* Two-sided mode: Flip on Long Edge (Portrait)
* Paper weight: Heavy cardstock (65 lb–110 lb) or regular paper inside standard card sleeves

## Customizing Pack Rosters
The script matches image filenames to positions on the 3×3 grid. By default, it is configured for 24 packs:

* Sheet 1: DECK_NAME_1 through DECK_NAME_9

* Sheet 2: DECK_NAME_10 through DECK_NAME_18

* Sheet 3: DECK_NAME_19 through DECK_NAME_24 (remaining slots set to blank)

To use your own set or cube names, update the roster lists in generate_sheets.py (or Section 4 of the notebook):

* Python
sheet1_packs = [
    "DECK_NAME_1", "DECK_NAME_2", "DECK_NAME_3",
    "DECK_NAME_4", "DECK_NAME_5", "DECK_NAME_6",
    "DECK_NAME_7", "DECK_NAME_8", "DECK_NAME_9"
]

Filenames in your input folder must match the list entries (e.g., DECK_NAME_1.png). Use None for any empty slots.

## Requirements
Python 3.8+

Pillow

ReportLab

## License
This project is licensed under the MIT License. See [LICENSE](https://github.com/jkund/mtg-jumpstart-theme-prints/blob/dadb413c5f1ad7958ce226acf447c54c133054fd/LICENSE)  for details.

Card imagery and theme layouts generated via BurgerTokens. 

Magic: The Gathering is a trademark of Wizards of the Coast LLC. 

This project is unofficial fan software.
