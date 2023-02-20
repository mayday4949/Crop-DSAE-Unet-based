from PIL import Image

def count_non_black_pixels(image_path):
    # 打开图片
    image = Image.open(image_path)

    # 将图片转换为 RGB 模式，以便读取每个像素的 RGB 值
    image = image.convert('RGB')

    # 计算非黑色像素点的数量
    count = 0
    width, height = image.size
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if r != 0 or g != 0 or b != 0:
                count += 1

    return count


if __name__ == "__main__":
    image1_path = 'Imgs\input\input_204291.jpg'
    non_black_pixel_count = count_non_black_pixels(image1_path)
    image2_path = 'Imgs\output\input_204291_78.jpg'
    white_pixel_count = count_non_black_pixels(image2_path)
    print("input 非黑色个数")
    print(non_black_pixel_count)
    print("output 白色个数")
    print(white_pixel_count)
    print("白色个数/非黑色个数")
    print(white_pixel_count/non_black_pixel_count)
    
