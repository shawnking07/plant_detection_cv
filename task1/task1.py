from cv2 import cv2
import numpy as np
import os


# base_path = './Plant_Phenotyping_Datasets'
base_path = './dataset'
output_path='./task1_out'

## Read
path1 = '/Tray/Ara2012/'
path2 = '/Tray/Ara2013-Canon/'
path3 = '/Tray/Ara2013-RPi/'

###########################################
## change work path here !!!

# work_path = os.getcwd()#get working path

## change work path here !!!
###########################################


# three folders, use to store the output
fold_name1 = 'Ara12_Results'
fold_name2 = 'Ara13_Results'
fold_name3 = 'AraRPI_Results'



def rect_in(pos):# delete small rectangles which all include in big rectangles
    # x,y,w,h
    del_list = []
    for i in pos:
        for j in pos:
            if i[0] > j[0]:
                if i[1] > j[1]:
                    if i[0] + i[2] < j[0] + j[2]:
                        if i[1] + i[3] < j[1] + j[3]:
                            del_list.append(i)
    for i in del_list:
        pos.remove(i)
    return pos

    




def operator(img,out,name,mode):
    ## convert to hsv
    list_p = []
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv,(40,70,20),(80,255,255))
    if mode == 1:
        mask = cv2.inRange(hsv,(30,70,80),(80,255,255))
    if mode == 2:
        # mask = cv2.inRange(hsv,(20,100,60),(80,255,180))
        mask = cv2.inRange(hsv,(20,70,55),(80,255,255))
    if mode == 3:
        mask = cv2.inRange(hsv,(25,60,80),(80,255,255))
        # mask = cv2.inRange(hsv,(100,0,145),(255,140,255))
    # mask = cv2.inRange(hsv,(40,60,80),(80,255,255))
    
    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]
    
    gray = cv2.cvtColor(green,cv2.COLOR_BGR2GRAY)
    mean = np.mean(gray)
    tmp,gray = cv2.threshold(gray, mean, 255, cv2.THRESH_BINARY)
    if mode == (1 and 2):     
        gray = cv2.medianBlur(gray,3)
        gray = cv2.medianBlur(gray,5)
    else:
        gray = cv2.medianBlur(gray,5)
        gray = cv2.blur(gray,(5,5))

    contours, hier = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print(contours)
    ori = np.copy(img)
    count = 0
    area_list = []
    position = []
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if (w < 4*h and h< 4*w):
            area_list.append(w*h)
    if len(area_list) > 30:
            area_list.sort(reverse = True)
            area_list = area_list[0:29]       
            
    mean_area =int( np.mean(area_list) -1)
    if mode == 1:
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if w*h > mean_area/2 :
                if (w < 3*h and h < 3*w):
                    position.append([x,y,w,h])
                    cv2.rectangle(ori, pt1=(x, y), pt2=(x + w, y + h),color=(255, 255, 255), thickness=3)
                    count = count + 1
    if mode == 2:
        b_list = []
        b,_,_ = cv2.split(img)
        blue_mean = np.mean(b)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if w*h > mean_area/25:
                if (w < 4*h and h < 4*w):
                    tmp_img = img[y:y+h,x:x+w]
                    b,_,_ = cv2.split(tmp_img)
                    b_list.append(np.mean(b))
        standard = 2*np.mean(b_list) - min(b_list) 
        # print(standard,blue_mean)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if w*h > mean_area/25:
                if (w < 4*h and h < 4*w):
                    tmp_img = img[y:y+h,x:x+w]
                    b,_,_ = cv2.split(tmp_img)
                    # if np.mean(b) < blue_mean:
                    if np.mean(b) < (blue_mean + standard)/2 :
                        tmp = [x,y,w,h]
                        position.append(tmp)
        position = rect_in(position)
        for i in position:
            cv2.rectangle(ori,pt1 = (i[0],i[1]),pt2 = (i[0]+i[2],i[1]+i[3]),color=(255,255,255),thickness=3)
            count = count + 1
    if mode == 3:
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if w*h > 200:
                if (w < 4*h and h < 4*w):
                    tmp = [x,y,w,h]
                    position.append(tmp)
        position = rect_in(position)
        for i in position:
            cv2.rectangle(ori,pt1 = (i[0],i[1]),pt2 = (i[0]+i[2],i[1]+i[3]),color=(255,255,255),thickness=3)
            count = count + 1
    
    csv = []
    for i in position:
        x = i[0]
        y = i[1]
        w = i[2]
        h = i[3]
        csv.append([x,y, x,y+h, x+w,y+h, x+w,y])
    csv = sorted(csv,key = (lambda x:x[0]))
    
    if mode == 1:
        if count > 19:
            precision = 19/count
        else:
            precision = count/19
        
    if mode == 2:
        precision = 24/count
    if mode == 3:
        precision = 24/count
    ## save 
    # work_path = os.getcwd() + task + '/' + fold_name
    # tmp = name.split('_')[1]
    tmp = str(mode)
    np.savetxt(out + '/' + name + '_.csv', csv, delimiter=",",fmt = '%d')
    cv2.imwrite(out + '/' + name + '_rect.png', ori)
    cv2.imwrite(out + '/' + name + '_green.png', green)
    # cv2.imwrite(work_path + '\\' + tmp + '_gray.png',gray)
    return count,precision 

# create four folders    

# Area_Ara12 = []
# Area_Ara13 = []
# Area_RPI = []
# precision_12 = []
# precision_13 = []
# precision_RPI = []

# read images from three folders
# for i in list_Ara12:
#     img = cv2.imread(work_path+path1+i)
#     result,precision = operator(img,i,fold_name1,task,1)
#     Area_Ara12.append(result)
#     precision_12.append(precision)
# print('Average precision of Ara2012 is {}'.format(round(np.mean(precision_12),3)))

# for i in list_Ara13:
#     img = cv2.imread(work_path+path2+i)
#     result,precision = operator(img,i,fold_name2,task,2)
#     Area_Ara13.append(result)
#     precision_13.append(precision)
# print('Average precision of Canon is {}'.format(round( np.mean(precision_13),3 )))

# for i in list_RPI:
#     img = cv2.imread(work_path+path3+i)
#     result,precision = operator(img,i,fold_name3,task,3)
#     Area_RPI.append(result)
#     precision_RPI.append(precision)
# print('Average precision of RPi is {}'.format(round(np.mean(precision_RPI),3)))
# print numbers of plants found in the three datasets
# print('number of plants found in Ara2012:')
# print(Area_Ara12)
# print('number of plants found in Canon:')
# print(Area_Ara13)
# print('number of plants found in RPi:')
# print(Area_RPI)

if __name__=='__main__':
    path1 = base_path + path1
    path2 = base_path + path2
    path3 = base_path + path3
    file_2012 = '/ara2012_tray07_rgb.png'
    file_canon = '/ara2013_tray07_rgb.png'
    file_RPi = '/ara2013_tray07_rgb.png'
    img1 = cv2.imread(path1 + file_2012)
    img2 = cv2.imread(path2 + file_canon)
    img3 = cv2.imread(path3 + file_RPi)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    count,_ = operator(img1,output_path,'2012',1)
    print('{} plants are found'.format(count))
    count,_ = operator(img2,output_path,'Canon',2)
    print('{} plants are found'.format(count))
    count,_ = operator(img3,output_path,'RPi',3)
    print('{} plants are found'.format(count))


