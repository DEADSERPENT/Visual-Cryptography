"""
Visual Cryptography - unified entry point.

Provides a single, menu-driven interface over the three implementations that
live in `Visual-Cryptography-main/`:

    * Grayscale images  -> XOR-based (n, n) secret sharing
    * Colour images     -> Modular-arithmetic (n, n) secret sharing
    * AES-VC            -> AES-256 + visual-cryptography key sharing

Run:  python main.py
"""

import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "Visual-Cryptography-main")
AES_DIR = os.path.join(SRC, "AES-VC")
OUTPUT_DIR = os.path.join(ROOT, "output")


# --------------------------------------------------------------------------- #
# Evaluation metrics (PSNR + normalised cross-correlation)
# --------------------------------------------------------------------------- #
def psnr(original, contrast):
    mse = np.mean((original.astype(np.float64) - contrast.astype(np.float64)) ** 2)
    if mse == 0:
        return 100.0
    return 20 * math.log10(255.0 / math.sqrt(mse))


def normxcorr2D(image, template):
    from scipy import signal

    t = np.asarray(template, dtype=np.float64)
    t = t - np.mean(t)
    norm = math.sqrt(np.sum(np.square(t)))
    if norm == 0:
        return 0.0
    t = t / norm

    sum_filter = np.ones(np.shape(t))
    a = np.asarray(image, dtype=np.float64)
    aa = np.square(a)

    a_sum = signal.correlate(a, sum_filter, "same")
    aa_sum = signal.correlate(aa, sum_filter, "same")

    numer = signal.correlate(a, t, "same")
    denom = np.sqrt(aa_sum - np.square(a_sum) / np.size(t))

    tol = np.sqrt(np.finfo(denom.dtype).eps)
    nxcorr = np.where(denom < tol, 0, numer / denom)
    nxcorr = np.where(np.abs(nxcorr - 1.0) > np.sqrt(np.finfo(nxcorr.dtype).eps), nxcorr, 0)
    return float(np.mean(nxcorr))


def report_metrics(original, reconstructed):
    print("\nEvaluation metrics:")
    print(f"  PSNR       : {psnr(original, reconstructed):.4f} dB")
    try:
        print(f"  Mean NCORR : {normxcorr2D(original, reconstructed):.6f}")
    except Exception as exc:  # scipy edge cases on flat images
        print(f"  Mean NCORR : (skipped: {exc})")


# --------------------------------------------------------------------------- #
# Small input helpers
# --------------------------------------------------------------------------- #
def ask_path(prompt):
    return input(prompt).strip().strip('"').strip("'")


def ask_share_count():
    raw = input("Number of shares to create (2-8): ").strip()
    if not raw.isdigit() or not (2 <= int(raw) <= 8):
        raise ValueError("Number of shares must be an integer between 2 and 8.")
    return int(raw)


def ensure_output(subdir):
    path = os.path.join(OUTPUT_DIR, subdir)
    os.makedirs(path, exist_ok=True)
    return path


# --------------------------------------------------------------------------- #
# Grayscale XOR scheme
# --------------------------------------------------------------------------- #
def gray_encrypt(image, share_size):
    img = np.asarray(image)
    row, column = img.shape
    shares = np.random.randint(0, 256, size=(row, column, share_size))
    shares[:, :, -1] = img.copy()
    for i in range(share_size - 1):
        shares[:, :, -1] = shares[:, :, -1] ^ shares[:, :, i]
    return shares, img


def gray_decrypt(shares):
    row, column, share_size = shares.shape
    work = shares.copy()
    for i in range(share_size - 1):
        work[:, :, -1] = work[:, :, -1] ^ work[:, :, i]
    final = work[:, :, share_size - 1]
    return Image.fromarray(final.astype(np.uint8)), final


def run_gray_encrypt():
    path = ask_path("Path of the grayscale/any image to encrypt: ")
    image = Image.open(path).convert("L")
    print(f"Loaded image, size = {image.size}")
    share_size = ask_share_count()

    out = ensure_output("grayscale")
    shares, original = gray_encrypt(image, share_size)
    for i in range(share_size):
        Image.fromarray(shares[:, :, i].astype(np.uint8)).save(
            os.path.join(out, f"XOR_Share_{i + 1}.png")
        )
    reconstructed_img, reconstructed = gray_decrypt(shares)
    reconstructed_img.save(os.path.join(out, "Output_XOR.png"))

    print(f"\n{share_size} shares + reconstruction saved to: {out}")
    report_metrics(original, reconstructed)


