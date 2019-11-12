import cv2
import sys
import numpy as np
import datetime
import os
import glob
from retinaface import RetinaFace
import math
import cv2 as cv

thresh = 0.8
scales = [1024, 1980]

count = 1

gpuid = 0
# detector = RetinaFace('./model/R50', 0, gpuid, 'net3')
detector = RetinaFace('./mnet.25/mnet.25', 0, gpuid, 'net3')

imgPaths = []  # 存放图片路径
# angle_dir = []  # 存放角度目录
# imageFileNames = [] #存放图片名称

imageDir = r'/home/lihongxia/projects/Retinaface-master/SCUT-FBP5500_v2_asian/ImageData/*/*.jpg'
detectResultRootPath = r'/home/lihongxia/projects/Retinaface-master/SCUT-FBP5500_v2_asian/detector_result'  # 人脸检测存放目录
cropImgRootPath = r'/home/lihongxia/projects/Retinaface-master/SCUT-FBP5500_v2_asian/crop_Images'  # 人脸裁剪结果存放目录

# 创建目录
if not os.path.isdir(detectResultRootPath):
    os.makedirs(detectResultRootPath)
if not os.path.isdir(cropImgRootPath):
    os.makedirs(cropImgRootPath)

imgPaths = glob.glob(imageDir)
imgPaths.sort()  # 对图像路径按编号从小到大排序
# for path in imgPaths:
#     print(path)
#
# imgPaths.sort()
#
# print(imgPaths)
# for imgPath in imgPaths:
#     imgPath = repr(imgPath)
#     # imgPaths.append(glob.glob(os.path.join(imageDir, imgFileName)))
#     # imgFileName.split("\\\\")
#     # print("split imgfilename", imgFileName.split("\\\\"))
#     dir = imgPath.split("\\\\")[4]
#     imgFileName = imgPath.split("\\\\")[5]
#     if dir not in angle_dir:
#         angle_dir.append(dir)
#     if imgFileName not in imageFileNames:
#         imageFileNames.append(imgFileName)
#
# angle_dir.sort()
#
# # 创建存放裁剪后的人脸的角度目录
# for dir in angle_dir:
#     detectResult_angleDir = os.path.join(detect_resultRootPath, dir)
#     cropImg_angleDir = os.path.join(cropImgRootPath, dir)
#     # print(detect_result_angle_dir)
#     if not os.path.isdir(detectResult_angleDir):
#         os.makedirs(detectResult_angleDir)
#     if not os.path.isdir(cropImg_angleDir):
#         os.makedirs(cropImg_angleDir)


