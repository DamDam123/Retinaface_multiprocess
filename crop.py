import cv2
import numpy as np
import time
import os
import glob
from retinaface import RetinaFace
import math


def crop(dstpath, number, img_angle_paths):
    """
    按角度通过多进程进行裁图
    :param dstpath: 裁剪图、检测图、日志和已裁剪的保存根目录
    :param number: 进程编号
    :param img_angle_paths: 按角度将文件分成列表
    """
    print("当前进程：%s" % os.getpid())

    print(dstpath)
    print(number)
    thresh = 0.8
    scales = [1024, 1980]

    count = 1
    gpuid = 0

    detector = RetinaFace('./mnet.25/mnet.25', 0, gpuid, 'net3')

    # 获得存放图片的绝对路径列表
    imgPaths = []
    for path in img_angle_paths:
        imgPaths += glob.glob(os.path.join(path, "*.jpg"))
    imgPaths.sort()

    # 在dstpath文件夹下创建cropImage、detect_result、log、iscropped文件夹
    detectresult_path = os.path.join(dstpath, "detect_result")
    cropresult_path = os.path.join(dstpath, "crop_result")
    log_path = os.path.join(dstpath, "log")
    iscropped_path = os.path.join(dstpath, "iscropped")
    if not os.path.isdir(detectresult_path):
        os.makedirs(detectresult_path)
    if not os.path.isdir(cropresult_path):
        os.makedirs(cropresult_path)
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    if not os.path.isdir(iscropped_path):
        os.makedirs(iscropped_path)

    day = time.strftime("%Y_%m_%d %H:%M", time.localtime())  # 获取当前时间

    # 按进程编号创建日志文本
    log_txt = os.path.join(log_path, str(number) + "_日志.txt")  # 日志路径
    log_f = open(log_txt, "a+")
    log_f.write("-----------------------------" + "\n")
    log_f.write("当前时间：" + str(day) + "\n")
    log_f.write("当前进程：%s" % os.getpid() + "\n")

    is_cropped_img_pathList = []
    is_cropped_txt = os.path.join(iscropped_path, str(number) + "_已裁剪.txt")
    is_cropped_f = open(is_cropped_txt, "a+")
    if is_cropped_f.readable():
        for imgname in is_cropped_f.readlines():
            imgname = imgname.strip()
            print(imgname)
            is_cropped_img_pathList.append(imgname)

    is_cropped_img_pathList.sort()
    print(is_cropped_img_pathList)

    print("已经裁剪的图像总数：", len(is_cropped_img_pathList))
    log_f.write("-----------------------------" + "\n")
    log_f.write("已经裁剪的图像总数：" + str(len(is_cropped_img_pathList)) + "\n")
    print("总共图片：" + str(len(imgPaths)))
    log_f.write("当前进程" + str(os.getpid()) + "总共图片：" + str(len(imgPaths)) + "\n")

    crop_face = None
    for j, imgPath in enumerate(imgPaths):
        print("第" + str(j) + "张")
        print("original img path:", imgPath)
        log_f.write("第" + str(j) + "张" + "\n")
        log_f.write("原图路径:" + str(imgPath) + "\n")
        img = cv2.imdecode(np.fromfile(imgPath, np.uint8), cv2.IMREAD_COLOR)
        imgPath = 'r%s' % imgPath
        # imgpathlist = imgPath.split("/")
        imgpathlist = imgPath.split("\\")
        angle_dir = imgpathlist[-2]
        imgFileName = imgpathlist[-1]
        print(angle_dir, imgFileName)

        # 创建crop角度子文件夹
        cropImg_angleDir = os.path.join(cropresult_path, angle_dir)
        # 创建detect角度子文件夹
        detectResult_angleDir = os.path.join(detectresult_path, angle_dir)
        if not os.path.isdir(cropImg_angleDir):
            os.makedirs(cropImg_angleDir)
        if not os.path.isdir(detectResult_angleDir):
            os.makedirs(detectResult_angleDir)

        img_angle_name = angle_dir + "_" + imgFileName
        if img_angle_name in is_cropped_img_pathList:
            print(img_angle_name + "已经裁剪")
            log_f.write(img_angle_name + "已经裁剪" + "\n")
            continue

        log_f.write("开始裁剪图片：" + str(img_angle_name) + "\n")

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
                    print('旋转前找到', faces.shape[0], '个脸')
                    log_f.write('旋转前找到' + str(faces.shape[0]) + '人脸')
                    log_f.write("\n")
                    for i in range(faces.shape[0]):
                        # print('score', faces[i][4])
                        box = faces[i].astype(np.int)
                        color = (0, 0, 255)
                        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 4)
                        print("face box position:x1:{}, y1:{}, x2:{}, y2:{}".format(box[0], box[1], box[2], box[3]))
                        log_f.write(
                            "face box position:x1:{}, y1:{}, x2:{}, y2:{}".format(box[0], box[1], box[2], box[3]))
                        log_f.write("\n")
                        if box[0] < 50:
                            continue
                        #原裁图方式
                        # w = box[2] - box[0] + 60
                        # h = box[3] - box[1] + 20
                        # crop_face = imgCopy[box[1] - 40:box[1] + h, box[0] - 30:box[0] + w]
                        #现按左右脸和0度分开裁，两个角点的位置不一致
                        x1, y1 = box[0], box[1]
                        x2, y2 = box[2], box[3]
                        if "-" in angle_dir:
                            print("-")
                            crop_face = imgCopy[y1 - 5: y2 + 5, x1: x2 + 50]
                        elif "+" in angle_dir:
                            print("+")
                            # w = x2 - x1
                            # h = y2 - y1
                            crop_face = imgCopy[y1 - 5: y2 + 5, x1 - 50: x2]
                        elif "0_0" == angle_dir:
                            print("0_0")
                            crop_face = imgCopy[y1 - 5: y2 + 5, x1 - 60: x2 + 60]
                        else:
                            crop_face = imgCopy[y1 - 5: y2 + 5, x1 - 30: x2 + 30]
                        crop_face = cv2.resize(crop_face, (224, 224), interpolation=cv2.INTER_LINEAR)
                        if landmarks is not None:
                            landmark5 = landmarks[i].astype(np.int)
                            # print(landmark5.shape)
                            for l in range(landmark5.shape[0]):
                                color = (0, 0, 255)
                                if l == 0 or l == 3:
                                    color = (0, 255, 0)
                                cv2.circle(img, (landmark5[l][0], landmark5[l][1]), 1, color, 3)

                            """
                            #旋转对齐
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

                    detect_imageFileName = os.path.join(detectResult_angleDir, imgFileName)
                    _, img = cv2.imencode('.jpg', img)
                    img.tofile(detect_imageFileName)
                    print('writing detect_imgPath:' + str(detect_imageFileName))
                    log_f.write('writing detect_imgPath:' + str(detect_imageFileName) + "\n")

                    crop_imageFileName = os.path.join(cropImg_angleDir, imgFileName)
                    _, crop_face = cv2.imencode('.jpg', crop_face)
                    crop_face.tofile(crop_imageFileName)
                    print('writing crop_imgPath:' + str(crop_imageFileName))
                    log_f.write('writing crop_imgPath:' + str(crop_imageFileName) + "\n")

                    is_cropped_f.write(img_angle_name + "\n")

                    scales = [1024, 1980]

            except Exception as e:
                print("没有裁剪的图像：" + str(angle_dir) + str(imgFileName))
                log_f.write("没有裁剪的图像：" + str(angle_dir) + str(imgFileName) + "\n")
                log_f.write("错误信息：" + str(e) + "\n")
                log_f.write("\n")
            finally:
                scales = [1024, 1980]

    log_f.close()  # 关闭日志文件
    is_cropped_f.close()
