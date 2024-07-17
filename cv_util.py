import time
import cv2
import numpy as np


def zhaotu(large_image_path, small_image_path):
    # 读取大图和小图
    large_image = cv2.imread(large_image_path)
    small_image = cv2.imread(small_image_path)

    # 转换为灰度图
    large_image_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    small_image_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    # 初始化 SIFT 检测器
    sift = cv2.SIFT_create()

    # 检测关键点和计算描述符
    keypoints1, descriptors1 = sift.detectAndCompute(small_image_gray, None)
    keypoints2, descriptors2 = sift.detectAndCompute(large_image_gray, None)

    # 使用 BFMatcher 进行特征匹配
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # 调整 Lowe's ratio test 的阈值
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # 确保有足够的匹配点
    threshold = 30
    if len(good_matches) > threshold:
        print('matches found : {}/{}'.format(len(good_matches), threshold))
        # 获取关键点位置
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算单应性变换
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()

        # 获取小图的四个角
        h, w = small_image_gray.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        # 中心(x,y), (宽,高), 旋转角度
        rect = cv2.minAreaRect(dst)
        print('rect:', rect)

        return rect
    
    return None

def test():
    # 读取大图和小图
    large_image = cv2.imread('pic/screenshot.png')
    small_image = cv2.imread('pic/fudai.png')

    # 转换为灰度图
    large_image_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    small_image_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    cv2.imshow('large gray', large_image_gray)
    cv2.imshow('small gray', small_image_gray)

    # 初始化 SIFT 检测器
    sift = cv2.SIFT_create()

    # 检测关键点和计算描述符
    keypoints1, descriptors1 = sift.detectAndCompute(small_image_gray, None)
    keypoints2, descriptors2 = sift.detectAndCompute(large_image_gray, None)

    # 使用 BFMatcher 进行特征匹配
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)
    print("matches : {}".format(matches))

    # 调整 Lowe's ratio test 的阈值
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # 确保有足够的匹配点
    threshold = 30
    if len(good_matches) > threshold:
        print('matches found : {}/{}'.format(len(good_matches), threshold))
        # 获取关键点位置
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算单应性变换
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()

        # 获取小图的四个角
        h, w = small_image_gray.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        # 在大图上绘制框
        large_image = cv2.polylines(large_image, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('find small in large', large_image)

        # 显示匹配结果
        draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None, matchesMask=matches_mask, flags=2)
        img_matches = cv2.drawMatches(small_image, keypoints1, large_image, keypoints2, good_matches, None, **draw_params)

        # 调整图像大小以适应显示窗口
        max_width = 800
        max_height = 600
        height, width = img_matches.shape[:2]
        if width > max_width or height > max_height:
            scaling_factor = min(max_width / width, max_height / height)
            new_size = (int(width * scaling_factor), int(height * scaling_factor))
            img_matches = cv2.resize(img_matches, new_size, interpolation=cv2.INTER_AREA)

        cv2.imshow('Matches', img_matches)
        cv2.waitKey(0)
    else:
        print("Not enough matches found - {}/{}".format(len(good_matches), threshold))

    if cv2.waitKey(1) & 0xFF == ord('q'): exit()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # test()
    zhaotu('pic/screenshot.png', 'pic/fudai.png')
    pass