print("总共图片：" + str(len(imgPaths)))
crop_face = None
for j, imgPath in enumerate(imgPaths):
    print("第" + str(j) + "张")
    print("original img path:", imgPath)
    img = cv2.imdecode(np.fromfile(imgPath, np.uint8), cv2.IMREAD_COLOR)
    imgPath = 'r%s' % imgPath
    # print(imgPath.split("/"))
    angle_dir = imgPath.split("/")[7]
    imgFileName = imgPath.split("/")[8]
    print(angle_dir, imgFileName)
    cropImg_angleDir = os.path.join(cropImgRootPath, angle_dir)
    detectResult_angleDir = os.path.join(detectResultRootPath, angle_dir)
    if not os.path.isdir(cropImg_angleDir):
        os.makedirs(cropImg_angleDir)
    if not os.path.isdir(detectResult_angleDir):
        os.makedirs(detectResult_angleDir)

    imgCopy = img.copy()

    im_shape = img.shape
    # print(scales)
    target_size = scales[0]
    # print(target_size)
    max_size = scales[1]
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    # im_scale = 1.0
    # if im_size_min>target_size or im_size_max>max_size:
    im_scale = float(target_size) / float(im_size_min)
    # prevent bigger axis from being more than max_size:
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)

    # print('im_scale', im_scale)

    scales = [im_scale]
    flip = False

    for c in range(count):
        faces, landmarks = detector.detect(img, thresh, scales=scales, do_flip=flip)
        # print(c, faces.shape, landmarks.shape)

    try:
        if faces is not None:
            print('旋转前find', faces.shape[0], 'faces')
            for i in range(faces.shape[0]):
                print('score', faces[i][4])
                box = faces[i].astype(np.int)
                color = (255, 0, 0)
                color = (0, 0, 255)
                cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 4)
                print("face box position:x1:{}, y1:{}, x2:{}, y2:{}".format(box[0], box[1], box[2], box[3]))
                w = box[2] - box[0] + 30
                h = box[3] - box[1] + 20
                crop_face = imgCopy[box[1] - 30:box[1] + h, box[0] - 30:box[0] + w]
                crop_face = cv2.resize(crop_face, (224, 224), interpolation=cv2.INTER_LINEAR)
                if landmarks is not None:
                    landmark5 = landmarks[i].astype(np.int)
                    print(landmark5.shape)
                    for l in range(landmark5.shape[0]):
                        color = (0, 0, 255)
                        if l == 0 or l == 3:
                            color = (0, 255, 0)
                        cv2.circle(img, (landmark5[l][0], landmark5[l][1]), 1, color, 3)
                """
                left_eye, right_eye = landmark5[0], landmark5[1]
                print("旋转前左眼：", left_eye, end="  ")
                print("右眼：", right_eye)

                dy = right_eye[1] - left_eye[1]
                dx = right_eye[0] - left_eye[0]

                angle = math.atan2(dy, dx) * 180. / math.pi
                print("左右眼角度：", angle)
                eye_center = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)  # 左右眼中心点坐标
                # 旋转
                rotate_matrix = cv2.getRotationMatrix2D(eye_center, angle, scale=1)
                rotated_img = cv2.warpAffine(img, rotate_matrix, (img.shape[1], img.shape[0]))
                imgCopy = rotated_img.copy()
                # 再次检测
                rotate_faces, rotate_landmarks = detector.detect(rotated_img, thresh, scales=scales, do_flip=flip)
                if rotate_faces is not None:
                    print('旋转后find', rotate_faces.shape[0], 'faces')
                    for i in range(rotate_faces.shape[0]):
                        box = rotate_faces[i].astype(np.int)
                        cv2.rectangle(rotated_img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 4)
                        print("旋转后脸标记框的位置:x1:{}, y1:{}, x2:{}, y2:{}".format(box[0], box[1], box[2], box[3]))
                        w = box[2] - box[0] + 50
                        h = box[3] - box[1] + 50
                        crop_face = imgCopy[box[1] - 30:box[1] + h, box[0] - 30:box[0] + w]
                        crop_face = cv2.resize(crop_face, (224, 224), interpolation=cv2.INTER_LINEAR)
                        if rotate_landmarks is not None:
                            rotate_landmark5 = rotate_landmarks[i].astype(np.int)
                            print("旋转后左眼：", landmark5[0], end="  ")
                            print("右眼：", rotate_landmark5[1])
                            for l in range(rotate_landmark5.shape[0]):
                                color = (0, 0, 255)
                                if l == 0 or l == 3:
                                    color = (0, 255, 0)
                                cv2.circle(rotated_img, (rotate_landmark5[l][0], rotate_landmark5[l][1]), 1, color, 3)
                """
        detect_imageFileName = os.path.join(detectResultRootPath, imgFileName)
        print('writing detect_imgPath:', detect_imageFileName)
        _, img = cv2.imencode('.jpg', img)
        img.tofile(detect_imageFileName)
        # cv2.imwrite(detect_imageFileName, img)

        crop_imageFileName = os.path.join(cropImgRootPath, imgFileName)
        print('writing crop_imgPath:', crop_imageFileName)
        _, crop_face = cv2.imencode('.jpg', crop_face)
        crop_face.tofile(crop_imageFileName)
        # cv2.imwrite(crop_imageFileName, crop_face)
        scales = [1024, 1980]

    except Exception as e:
        print("错误" + str(e))
        print("报错" + str(angle_dir) + str(imgFileName))
    finally:
        scales = [1024, 1980]