def run_gray_decrypt():
    folder = ask_path("Folder containing 'XOR_Share_*.png': ")
    files = sorted(
        f for f in os.listdir(folder)
        if f.startswith("XOR_Share_") and f.endswith(".png")
    )
    if not files:
        print("No 'XOR_Share_*.png' files found in that folder.")
        return
    shares = None
    for i, name in enumerate(files):
        arr = np.asarray(Image.open(os.path.join(folder, name)))
        if shares is None:
            shares = np.zeros((*arr.shape, len(files)), dtype=np.uint8)
        elif arr.shape != shares.shape[:2]:
            print(f"Share '{name}' has mismatched dimensions.")
            return
        shares[:, :, i] = arr
    result, _ = gray_decrypt(shares)
    dest = os.path.join(folder, "Reconstructed_Image.png")
    result.save(dest)
    print(f"Reconstructed image saved to: {dest}")


# --------------------------------------------------------------------------- #
# Colour modular-arithmetic scheme
# --------------------------------------------------------------------------- #
def colour_encrypt(image, share_size):
    img = np.asarray(image)
    row, column, depth = img.shape
    shares = np.random.randint(0, 256, size=(row, column, depth, share_size))
    shares[:, :, :, -1] = img.copy()
    for i in range(share_size - 1):
        shares[:, :, :, -1] = (shares[:, :, :, -1] + shares[:, :, :, i]) % 256
    return shares, img


def colour_decrypt(shares):
    row, column, depth, share_size = shares.shape
    work = shares.copy().astype(np.int32)
    for i in range(share_size - 1):
        work[:, :, :, -1] = (work[:, :, :, -1] - work[:, :, :, i] + 256) % 256
    final = work[:, :, :, share_size - 1].astype(np.uint8)
    return Image.fromarray(final), final


def run_colour_encrypt():
    path = ask_path("Path of the colour image to encrypt: ")
    image = Image.open(path).convert("RGB")
    print(f"Loaded image, size = {image.size}")
    share_size = ask_share_count()

    out = ensure_output("colour")
    shares, original = colour_encrypt(image, share_size)
    for i in range(share_size):
        Image.fromarray(shares[:, :, :, i].astype(np.uint8)).save(
            os.path.join(out, f"MA_Share_{i + 1}.png")
        )
    reconstructed_img, reconstructed = colour_decrypt(shares)
    reconstructed_img.save(os.path.join(out, "Output_MA.png"))

    print(f"\n{share_size} shares + reconstruction saved to: {out}")
    report_metrics(original, reconstructed)


def run_colour_decrypt():
    folder = ask_path("Folder containing 'MA_Share_*.png': ")
    files = sorted(
        f for f in os.listdir(folder)
        if f.startswith("MA_Share_") and f.endswith(".png")
    )
    if not files:
        print("No 'MA_Share_*.png' files found in that folder.")
        return
    shares = None
    for i, name in enumerate(files):
        arr = np.asarray(Image.open(os.path.join(folder, name)).convert("RGB"))
        if shares is None:
            shares = np.zeros((*arr.shape, len(files)), dtype=np.uint8)
        elif arr.shape != shares.shape[:3]:
            print(f"Share '{name}' has mismatched dimensions.")
            return
        shares[:, :, :, i] = arr
    result, _ = colour_decrypt(shares)
    dest = os.path.join(folder, "Reconstructed_Image.png")
    result.save(dest)
    print(f"Reconstructed image saved to: {dest}")


# --------------------------------------------------------------------------- #
# AES-VC (delegates to the existing scripts)
# --------------------------------------------------------------------------- #
def _run_aes_script(script_name):
    try:
        import Crypto  # noqa: F401  (pycryptodome provides the 'Crypto' package)
    except ImportError:
        print(
            "\nThe AES-VC scheme needs 'pycryptodome'.\n"
            "Install it with:  pip install pycryptodome\n"
        )
        return
    subprocess.run([sys.executable, script_name], cwd=AES_DIR)


def run_aes_encrypt():
    _run_aes_script("main encrypt.py")


def run_aes_decrypt():
    _run_aes_script("main decrypte.py")


# --------------------------------------------------------------------------- #
# Menu
# --------------------------------------------------------------------------- #
MENU = """
============================================================
                 VISUAL CRYPTOGRAPHY
============================================================
  Grayscale (XOR):
    1) Encrypt an image into shares
    2) Decrypt shares back into an image

  Colour (Modular Arithmetic):
    3) Encrypt an image into shares
    4) Decrypt shares back into an image

  AES-VC (AES-256 + share-based key):
    5) Encrypt an image
    6) Decrypt an image

    0) Exit
============================================================"""

ACTIONS = {
    "1": run_gray_encrypt,
    "2": run_gray_decrypt,
    "3": run_colour_encrypt,
    "4": run_colour_decrypt,
    "5": run_aes_encrypt,
    "6": run_aes_decrypt,
}


def main():
    while True:
        print(MENU)
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            return
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice, please try again.")
            continue
        try:
            action()
        except FileNotFoundError:
            print("Error: file or folder not found.")
        except ValueError as exc:
            print(f"Error: {exc}")
        except Exception as exc:  # keep the menu alive on any failure
            print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
