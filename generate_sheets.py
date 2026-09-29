"""
MTG Jumpstart Themes Print Generator
==================================================
Converts side-by-side exports from BurgerTokens into print-ready,
double-sided 3x3 US Letter PDFs with long-edge duplex alignment.

Usage:
  1. pip install reportlab pillow
  2. Place your raw images in 'raw_inputs/'
  3. Run: python generate_sheets.py

Repository & Documentation:
https://github.com/jkund/mtg-jumpstart-theme-prints
"""

import glob
import os
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ==============================================================================
# 1. SETUP ENVIRONMENT & DIRECTORIES
# ==============================================================================
RAW_INPUT_DIR = "raw_inputs"
CROPPED_FRONT_DIR = "cropped_fronts"
CROPPED_BACK_DIR = "cropped_backs"

for d in [RAW_INPUT_DIR, CROPPED_FRONT_DIR, CROPPED_BACK_DIR]:
    os.makedirs(d, exist_ok=True)

# ==============================================================================
# 2. CHECK RAW INPUTS
# ==============================================================================
valid_exts = ("*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG", "*.webp")


def get_raw_files():
    found = []
    for ext in valid_exts:
        found.extend(glob.glob(os.path.join(RAW_INPUT_DIR, ext)))
    return found


raw_files = get_raw_files()

if not raw_files:
    print(f"No raw files found in '{RAW_INPUT_DIR}/'.")
    print("Please place your side-by-side card images into that folder and re-run.")
    raise SystemExit(1)

print(f"Ready to process {len(raw_files)} raw image(s).")

# ==============================================================================
# 3. BURGERTOKENS DUAL-CARD EXTRACTION & STANDARDIZATION
# ==============================================================================
TARGET_W = 750   # 2.5" at 300 DPI
TARGET_H = 1050  # 3.5" at 300 DPI


def get_card_bounding_boxes(img):
    """Locates the front card using the outer black frame on the left,

    and applies identical dimensions to the right card.
    """
    total_w, total_h = img.size
    mid_x = total_w // 2

    # Analyze left half to locate the black card frame
    left_half = img.crop((0, 0, mid_x, total_h)).convert("L")

    # Invert so black borders become bright highlights
    inv = ImageOps.invert(left_half)

    # Bounding box of the card (ignoring white outer canvas)
    bbox = inv.point(lambda p: 255 if p > 30 else 0).getbbox()

    # Fallback to standard BurgerTokens proportional template if detection slips
    if not bbox:
        card_w = int(total_w * 0.455)
        card_h = int(card_w * (3.5 / 2.5))
        top = int(total_h * 0.045)
        left = int(total_w * 0.03)
        right_left = int(total_w * 0.515)
        box_left = (left, top, left + card_w, top + card_h)
        box_right = (right_left, top, right_left + card_w, top + card_h)
        return box_left, box_right

    left, top, right, bottom = bbox
    card_w = right - left
    card_h = bottom - top

    # Ensure exact 2.5 : 3.5 aspect ratio
    expected_h = int(card_w * (3.5 / 2.5))
    if abs(card_h - expected_h) > 4:
        card_h = expected_h

    # The right card shares the exact top, height, and width
    right_card_left = total_w - right

    box_front = (left, top, left + card_w, top + card_h)
    box_back = (right_card_left, top, right_card_left + card_w, top + card_h)

    return box_front, box_back


print("\n--- Step 1: Extracting Fronts & Backs (BurgerTokens Layout) ---")
processed_count = 0

for file_path in raw_files:
    filename = os.path.basename(file_path)
    base_name, _ = os.path.splitext(filename)

    try:
        with Image.open(file_path) as img:
            img = img.convert("RGB")

            box_front, box_back = get_card_bounding_boxes(img)

            # Crop both cards using identical dimensions
            front_card = img.crop(box_front).resize(
                (TARGET_W, TARGET_H), Image.Resampling.LANCZOS
            )
            back_card = img.crop(box_back).resize(
                (TARGET_W, TARGET_H), Image.Resampling.LANCZOS
            )

            front_card.save(
                os.path.join(CROPPED_FRONT_DIR, f"{base_name}.png"),
                dpi=(300, 300),
            )
            back_card.save(
                os.path.join(CROPPED_BACK_DIR, f"{base_name}.png"),
                dpi=(300, 300),
            )

            print(f"  ✓ Processed: {base_name}")
            processed_count += 1

    except Exception as e:
        print(f"  ✗ Error processing {filename}: {e}")

if processed_count == 0:
    raise SystemExit("No images processed. Stopping before PDF build.")

# ==============================================================================
# 4. DUPLEX 3x3 GRID BUILDER (PDF CANVAS)
# ==============================================================================
print("\n--- Step 2: Assembling Printable Duplex PDF ---")
DPI_PDF = 72.0
PAGE_WIDTH, PAGE_HEIGHT = letter  # 612.0 x 792.0 points (8.5" x 11")

CARD_WIDTH_PT = 2.5 * DPI_PDF    # 180.0 points
CARD_HEIGHT_PT = 3.5 * DPI_PDF   # 252.0 points

