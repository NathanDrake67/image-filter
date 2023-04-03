# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 11:37:38 2022
Microsoft Windows10 家庭中文版
版本20H2(操作系统内部版本19042.1586)
处理器 lntel(R) Core(TM) i5-8300H CPU @ 2.30GHz2.30 GHz
机带RAM 8.00 GB (7.80 GB可用)
GPU0 lntel(R) UHD Graphics 630
GPU1 NVIDIA GeForce GTX 1050 Ti

@author: 10554
"""
import cv2
import numpy as np
import os
import glob
# 读取图片
Image_glob = os.path.join(r'images/',"*.png")     #读取指定文件夹中的所有.png文件
Image_name_list=[]                                #创建空列表Image_name_list
Image_name_list.extend(glob.glob(Image_glob))     #并将其名称添加到列表Image_name_list
#print(Image_name_list[::])                       #可检验一下读取的图片名称及数量
#print(len(Image_name_list))

for i in range(3):                                #设置一个循环，目的是循环读取并滤波处理所有三种图片
    img = cv2.imread(Image_name_list[i])          #读取用来读取图片，返回一个numpy.ndarray类型的多维数组
    source = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #将图像处理成灰度图

    # REPLICATE：通过复制边缘像素补全 ，选定图片上下左右各需要复制边缘像素的宽度范围，这里为滤波器(3*3)长度的一半，即为1
    source = cv2.copyMakeBorder(source, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
    #sobel_x:发现垂直边缘
    '''
         source 代表原始图像。
         cv2.CV_64F代表输出图像的深度ddepth 。
         dx 代表 x 方向上的求导阶数。此处取1
         dy 代表 y 方向上的求导阶数。此处取0，即是在x方向上进行Sobel滤波，同理，下面的语句是在y方向进行滤波
         ksize 代表 Sobel 核的大小。该值为-1 时，则会使用 Scharr 算子进行运算。
'''
    sobel_x =cv2.Sobel(source,cv2.CV_64F,1,0,None,3)#设置核数为3×3
      #sobel_y:发现水平边缘
    sobel_y = cv2.Sobel(source,cv2.CV_64F,0,1,None,3)
    sobel_x = np.uint8(np.absolute(sobel_x))   #将sobel_x像素矩阵取绝对值后转换为uint8类型，方便后续显示
    sobel_y = np.uint8(np.absolute(sobel_y))   #将sobel_y像素矩阵取绝对值后转换为uint8类型，方便后续显示
    np.set_printoptions(threshold=np.inf)       #打印完整的numpy数组a而不截断
    
    if i == 0: #这里设置了判断语句，以分别对三种不同的原图进行分别保存,根据每种图片的噪声类型及滤波处理的方向(x或y)，分别命名存储
        cv2.imwrite(os.path.join(r"output_1/","3x3_Sobel_x_gaussian.png"),sobel_x)
        cv2.imwrite(os.path.join(r"output_1/","3x3_Sobel_y_gaussian.png"),sobel_y)
        # 显示图像,下面同理
        cv2.imshow('gaussian_sobel_x',sobel_x)
        cv2.imshow('gaussian_sobel_y',sobel_y)
    if i == 1:
        cv2.imwrite(os.path.join(r"output_1/","3x3_Sobel_x_origin.png"),sobel_x)
        cv2.imwrite(os.path.join(r"output_1/","3x3_Sobel_y_origin.png"),sobel_y)
        cv2.imshow('origin_sobel_x',sobel_x)
        cv2.imshow('origin_sobel_y',sobel_y)
    if i == 2:
        cv2.imwrite(os.path.join(r"output_1/","3x3_Sobel_x_pepper.png"),sobel_x)
        cv2.imwrite(os.path.join(r"output_1/","3x3_Sobel_y_pepper.png"),sobel_y)
        cv2.imshow('pepper_sobel_x',sobel_x)
        cv2.imshow('pepper_sobel_y',sobel_y)
    
    # 等待显示
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    
    

  
    
    
          
     
    
   