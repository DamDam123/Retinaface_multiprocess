import os
import glob


path = r"/home/lihongxia/projects/Retinaface-master/data_set/侧脸生成正脸/crop_Images/+15/*.jpg"

imglist = glob.glob(path)
imglist.sort()
print(len(imglist))

imgname = []
img_number = []
for name in imglist:
    name = name.split("/")[-1] #图片名称
    print(name)
    imgname.append(name)
    namelist = name.split("_")
    number = namelist[0]
    if number not in img_number:
        img_number .append(number)

print(imgname)
print(img_number)






