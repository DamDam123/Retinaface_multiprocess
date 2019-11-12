"""
重命名图片名称，去除图片名的空格
"""

import os
import glob

rootpath = r"/home/lihongxia/人脸照片信息/中北大学+警察学院2019.11.1/中北大学+警察学院_12019.11.1/ImageData/*/*.jpg"


def rename(root):
    imgList = glob.glob(root)
    # print(imgList)
    print(len(imgList))
    for img in imgList:
        print(img)
        imgnameList = img.split("/")
        # print(imgnameList)
        pathlist = imgnameList[0:8]
        # print(pathlist)
        path = "/".join(pathlist)
        # print("path :", path)
        imgname = imgnameList[-1].strip()
        # print(imgname)
        imgpath = os.path.join(path, imgname)
        print(imgpath)
        os.rename(img, imgpath)



if __name__ == "__main__":
    rename(rootpath)