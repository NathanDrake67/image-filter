# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 20:38:22 2022
Microsoft Windows10 家庭中文版
版本20H2(操作系统内部版本19042.1586)
处理器 lntel(R) Core(TM) i5-8300H CPU @ 2.30GHz2.30 GHz
机带RAM 8.00 GB (7.80 GB可用)
GPU0 lntel(R) UHD Graphics 630
GPU1 NVIDIA GeForce GTX 1050 Ti

@author: 10554
"""
import cv2
import numpy
import os
import glob

def gaussian(x,sigma):        #灰度距离（像素差异权值）计算，x为中心点和目标点的像素差值
                              #但此处的gaussian()函数并不是完整的计算灰度距离的函数，只是方便调用求解，且一个函数在求解空间距离也有作用（模型套用）
    return (1.0/(2*numpy.pi*(sigma**2)))*numpy.exp(-(x**2)/(2*(sigma**2)))

def distance(x1,y1,x2,y2):    #空间距离的权值计算，此权值只与空间中两点的距离有关
    return numpy.sqrt(numpy.abs((x1-x2)**2-(y1-y2)**2))

def bilateral_filter(image, diameter, sigma_i, sigma_s):  #四个参数分别为原图像，核数（滤波器长度），颜色空间过滤器的sigma值，坐标空间滤波器的sigma值。
    new_image = numpy.zeros(image.shape)          #创立新的空矩阵，用来填充处理好的像素
    for row in range(len(image)):                 #通过循环遍历图片中每一个像素
        for col in range(len(image[0])):
            wp_total = 0
            filtered_image = 0
            for k in range(diameter):
                for l in range(diameter):         #此时，中心点为(row,col)
                    n_x =row - (diameter/2 - k)   #选取目标点的x坐标值
                    n_y =col - (diameter/2 - l)   #选取目标点的y坐标值
                    if n_x >= len(image):
                        n_x -= len(image)         #将超出范围的值根据图片长度（len(image))取补
                    if n_y >= len(image[0]):
                        n_y -= len(image[0])
                    gi = gaussian(image[int(n_x)][int(n_y)] - int(image[row][col]), sigma_i) #计算gi即为像素差异权重表达式
                    gs = gaussian(distance(n_x, n_y, row, col), sigma_s)                #计算gs即为空间距离差异权重表达式
                    wp = gi * gs               #这就是双边滤波器的权重表达式，相当于一个高斯滤波器与一个颜色权重滤波器的乘积
                    filtered_image = (filtered_image) + (image[int(n_x)][int(n_y)] * wp) #对这一中心点进行滤波
                    wp_total = wp_total + wp                         #得到总的双边滤波权重
            filtered_image = filtered_image // wp_total              #进行滤波处理
            new_image[row][col] = int(numpy.round(filtered_image))   #将像素转为int类型
    return new_image


# 读取图片
Image_glob = os.path.join(r'images/',"*.png")         #读取指定文件夹中的所有.png文件
Image_name_list=[]                                    #创建空列表Image_name_list
Image_name_list.extend(glob.glob(Image_glob))         #并将其名称添加到列表Image_name_list
for i in range(3):                                    #设置一个循环，目的是循环读取并滤波处理所有三种图片
    img = cv2.imread(Image_name_list[i])              #读取用来读取图片，返回一个numpy.ndarray类型的多维数组
    source = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)     #将图像处理成灰度图

    # REPLICATE：通过复制边缘像素补全 ，选定图片上下左右各需要复制边缘像素的宽度范围，这里为滤波器长度的一半，即为3
    source = cv2.copyMakeBorder(source, 3, 3, 3, 3, cv2.BORDER_REPLICATE)
    result = bilateral_filter(source, 7, 20.0, 20.0)  #调用自定义的双边滤波函数bilateral_filter，核数为7，sigma_i,sigma_s取较优值20
    # 显示图像(但此处显示需要时间过长，且容易卡死，故补为注释)
    #cv2.imshow("source img", img)
    #cv2.imshow("BilateralBlur img(7*7)", result)
    #这里设置了判断语句，以分别对三种不同的原图进行分别保存，根据每种图片的噪声类型，分别命名
    if i == 0:
        cv2.imwrite(os.path.join(r"output_2/","7x7_Bilateral_gaussian.png"),result)
    if i == 1:
        cv2.imwrite(os.path.join(r"output_2/","7x7_Bilateral_origin.png"),result)
    else:
        cv2.imwrite(os.path.join(r"output_2/","7x7_Bilateral_pepper.png"),result)
    
    # 等待显示
    cv2.waitKey(0)
    cv2.destroyAllWindows()



"""
The bilateral filter is controlled by important parameters. Two of them are sigma values.
Generally, the bilateral filter gives us more control over image.
If we increment both sigma values at the same time, the bigger sigma values gives us a
more blurred image. If we give sigma values near zero, smoothing does not occur. Changing sigma i
directly affects the blur effect on the image. However, sigma s does not affect blur rate. There
is no big effect on the image after changing only the sigma s. Sharpness does not necessary that
much with sigma s rather than sigma i. To have a more blurred image, we should take sigma values
bigger.
"""
'''
img = cv2.imread(r'images/gaussian_noise.png')
image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
image = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_REPLICATE)'''