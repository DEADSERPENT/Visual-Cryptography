# Visual Cryptography

Visual Cryptography is an encryption technique that allows for the secure transmission of images. This repository provides an implementation of visual cryptography algorithms and showcases how images can be encrypted and decrypted using these methods.

## Features

- **Encryption and Decryption**: Easily encrypt images into multiple shares and decrypt them back to the original image.
- **Support for Various Image Formats**: Compatible with common image formats like PNG, JPEG, and BMP.
- **User-friendly Interface**: Simple and intuitive interface for users to upload, encrypt, and decrypt images.
- **Customizable Parameters**: Adjust encryption parameters such as the number of shares and the threshold for decryption.
- **High Security**: Ensures that individual shares do not reveal any information about the original image unless combined correctly.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries (listed in `requirements.txt`)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/DEADSERPENT/visual-cryptography.git
    ```
2. Navigate to the project directory:
    ```bash
    cd visual-cryptography
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Run the main script to start the application:
    ```bash
    python main.py
    ```
2. Choose an option from the menu:

    | Option | Scheme | Action |
    | ------ | ------ | ------ |
    | 1 / 2  | Grayscale (XOR) | Encrypt into shares / Decrypt shares |
    | 3 / 4  | Colour (Modular Arithmetic) | Encrypt into shares / Decrypt shares |
    | 5 / 6  | AES-VC (AES-256 + share-based key) | Encrypt / Decrypt |

3. Follow the on-screen prompts to provide an image path (for encryption) or a
   folder of shares (for decryption). Generated shares and reconstructions are
   written to the `output/` directory.

## Examples

Sample images are provided in the `Example imges/` folder.

### Encrypting an Image

1. Start `python main.py` and pick option **1** (grayscale) or **3** (colour).
2. Enter the path to your image, e.g. `Example imges/spectre logo.png`.
3. Choose the number of shares (2–8); the shares and a reconstructed preview are
   saved under `output/`.

### Decrypting an Image

1. Start `python main.py` and pick option **2** (grayscale) or **4** (colour).
2. Enter the folder that contains the generated share images
   (`XOR_Share_*.png` or `MA_Share_*.png`).
3. The original image is reconstructed and saved as `Reconstructed_Image.png`
   in that folder.

## Project Structure

```
main.py                     # Unified menu-driven entry point
requirements.txt            # Python dependencies
Example imges/              # Sample input images
Visual-Cryptography-main/
├── Grayscale Images/       # XOR-based (n, n) scheme + metrics
├── Colour Images/          # Modular-arithmetic (n, n) scheme + metrics
├── AES-VC/                 # AES-256 + visual-cryptography key sharing
└── utils/                  # PSNR / normalised cross-correlation helpers
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Reference Paper/Project](link to reference)
- Contributors and their GitHub profiles

