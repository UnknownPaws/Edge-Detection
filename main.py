import zlib


def main():
    img = open('lions.png', 'rb')
    mod_img = open('processed_lions.png', 'wb')

    pre_data = img.read(179)  # All the chunks before the IDAT chunk plus the length and type bytes (8 bytes combined) from the IDAT chunk
    compressed_image_data = img.read(1106450)  # Image data
    decompressed_image_data = decompress_image(compressed_image_data)
    post_data = img.read(16)  # CRC32 of IDAT chunk plus the IEND chunk

    modified_data = bytearray()
    for i in range(0, len(decompressed_image_data)-2, 3):
        r = decompressed_image_data[i]
        g = decompressed_image_data[i + 1]
        b = decompressed_image_data[i + 2]
        average = (r + g + b) // 3  # Compute the average of RGB channels for grayscale value
        modified_data.extend([average, average, average])

    # Write "new" data to a new file
    mod_img.write(pre_data)
    mod_img.write(compress_image(modified_data))
    mod_img.write(post_data)

    img.close()
    mod_img.close()


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
