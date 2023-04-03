# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 15:03:59 2022
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
import matplotlib.pyplot as plt
import os
import glob

def Derivative_FILTER(image,K_size =3):
    #由下文自定义滤波器已定义好默认的核为3
    kx = np.array([
        [0,0,0],
        [1,0,-1],
        [0,0,0]])
    #x方向的卷积矩阵,即由 1D Derivative_Filter[1,0,-1]补零所得
    ky = np.array([
        [0,1,0],
        [0,0,0],
        [0,-1,0]])
    #x方向的卷积矩阵，即由 1D Derivative_Filter[1,0,-1]T补零所得
    global output_x                           #此处及下处将output_x,output_y命名为全局变量，目的是方便后续图片的命名及保存
    output_x=cv2.filter2D(image,-1,kx)        #采用cv2.filter2D()函数进行原图与所定义滤波器的卷积
    global output_y
    output_y=cv2.filter2D(image,-1,ky)        #-1 表示输出类型和输入相同,核数默认为3


output_x =0;output_y=0                        #初始化output_x,output_y
Image_glob = os.path.join(r'images/',"*.png") #读取指定文件夹中的所有.png文件
Image_name_list=[]                            #并将其名称添加到列表Image_name_list
Image_name_list.extend(glob.glob(Image_glob))


for i in range(3):                           #设置一个循环，目的是循环读取并滤波处理所有三种图片
    img = cv2.imread(Image_name_list[i])     #读取用来读取图片，返回一个numpy.ndarray类型的多维数组
    source = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #将图像处理成灰度图
    # REPLICATE：通过复制边缘像素补全 ，选定图片上下左右各需要复制边缘像素的宽度范围，这里暂定为5
    image = cv2.copyMakeBorder(source, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
    # 调用定义好的导数滤波函数
    Derivative_FILTER(image, K_size=3)


     #这里设置了判断语句，以分别对三种不同的原图进行分别保存
    if i == 0:
        cv2.imwrite(os.path.join(r"output_1/","3x3_Derivative_x_gaussian.png"),output_x)
        cv2.imwrite(os.path.join(r"output_1/","3x3_Derivative_y_gaussian.png"),output_y)
        cv2.imshow('gaussian_derivative_x Image',output_x)
        cv2.imshow('gaussian_derivative_y Image',output_y)
    if i == 1:
        cv2.imwrite(os.path.join(r"output_1/","3x3_Derivative_x_origin.png"),output_x)
        cv2.imwrite(os.path.join(r"output_1/","3x3_Derivative_y_origin.png"),output_y)
        cv2.imshow('origin_derivative_x Image',output_x)
        cv2.imshow('origin_derivative_y Image',output_y)
    if i == 2:
        cv2.imwrite(os.path.join(r"output_1/","3x3_Derivative_x_pepper.png"),output_x)
        cv2.imwrite(os.path.join(r"output_1/","3x3_Derivative_y_pepper.png"),output_y)
        cv2.imshow('pepper_derivative_x Image',output_x)
        cv2.imshow('pepper_derivative_y Image',output_y)
    
    # 等待显示
    cv2.waitKey(0)
    cv2.destroyAllWindows()