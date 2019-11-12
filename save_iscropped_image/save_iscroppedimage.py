import os
import glob


iscropped_rootPath = r"/home/lihongxia/projects/Retinaface-master/data_set/侧脸生成正脸/crop_Images/*/*.jpg"
save_iscropped_path = r"/home/lihongxia/projects/Retinaface-master/exist_croppedImgTxt"

imgpathList = glob.glob(iscropped_rootPath)
imgpathList.sort()
print(len(imgpathList))

#创建已裁剪图片文件夹
if not os.path.exists(save_iscropped_path):
    os.makedirs(save_iscropped_path)

save_iscropped_txt = os.path.join(save_iscropped_path, "iscropped.txt")
fo = open(save_iscropped_txt, "w")
# fo.write("已裁剪图像：")
# fo.write("\n")
for img in imgpathList:
    imglist = img.split("/")
    print(imglist)
    iscropImg_angle_name = imglist[-2] + "_" + imglist[-1]
    # print(iscropImg_angle_name)
    fo.write(iscropImg_angle_name)
    fo.write("\n")

print("end")
fo.close()

