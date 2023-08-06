import cv2

class ConvertImg:
    def to_pencil_sketch(self, img):
        img_original = cv2.imread(img)
        img_grayscale = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        inverted_image = 255 - img_grayscale
        blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
        inverted_blurred = 255 - blurred
        pencil_sketch = cv2.divide(img_grayscale, inverted_blurred, scale=256.0)
        cv2.imshow('Original Image', img_original)
        cv2.imshow('Original Image', pencil_sketch)
        cv2.waitKey(0)


