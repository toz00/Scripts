import sys
from PIL import Image
import random

def encode_message(image_path, message):
    """
    Encode a message in the pixel values of a PNG image.
    
    Args:
        image_path (str): The path to the input PNG image.
        message (str): The message to be encoded.
    
    Returns:
        The modified image with the message encoded.
    """
    # Open the image
    image = Image.open(image_path)
    
    # Convert the image to RGBA mode if necessary
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    # Get the image dimensions
    width, height = image.size
    
    # Convert the message to bytes
    message_bytes = message.encode("utf-8")
    
    # Encode the message in the pixel values
    pixel_data = list(image.getdata())
    for i, byte in enumerate(message_bytes):
        x = i % width
        y = i // width
        r, g, b, a = pixel_data[y * width + x]
        pixel_data[y * width + x] = (r ^ byte, g ^ byte, b ^ byte, a)
    
    # Update the image with the modified pixel data
    image.putdata(pixel_data)

    image_path=image_path[:image_path.rfind('.')]

    image.save(image_path + "encoded.png", "PNG", quality='keep')

def decode_message(image_path):
    """
    Decode a message from the pixel values of a PNG image.
    
    Args:
        image_path (str): The path to the input PNG image.
    
    Returns:
        The decoded message, or None if no message is found.
    """
    # Open the image
    image = Image.open(image_path)
    
    # Convert the image to RGBA mode if necessary
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    # Get the image dimensions
    width, height = image.size
    
    # Decode the message from the pixel values
    pixel_data = list(image.getdata())
    message_bytes = bytearray()
    for i in range(width * height):
        x = i % width
        y = i // width
        r, g, b, a = pixel_data[y * width + x]
        message_bytes.append(r ^ g ^ b)
    
    # Try to decode the message as UTF-8
    try:
        message = message_bytes.decode("utf-8")
        return message
    except UnicodeDecodeError:
        return "erreur"
    
def main():
    if len(sys.argv) == 3:
        encode_message(sys.argv[1], sys.argv[2])
        print("Deux arguments, encode")
    elif len(sys.argv) == 2:
        print(decode_message(sys.argv[1]))
        print("un argument, décode")
    else:
        print("Erreur : le script doit être exécuté avec un ou deux paramètres.")

if __name__ == "__main__":
    main()