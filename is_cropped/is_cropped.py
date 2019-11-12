"""
将
"""

import os
import glob


cropped_Imgpath = r"../data_set/侧脸生成正脸/crop_Images/+15"

# cropped_img = glob.glob(cropped_Imgpath)
# cropped_img.sort()
# print(cropped_img)
exist_croppedImgTxt = r"../exist_croppedImgTxt"
if not os.path.exists(exist_croppedImgTxt):
    os.makedirs(exist_croppedImgTxt)

exist_croppedImgTxt = os.path.join(exist_croppedImgTxt, 'exist_croppedImg.txt')
f = open(exist_croppedImgTxt, 'w')
# print(f)
imgname_textList = []
for root, dir, file in os.walk(cropped_Imgpath):
    # print(file)
    imgname_textList = file

imgname_textList.sort()
for img in imgname_textList:
    print(img)
    f.write(str(img))
    f.write("\n")
f.close()
print("end")