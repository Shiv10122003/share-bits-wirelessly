import sys
import base64
import qrcode
import urllib.parse
import os
import argparse

WEB_URL_PREFIX = "https://amanraox.github.io/share-bits-wirelessly/dl.html"
CHUNK_SIZE = 2000  # Adjust this as needed for QR code capacity

def validate_file(input_filename):
    """Check if the input file exists and is a valid file."""
    if not os.path.isfile(input_filename):
        raise FileNotFoundError(f"The file {input_filename} does not exist.")

def encode_file(input_filename):
    """Encode the file to base64."""
    with open(input_filename, "rb") as f:
        file_data = f.read()
    return base64.b64encode(file_data).decode('ascii')

def chunk_data(data, chunk_size):
    """Yield successive chunks of data."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def generate_qr_code(url, output_filename, chunk_index=None):
    """Generate QR code and save it."""
    qr_img = qrcode.make(url)
    filename = f"{output_filename}_qr.png" if chunk_index is None else f"{output_filename}_qr_{chunk_index}.png"
    qr_img.save(filename)
    print(f"QR code saved as {filename}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate a QR code for a file.")
    parser.add_argument("input_filename", help="The input file to encode")
    parser.add_argument(
        "output_filename",
        nargs="?",
        help="The output filename (default: same as input filename)",
        default=None
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    input_filename = args.input_filename
    output_filename = args.output_filename or input_filename

    try:
        validate_file(input_filename)
        b64_file_data = encode_file(input_filename)
        url_file_data = urllib.parse.quote_plus(b64_file_data)
        
        chunks = list(chunk_data(url_file_data, CHUNK_SIZE))
        for idx, chunk in enumerate(chunks):
            full_url = f"{WEB_URL_PREFIX}?f={output_filename}#{chunk}"
            generate_qr_code(full_url, output_filename, idx if len(chunks) > 1 else None)
        
    except FileNotFoundError as e:
        print(e)
    except (OSError, IOError) as e:
        print(f"File operation error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
