# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 22:06:16 2022
Microsoft Windows10 家庭中文版
版本20H2(操作系统内部版本19042.1586)
处理器 lntel(R) Core(TM) i5-8300H CPU @ 2.30GHz2.30 GHz
机带RAM 8.00 GB (7.80 GB可用)
GPU0 lntel(R) UHD Graphics 630
GPU1 NVIDIA GeForce GTX 1050 Ti

@author: 10554
"""
# encoding:utf-8
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
# 读取图片
Image_glob = os.path.join(r'images/',"*.png")              #读取指定文件夹中的所有.png文件
Image_name_list=[]                                         #创建空列表Image_name_list
Image_name_list.extend(glob.glob(Image_glob))              #并将其名称添加到列表Image_name_list

for i in range(3):                                         #设置一个循环，目的是循环读取并滤波处理所有三种图片
    img = cv2.imread(Image_name_list[i])                   #读取用来读取图片，返回一个numpy.ndarray类型的多维数组
    source = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)          #将图像处理成灰度图

    # REPLICATE：通过复制边缘像素补全 ，选定图片上下左右各需要复制边缘像素的宽度范围，这里为滤波器长度的一半，即为1
    REPLICATE = cv2.copyMakeBorder(source, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
    # 中值滤波
    result = cv2.medianBlur(REPLICATE, 3)                  #3即为核的大小，在中值滤波中默认为3
    # 显示图像
    cv2.imshow("source img", img)                          #显示原始图像
    cv2.imshow("medianBlur img(3*3)", result)              #显示中值滤波处理后的图像
     #这里设置了判断语句，以分别对三种不同的原图进行分别保存
    if i == 0:
        cv2.imwrite(os.path.join(r"output_1/","3x3_Median_gaussian.png"),result)
    if i == 1:
        cv2.imwrite(os.path.join(r"output_1/","3x3_Median_origin.png"),result)
    else:
        cv2.imwrite(os.path.join(r"output_1/","3x3_Median_pepper.png"),result)
    
    # 等待显示
    cv2.waitKey(0)
    cv2.destroyAllWindows()




 




