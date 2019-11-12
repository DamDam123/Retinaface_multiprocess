import os
import glob


srcroot = r"/home/lihongxia/projects/Retinaface-master/data_set/侧脸生成正脸/ImageData/+90/*.jpg"
dstroot = r"/home/lihongxia/projects/Retinaface-master/data_set/侧脸生成正脸/crop_Images/+90/*.jpg"


srclist = glob.glob(srcroot)
dstlist = glob.glob(dstroot)

print(len(srclist))
print(len(dstlist))


srcnamelist = []
dstnamelist = []

for src in srclist:
    srcimgname = src.split("/")[9]
    print(srcimgname)
    srcnamelist.append(srcimgname)

for dst in dstlist:
    dstimgname = dst.split("/")[9]
    print(dstimgname)
    dstnamelist.append(dstimgname)

imgname = [x for x in srcnamelist if x not in dstnamelist]
imgname.sort()
print(imgname)
print(len(imgname))








