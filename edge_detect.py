from PIL import Image
import math


def main():
    img = Image.open('cat.png')
    grayscale_img = Image.new('RGB', img.size)
    blur_img = Image.new('RGB', img.size)
    sobel_img = Image.new('RGB', img.size)

    pixel_data = list(img.getdata())

    grayscale(img, grayscale_img)
    grayscale_img.save('grayscale.png')

    gaussian_blur(grayscale_img, blur_img, 5)
    blur_img.save('gaussian_blur.png')

    sobel_detection(blur_img, sobel_img)
    sobel_img.save('processed_cat.png')


def grayscale(img, mod_img):
    for row in range(img.size[0]):
        for col in range(img.size[1]):
            r, g, b = img.getpixel((row, col))

            # Calculate the grayscale value using the luminance formula
            # gray = 0.299*R + 0.587*G + 0.114*B
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)

            mod_img.putpixel((row, col), (gray, gray, gray))


def gaussian_blur(img, mod_img, radius):
    width, height = img.size
    kernel = gaussian_kernel(radius)

    for col in range(width):
        for row in range(height):
            r_sum, g_sum, b_sum, weight_sum = 0, 0, 0, 0

            for i in range(-radius, radius + 1):
                for j in range(-radius, radius + 1):
                    if 0 <= col + i < width and 0 <= row + j < height:
                        r, g, b = img.getpixel((col + i, row + j))
                        kernel_value = kernel[i + radius][j + radius]

                        r_sum += r * kernel_value
                        g_sum += g * kernel_value
                        b_sum += b * kernel_value
                        weight_sum += kernel_value

            if weight_sum > 0:
                r_sum = int(r_sum / weight_sum)
                g_sum = int(g_sum / weight_sum)
                b_sum = int(b_sum / weight_sum)

            mod_img.putpixel((col, row), (r_sum, g_sum, b_sum))


def gaussian_kernel(radius):
    size = 2 * radius + 1
    kernel = []

    for i in range(0, size):
        row = []
        for j in range(0, size):
            koffset_x = i - radius
            koffset_y = j - radius
            # Gaussian Function
            kernel_val = (1 / (2 * math.pi * radius**2)) * math.exp(-(koffset_x**2 + koffset_y**2) / (2 * radius**2))
            row.append(kernel_val)
        kernel.append(row)

    # Normalize the kernel
    kernel_sum = sum(sum(row) for row in kernel)
    kernel = [[value / kernel_sum for value in row] for row in kernel]

    return kernel


def sobel_detection(img, mod_img):
    width, height = img.size

    # Define the Sobel operator kernels
    sobel_kernel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_kernel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # The ranges are such that the kernels don't go out of bounds
    for col in range(1, width - 1):
        for row in range(1, height - 1):
            r_x, g_x, b_x = 0, 0, 0
            r_y, g_y, b_y = 0, 0, 0

            # Apply the Sobel operator for both X and Y directions
            for i in range(3):
                for j in range(3):
                    x_offset, y_offset = col + i - 1, row + j - 1
                    r, g, b = img.getpixel((x_offset, y_offset))

                    r_x += r * sobel_kernel_x[i][j]
                    g_x += g * sobel_kernel_x[i][j]
                    b_x += b * sobel_kernel_x[i][j]

                    r_y += r * sobel_kernel_y[i][j]
                    g_y += g * sobel_kernel_y[i][j]
                    b_y += b * sobel_kernel_y[i][j]

            # Calculate the gradient magnitude using formula found online
            gradient = int(math.sqrt(r_x**2 + g_x**2 + b_x**2 + r_y**2 + g_y**2 + b_y**2))
            mod_img.putpixel((col, row), (gradient, gradient, gradient))


main()