GRID_COLS = 3
GRID_ROWS = 3

GRID_TOTAL_WIDTH = GRID_COLS * CARD_WIDTH_PT    # 7.5 inches
GRID_TOTAL_HEIGHT = GRID_ROWS * CARD_HEIGHT_PT  # 10.5 inches

# Perfect center margins: 0.5" horizontal, 0.25" vertical
MARGIN_LEFT = (PAGE_WIDTH - GRID_TOTAL_WIDTH) / 2.0
MARGIN_BOTTOM = (PAGE_HEIGHT - GRID_TOTAL_HEIGHT) / 2.0

OUTPUT_PDF = "MtG_JumpStart_Themes_Print.pdf"

# Rename deck examples to match each image filename
sheet1_packs = [
    "DECK_NAME_1", "DECK_NAME_2", "DECK_NAME_3",
    "DECK_NAME_4", "DECK_NAME_5", "DECK_NAME_6",
    "DECK_NAME_7", "DECK_NAME_8", "DECK_NAME_9"
]

sheet2_packs = [
    "DECK_NAME_10", "DECK_NAME_11", "DECK_NAME_12",
    "DECK_NAME_13", "DECK_NAME_14", "DECK_NAME_15",
    "DECK_NAME_16", "DECK_NAME_17", "DECK_NAME_18"
]

sheet3_packs = [
    "DECK_NAME_19", "DECK_NAME_20", "DECK_NAME_21",
    "DECK_NAME_22", "DECK_NAME_23", "DECK_NAME_24",
    None, None, None
]

all_sheets = [sheet1_packs, sheet2_packs, sheet3_packs]


def find_image(folder, pack_id):
    for ext in [".png", ".jpg", ".jpeg"]:
        candidate = os.path.join(folder, f"{pack_id}{ext}")
        if os.path.exists(candidate):
            return candidate
    return None


def draw_sheet(pdf_canvas, pack_list, is_back=False):
    for index, pack_id in enumerate(pack_list):
        row = index // GRID_COLS
        col = index % GRID_COLS

        # Duplex column mirroring (0 -> 2, 2 -> 0)
        if is_back:
            col = (GRID_COLS - 1) - col

        x = MARGIN_LEFT + (col * CARD_WIDTH_PT)
        y = MARGIN_BOTTOM + ((GRID_ROWS - 1 - row) * CARD_HEIGHT_PT)

        # Faint dashed cutting guide
        pdf_canvas.saveState()
        pdf_canvas.setStrokeColorRGB(0.7, 0.7, 0.7)
        pdf_canvas.setLineWidth(0.5)
        pdf_canvas.setDash(2, 2)
        pdf_canvas.rect(x, y, CARD_WIDTH_PT, CARD_HEIGHT_PT)
        pdf_canvas.restoreState()

        if pack_id is not None:
            folder = CROPPED_BACK_DIR if is_back else CROPPED_FRONT_DIR
            img_path = find_image(folder, pack_id)

            if img_path:
                pdf_canvas.drawImage(
                    img_path, x, y, width=CARD_WIDTH_PT, height=CARD_HEIGHT_PT
                )
            else:
                pdf_canvas.saveState()
                pdf_canvas.setFont("Helvetica-Bold", 8.5)
                pdf_canvas.drawCentredString(
                    x + CARD_WIDTH_PT / 2.0, y + CARD_HEIGHT_PT / 2.0 + 10, str(pack_id)
                )
                pdf_canvas.setFont("Helvetica", 7.5)
                label = "• Decklist Back •" if is_back else "• Front Art •"
                pdf_canvas.drawCentredString(
                    x + CARD_WIDTH_PT / 2.0, y + CARD_HEIGHT_PT / 2.0 - 5, label
                )
                pdf_canvas.setFillColorRGB(0.5, 0.5, 0.5)
                pdf_canvas.drawCentredString(
                    x + CARD_WIDTH_PT / 2.0, y + CARD_HEIGHT_PT / 2.0 - 18, "(Missing Image)"
                )
                pdf_canvas.restoreState()
        else:
            pdf_canvas.saveState()
            pdf_canvas.setFont("Helvetica-Oblique", 8)
            pdf_canvas.setFillColorRGB(0.65, 0.65, 0.65)
            pdf_canvas.drawCentredString(
                x + CARD_WIDTH_PT / 2.0, y + CARD_HEIGHT_PT / 2.0, "[ Empty Slot ]"
            )
            pdf_canvas.restoreState()

    pdf_canvas.showPage()


# ==============================================================================
# 5. ASSEMBLE PDF
# ==============================================================================
if __name__ == "__main__":
    pdf = canvas.Canvas(OUTPUT_PDF, pagesize=letter)

    for sheet in all_sheets:
        draw_sheet(pdf, sheet, is_back=False)
        draw_sheet(pdf, sheet, is_back=True)

    pdf.save()
    print(f"\nGenerated: '{OUTPUT_PDF}' (6 pages total).")
    print("Reminder: Print at 100% / Actual Size with 'Flip on Long Edge'.")
