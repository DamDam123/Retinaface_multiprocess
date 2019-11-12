import multiprocessing as mp
import glob
import os
import time
import sys
from crop import crop

ori_img_path = sys.argv[1]

if __name__ == "__main__":
    day = time.strftime("%Y_%m_%d", time.localtime())
    # ori_img_path = r"/home/lihongxia/face_data/2019_11_05/ImageData/*"
    ori_img_path = os.path.join(ori_img_path, "*")
    # ori_data = ori_img_path.split("/")[-3]
    dst_img_path = r"/home/lihongxia/face_data/all"
    # dst_img_path = os.path.join(dst_img_path, ori_data)
    angle = glob.glob(ori_img_path)
    angle.sort()
    p0_1 = mp.Process(target=crop, args=(dst_img_path, 1, angle[0:2]))
    p2_3 = mp.Process(target=crop, args=(dst_img_path, 2, angle[2:4]))
    p4_5 = mp.Process(target=crop, args=(dst_img_path, 3, angle[4:6]))
    p6_7 = mp.Process(target=crop, args=(dst_img_path, 4, angle[6:8]))
    p8_9 = mp.Process(target=crop, args=(dst_img_path, 5, angle[8:10]))
    p10_11 = mp.Process(target=crop, args=(dst_img_path, 6, angle[10:12]))
    p12_13 = mp.Process(target=crop, args=(dst_img_path, 7, angle[12:14]))
    p14_15 = mp.Process(target=crop, args=(dst_img_path, 8, angle[14:16]))
    p16_17 = mp.Process(target=crop, args=(dst_img_path, 9, angle[16:18]))
    p18_19 = mp.Process(target=crop, args=(dst_img_path, 10, angle[18:20]))
    p20_23 = mp.Process(target=crop, args=(dst_img_path, 11, angle[20:]))
    p0_1.start()
    p2_3.start()
    p4_5.start()
    p6_7.start()
    p8_9.start()
    p10_11.start()
    p12_13.start()
    p14_15.start()
    p16_17.start()
    p18_19.start()
    p20_23.start()

    p0_1.join()
    p2_3.join()
    p4_5.join()
    p6_7.join()
    p8_9.join()
    p10_11.join()
    p12_13.join()
    p14_15.join()
    p16_17.join()
    p18_19.join()
    p20_23.join()

    # p0_1 = mp.Process(target=crop, args=(dst_img_path, 1, angle[0:12]))
    # p2_3 = mp.Process(target=crop, args=(dst_img_path, 2, angle[12:]))
    # # p4_5 = mp.Process(target=crop, args=(dst_img_path, 3, angle[16:21]))
    # # # p6_7 = mp.Process(target=crop, args=(dst_img_path, 4, angle[16:21]))
    # # p8_9 = mp.Process(target=crop, args=(dst_img_path, 5, angle[21:]))
    #
    # p0_1.start()
    # p2_3.start()
    # # p4_5.start()
    # # # p6_7.start()
    # # p8_9.start()
    #
    # p0_1.join()
    # p2_3.join()
    # # p4_5.join()
    # # # p6_7.join()
    # # p8_9.join()

    print("end")
