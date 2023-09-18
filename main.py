import os
import zlib


def main():
    img = open('pixel_art.png', 'rb')
    mod_img = open('processed.png', 'wb')

    # Useful indexes
    mod_bytearray = bytearray()

    seek_idat_start(img)
    idat_index = img.tell()
    img.seek(0, 0)

    # PNG Header, IHDR chunk, plus any other chunks between IHDR and IDAT
    for i in range(0, idat_index):
        byte = img.read(1)
        mod_bytearray.extend(byte)

    img.seek(4, os.SEEK_CUR)
    data_length = int.from_bytes(img.read(4), 'big')

    compressed_image_data = img.read(data_length)  # Image data
    decompressed_image_data = decompress_image(compressed_image_data)
    decompressed_length = len(decompressed_image_data)

    modified_data = bytearray()
    image = [[]]
    filtering_method = []
    for r in range(0, 10):
        filtering_method[r] = decompressed_image_data[31 * r]
        for c in range(1, 31):
            image[r][c-1] = decompressed_image_data[31 * r + c]

    for i in range(0, 10):
        row
        if filtering_method[i] == 0:
            # None
            for num in range(0, 10):

        elif filtering_method[i] == 1:
            # Sub
        elif filtering_method[i] == 2:
            # Up
        elif filtering_method[i] == 3:
            # Average
        elif filtering_method[i] == 4:
            # Paeth

    # modified_data = bytearray()
    # for i in range(0, rgb_vals, 3):
    #     r = decompressed_image_data[i]
    #     g = decompressed_image_data[i + 1]
    #     b = decompressed_image_data[i + 2]
    #     print(r, g, b)
    #     gray = int(0.299*r+0.587*g+0.114*b)  # Compute the average of RGB channels for grayscale value
    #     modified_data.extend([gray, gray, gray])

    if decompressed_length % 3 == 1:
        modified_data.extend([decompressed_image_data[decompressed_length-1]])
    elif decompressed_length % 3 == 2:
        modified_data.extend([decompressed_image_data[decompressed_length-2], decompressed_image_data[decompressed_length-1]])
    recompressed_image_data = compress_image(bytes(modified_data))

    # IDAT data length and type
    idat_type = [b'I', b'D', b'A', b'T']
    recompressed_data_length = len(recompressed_image_data)
    mod_bytearray.extend(recompressed_data_length.to_bytes(4, 'big'))
    for byte in idat_type:
        mod_bytearray.extend(byte)

    # IDAT modified data
    mod_bytearray.extend(recompressed_image_data)

    # IDAT CRC32 checksum
    crc32_value = zlib.crc32(b'IDAT' + recompressed_image_data, 0)
    crc32_bytes = crc32_value.to_bytes(4, 'big')
    mod_bytearray.extend(crc32_bytes)

    # IEND chunk
    while True:
        byte = img.read(1)
        if byte == b'':
            break
        mod_bytearray.extend(byte)

    # Final write
    mod_img.write(mod_bytearray)

    img.close()
    mod_img.close()


def decompress_image(data):
    try:
        decompressed_data = zlib.decompress(data)
        return decompressed_data
    except zlib.error as e:
        raise Exception("Decompression error:", e)


def compress_image(data):
    try:
        compressed_data = zlib.compress(data)
        return compressed_data
    except zlib.error as e:
        raise Exception("Compression error:", e)


def seek_idat_start(img):
    while True:
        byte = img.read(1)
        if byte == b'':
            # Reached the end of the file without finding IDAT
            raise Exception("No IDAT chunk found")
        if byte == b'I':
            if img.read(3) == b'DAT':
                img.seek(-8, os.SEEK_CUR)  # Seek to the beginning of the IDAT chunk
                break
            else:
                img.seek(-3, os.SEEK_CUR)  # Undo the 3 byte read


main()
