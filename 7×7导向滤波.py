# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 11:31:53 2022
Microsoft Windows10 家庭中文版
版本20H2(操作系统内部版本19042.1586)
处理器 lntel(R) Core(TM) i5-8300H CPU @ 2.30GHz2.30 GHz
机带RAM 8.00 GB (7.80 GB可用)
GPU0 lntel(R) UHD Graphics 630
GPU1 NVIDIA GeForce GTX 1050 Ti

@author: 10554
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import glob
def guideFilter(I, p, winSize, eps):  #I为输入图片，p为导向图片，winSize即处理窗口大小，可等效认为是核数，eps为正则化参数

    mean_I = cv2.blur(I, winSize)      # I的均值平滑
    mean_p = cv2.blur(p, winSize)      # p的均值平滑

    mean_II = cv2.blur(I * I, winSize) # I*I的均值平滑
    mean_Ip = cv2.blur(I * p, winSize) # I*p的均值平滑

    var_I = mean_II - mean_I * mean_I  # 求方差var_I
    cov_Ip = mean_Ip - mean_I * mean_p # 求协方差cov_Ip

    a = cov_Ip / (var_I + eps)         # 相关因子a
    b = mean_p - a * mean_I            # 相关因子b

    mean_a = cv2.blur(a, winSize)      # 对a进行均值平滑
    mean_b = cv2.blur(b, winSize)      # 对b进行均值平滑

    q = mean_a * I + mean_b            #得到滤波结果(形如q=mean a* I + mean b的滤波形式)
    return q


if __name__ == '__main__':
    eps = 0.01
    winSize = (7,7)
    # 读取图片
    Image_glob = os.path.join(r'images/',"*.png") #读取指定文件夹中的所有.png文件
    Image_name_list=[]                            #并将其名称添加到列表Image_name_list
    Image_name_list.extend(glob.glob(Image_glob))
    for i in range(3):                           #设置一个循环，目的是循环读取并滤波处理所有三种图片
        img = cv2.imread(Image_name_list[i])     #读取用来读取图片，返回一个numpy.ndarray类型的多维数组
        image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #将图像处理成灰度图

    # REPLICATE：通过复制边缘像素补全 ，选定图片上下左右各需要复制边缘像素的宽度范围，这里暂定为5
        source = cv2.copyMakeBorder(image, 3, 3, 3, 3, cv2.BORDER_REPLICATE)
        
        image = cv2.resize(source, None,fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
        
        I = image/255.0        #将图像归一化
        p =I
    #调用定义好的导向滤波函数
        guideFilter_img = guideFilter(I, p, winSize, eps)
        guideFilter_img  = guideFilter_img  * 255
    #将超出范围的像素值定义在0~255区间
        guideFilter_img [guideFilter_img  > 255] = 255
        guideFilter_img  = np.round(guideFilter_img )
    #将图像处理成便于显示和保存的uint8类型
        result  = guideFilter_img.astype(np.uint8)
   
    # 显示图像
        cv2.imshow("source img", img)
        cv2.imshow("GuideBlur img(7*7)", result)
     #这里设置了判断语句，以分别对三种不同的原图进行分别保存
        if i == 0:
            cv2.imwrite(os.path.join(r"output_2/","7x7_Guide_gaussian.png"),result)
        if i == 1:
            cv2.imwrite(os.path.join(r"output_2/","7x7_Guide_origin.png"),result)
        else:
            cv2.imwrite(os.path.join(r"output_2/","7x7_Guide_pepper.png"),result)
    
    # 等待显示
        cv2.waitKey(0)
        cv2.destroyAllWindows()
                           
    
    
    

