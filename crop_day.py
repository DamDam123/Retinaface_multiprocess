import cv2
import sys
import numpy as np
import time
import os
import glob
from retinaface import RetinaFace
import math

thresh = 0.8
scales = [1024, 1980]

count = 1

gpuid = 0
# detector = RetinaFace('./model/R50', 0, gpuid, 'net3')
detector = RetinaFace('./mnet.25/mnet.25', 0, gpuid, 'net3')

imgPaths = []  # 存放图片路径
# angle_dir = []  # 存放角度目录
# imageFileNames = [] #存放图片名称


day = time.strftime("%Y_%m_%d", time.localtime())#获取当前时间

imageDir = r"/home/lihongxia/face_data/2019.11.4/ImageData/*"  # 原图文件路径
detectResultRootPath = r"/home/lihongxia/projects/Retinaface-master/data_set/" + day + "/detector_result"  # 人脸检测+关键点检测保存路径
cropImgRootPath = r"/home/lihongxia/projects/Retinaface-master/data_set/" + day + "/crop_Images"  # 人脸裁剪保存路径
log_path = r"/home/lihongxia/projects/Retinaface-master/log/" + day
iscropped_path = "/home/lihongxia/projects/Retinaface-master/exist_croppedImgTxt/" + day

# 创建目录
# 创建人脸检测文件夹
if not os.path.isdir(detectResultRootPath):
    os.makedirs(detectResultRootPath)
# 创建人脸裁剪文件夹
if not os.path.isdir(cropImgRootPath):
    os.makedirs(cropImgRootPath)
# 创建日志文件夹
if not os.path.isdir(log_path):
    os.makedirs(log_path)

if not os.path.isdir(iscropped_path):
    os.makedirs(iscropped_path)

# 遍历获得所有原图的路径
imgPaths = glob.glob(imageDir)
imgPaths.sort()  # 对图像路径按编号从小到大排序

# 日志文本
log_txt = os.path.join(log_path, "日志.txt")
log_f = open(log_txt, "a+")
# 打开记录已裁剪图像的文本文件
iscropped_txt = os.path.join(iscropped_path, "is_cropped.txt")
print(iscropped_txt)
is_croppedImgList = []  # 保存已经裁剪的图像的角度和图片名称
with open(iscropped_txt, 'w') as iscropped_f:
    if iscropped_f.readable():
        print("11")
        for imgname in iscropped_f.readlines():
            imgname = imgname.strip()
            print(imgname)
            is_croppedImgList.append(imgname)

print(is_croppedImgList)


log_f.write("\n")
localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
log_f.write("当前日期：" + str(localtime))
log_f.write("\n")

print("已经裁剪的图像：")
print(is_croppedImgList)
print("已经裁剪的图像总数：", len(is_croppedImgList))
log_f.write("----------------")
log_f.write("\n")
log_f.write("已经裁剪的图像总数：" + str(len(is_croppedImgList)))
log_f.write("\n")

