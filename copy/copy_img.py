"""
复制图片到指定文件
"""
import os
import glob
import shutil
import sys

src_path = r"/home/lihongxia/face_data/2019_11_11/crop_result"
dst_path = r"/home/lihongxia/face_data/all/crop_result"

# src_path = sys.argv[1]
# dst_path = sys.argv[2]

def copy(src_path, dst_path):
    src_path = os.path.join(src_path, "*")
    print(src_path)
    angle_dir = glob.glob(src_path)
    angle_dir.sort()
    print(angle_dir)
    for dir in angle_dir:

        angle = dir.split("/")[-1]
        print(angle)
        src_img_path = os.path.join(dir, "*.jpg")
        src_img = glob.glob(src_img_path)
        src_img.sort()
        dst_angle_path = os.path.join(dst_path, angle)
        if not os.path.isdir(dst_angle_path):
            os.makedirs(dst_angle_path)
        for img in src_img:
            img_name = img.split("/")[-1]
            dst_img = os.path.join(dst_angle_path, img_name)
            print("源路径：", img)
            print("目标路径：", dst_img)
            shutil.copy(img, dst_img)  # 复制图片

    print("end")


if __name__ == "__main__":
    copy(src_path, dst_path)
