from img_convert.utils.io import ConvertImg

if __name__ == '__main__':
    image_path = 'Karina.png'
    #
    img = ConvertImg()
    img.to_pencil_sketch(image_path)

