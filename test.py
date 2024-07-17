import cv2
import ocr_util


def main():
    ss = cv2.imread("pic/screenshot.png")

    rect = (
        (216.0415802001953, 366.7724914550781),
        (113.06156158447266, 112.87445831298828),
        89.58692932128906,
    )

    wh = rect[1]
    w = int(wh[0])
    h = int(wh[1])

    xy = rect[0]
    x = int(xy[0]) - (w // 2)
    y = int(xy[1]) - (h // 2)

    crop = ss[y : y + h, x : x + w]
    cv2.imshow("crop", crop)
    cv2.waitKey(0)

    cv2.imwrite("pic/fudai_jietu.png", crop)

    ocr_result = ocr_util.ocr_img("pic/fudai_jietu.png")
    print(ocr_result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit()
    cv2.destroyAllWindows()

    pass


if __name__ == "__main__":
    main()
    pass
