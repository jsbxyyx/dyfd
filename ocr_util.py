import cv2
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch")


def ocr_img(image_path):
    # 读取图片文件
    img = cv2.imread(image_path)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # 识别图片中的文字
    result = ocr.ocr(img)
    return result[0]
