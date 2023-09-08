import zlib


# This code is all temporary and is only for testing deflate decompression using zlib
def main():
    img = open('lions.png', 'rb')
    mod_img = open('processed_lions.png', 'wb')

    pre_data = img.read(179)  # All the chunks before the IDAT chunk plus the length and type bytes (8 bytes combined) from the IDAT chunk
    compressed_image_data = img.read(1106450)  # Image data

    # Decompress and recompress just to make sure it will go back to its original state
    decompressed_image_data = decompress_image(compressed_image_data)
    recompressed_image_data = compress_image(decompressed_image_data)

    post_data = img.read(16)  # CRC32 of IDAT chunk plus the IEND chunk

    # Write "new" data to a new file
    mod_img.write(pre_data)
    mod_img.write(recompressed_image_data)
    mod_img.write(post_data)

    img.close()
    mod_img.close()

    print(decompressed_image_data)


def decompress_image(data):
    try:
        decompressed_data = zlib.decompress(data)
        return decompressed_data
    except zlib.error as e:
        print("Decompression error:", e)
        return None


def compress_image(data):
    try:
        compressed_data = zlib.compress(data)
        return compressed_data
    except zlib.error as e:
        print("Compression error:", e)
        return None


main()
