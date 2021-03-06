from sklearn.model_selection import train_test_split
import os
import numpy as np
import cv2
from scipy.cluster.vq import *
from sklearn.svm import LinearSVC
from sklearn import metrics
from collections import defaultdict
base_path = './dataset'

os.mkdir('task2_out')

if __name__=='__main__':
    path1=base_path + '/Tray/Ara2012'
    path2=base_path + '/Tray/Ara2013-Canon'
    file2012='/ara2012_tray07_rgb.png'
    target2012='/ara2012_tray07_fg.png'
    file2013='/ara2013_tray07_rgb.png'
    target2013='/ara2013_tray07_fg.png'
    sample_img=cv2.imread(path2+file2013)
    sample_target=cv2.imread(path2+target2013,0)

    #cv2.imshow('1',imgs_1[1])
    #cv2.imshow('2', targets_1[1])
    #cv2.waitKey(0)

    lower_green = np.array([36, 43, 106])
    upper_green = np.array([77, 255, 255])
    hsv = cv2.cvtColor(sample_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lowerb=lower_green,upperb=upper_green)
    #des=cv2.fastNlMeansDenoising(mask,None,10,10,7,21
    mask_name = './task2_out/mask.png'
    cv2.imwrite(mask_name, mask)
    median = cv2.medianBlur(mask, 5)
    median_name ='./task2_out/median.png'
    cv2.imwrite(median_name,median)


    # q = defaultdict(int)
    # for x in range(sample_target.shape[0]):
    #     for y in range(sample_target.shape[1]):
    #         if sample_target[x][y] == 0 and median[x][y] == 0:
    #             q['tn'] += 1
    #         if sample_target[x][y] == 255 and median[x][y] == 0:
    #             q['fn'] += 1
    #         if sample_target[x][y] == 0 and median[x][y] == 255:
    #             q['fp'] += 1
    #         if sample_target[x][y] == 255 and median[x][y] == 255:
    #             q['tp'] += 1

    # dice = (2 * q['tp']) / (q['fn'] + q['fp'] + 2 * q['tp'])
    # iou = q['tp'] / ( q['fp'] + q['tp'] + q['fn'])
    # print('dice:',dice)
    # print('IOU:',iou)



