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
2. Follow the on-screen instructions to upload an image, choose encryption parameters, and generate encrypted shares.

3. To decrypt, upload the necessary shares and follow the instructions to reconstruct the original image.

## Examples

### Encrypting an Image

1. Upload an image file.
2. Choose the number of shares and threshold.
3. Generate and save the encrypted shares.

### Decrypting an Image

1. Upload the required number of shares.
2. Combine the shares to reconstruct the original image.

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