print("总共图片：" + str(len(imgPaths)))
log_f.write("现有总共原始图片：" + str(len(imgPaths)))
crop_face = None
for j, imgPath in enumerate(imgPaths):
    print("第" + str(j) + "张")
    print("original img path:", imgPath)
    log_f.write("第" + str(j) + "张")
    log_f.write("\n")
    log_f.write("原图路径:" + str(imgPath))
    log_f.write("\n")
    img = cv2.imdecode(np.fromfile(imgPath, np.uint8), cv2.IMREAD_COLOR)
    imgPath = 'r%s' % imgPath
    imgpathlist = imgPath.split("/")
    angle_dir = imgpathlist[-2]
    imgFileName = imgpathlist[-1]
    print(angle_dir, imgFileName)
    img_angle_name = angle_dir + "_" + imgFileName
    if img_angle_name in is_croppedImgList:
        print(img_angle_name + "已经裁剪")
        log_f.write(img_angle_name + "已经裁剪")
        log_f.write("\n")
        continue

    log_f.write("开始裁剪图片：" + str(img_angle_name))
    cropImg_angleDir = os.path.join(cropImgRootPath, angle_dir)
    detectResult_angleDir = os.path.join(detectResultRootPath, angle_dir)
    if not os.path.isdir(cropImg_angleDir):
        os.makedirs(cropImg_angleDir)
    if not os.path.isdir(detectResult_angleDir):
        os.makedirs(detectResult_angleDir)

    imgCopy = img.copy()

    im_shape = img.shape
    target_size = scales[0]
    max_size = scales[1]
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    im_scale = float(target_size) / float(im_size_min)
    # prevent bigger axis from being more than max_size:
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)

    scales = [im_scale]
    flip = False

    for c in range(count):
        faces, landmarks = detector.detect(img, thresh, scales=scales, do_flip=flip)

    try:
        if faces is not None:
            print('旋转前find', faces.shape[0], 'faces')
            log_f.write('旋转前找到' + str(faces.shape[0]) + '人脸')
            log_f.write("\n")
            for i in range(faces.shape[0]):
                # print('score', faces[i][4])
                box = faces[i].astype(np.int)
                color = (255, 0, 0)
                color = (0, 0, 255)
                cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 4)
                print("face box position:x1:{}, y1:{}, x2:{}, y2:{}".format(box[0], box[1], box[2], box[3]))
                log_f.write("face box position:x1:{}, y1:{}, x2:{}, y2:{}".format(box[0], box[1], box[2], box[3]))
                log_f.write("\n")
                if box[0] < 50:
                    continue
                w = box[2] - box[0] + 60
                h = box[3] - box[1] + 20
                crop_face = imgCopy[box[1] - 30:box[1] + h, box[0] - 30:box[0] + w]
                crop_face = cv2.resize(crop_face, (224, 224), interpolation=cv2.INTER_LINEAR)
                if landmarks is not None:
                    landmark5 = landmarks[i].astype(np.int)
                    # print(landmark5.shape)
                    for l in range(landmark5.shape[0]):
                        color = (0, 0, 255)
                        if l == 0 or l == 3:
                            color = (0, 255, 0)
                        cv2.circle(img, (landmark5[l][0], landmark5[l][1]), 1, color, 3)
                    #旋转对齐
                    # left_eye, right_eye = landmark5[0], landmark5[1]
                    # print("旋转前左眼：", left_eye, end="  ")
                    # print("右眼：", right_eye)
                    #
                    # dy = right_eye[1] - left_eye[1]
                    # dx = right_eye[0] - left_eye[0]
                    #
                    # angle = math.atan2(dy, dx) * 180. / math.pi
                    # print("左右眼角度：", angle)
                    # eye_center = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)  # 左右眼中心点坐标
                    # # 旋转
                    # rotate_matrix = cv2.getRotationMatrix2D(eye_center, angle, scale=1)
                    # rotated_img = cv2.warpAffine(img, rotate_matrix, (img.shape[1], img.shape[0]))
                    # imgCopy = rotated_img.copy()
                    # # 再次检测
                    # rotate_faces, rotate_landmarks = detector.detect(rotated_img, thresh, scales=scales, do_flip=flip)
                    # if rotate_faces is not None:
                    #     print('旋转后find', rotate_faces.shape[0], 'faces')
                    #     for i in range(rotate_faces.shape[0]):
                    #         box = rotate_faces[i].astype(np.int)
                    #         cv2.rectangle(rotated_img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 4)
                    #         print("旋转后脸标记框的位置:x1:{}, y1:{}, x2:{}, y2:{}".format(box[0], box[1], box[2], box[3]))
                    #         w = box[2] - box[0] + 50
                    #         h = box[3] - box[1] + 50
                    #         crop_face = imgCopy[box[1] - 30:box[1] + h, box[0] - 30:box[0] + w]
                    #         crop_face = cv2.resize(crop_face, (224, 224), interpolation=cv2.INTER_LINEAR)
                    #         if rotate_landmarks is not None:
                    #             rotate_landmark5 = rotate_landmarks[i].astype(np.int)
                    #             print("旋转后左眼：", landmark5[0], end="  ")
                    #             print("右眼：", rotate_landmark5[1])
                    #             for l in range(rotate_landmark5.shape[0]):
                    #                 color = (0, 0, 255)
                    #                 if l == 0 or l == 3:
                    #                     color = (0, 255, 0)
                    #                 cv2.circle(rotated_img, (rotate_landmark5[l][0], rotate_landmark5[l][1]), 1, color, 3)
                    #

            detect_imageFileName = os.path.join(detectResult_angleDir, imgFileName)
            _, img = cv2.imencode('.jpg', img)
            img.tofile(detect_imageFileName)
            log_f.write('writing detect_imgPath:' + str(detect_imageFileName))
            log_f.write("\n")

            crop_imageFileName = os.path.join(cropImg_angleDir, imgFileName)
            _, crop_face = cv2.imencode('.jpg', crop_face)
            crop_face.tofile(crop_imageFileName)
            log_f.write('writing crop_imgPath:' + str(crop_imageFileName))
            log_f.write("\n")

            with open(iscropped_txt, "a+") as iscropped_f:
                iscropped_f.write(img_angle_name)
                iscropped_f.write("\n")

            scales = [1024, 1980]


    except Exception as e:
        print("没有裁剪的图像：" + str(angle_dir) + str(imgFileName))
        log_f.write("没有裁剪的图像：" + str(angle_dir) + str(imgFileName))
        log_f.write("\n")
        log_f.write("错误信息：" + str(e))
        log_f.write("\n")
    finally:
        scales = [1024, 1980]


log_f.close()  # 关闭日志文件

