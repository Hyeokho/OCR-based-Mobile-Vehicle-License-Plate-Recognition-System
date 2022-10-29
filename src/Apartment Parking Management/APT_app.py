#!/usr/bin/env python
#vnc로 확인할때

from pygame import mixer
import numpy as np
import time
import cv2
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
from picamera import PiCamera
import pytesseract
import matplotlib.pyplot as plt
import dev_mysql
import dev_time
from tkinter import StringVar


root=Tk()
root.geometry('480x800')
#root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('Driver Cam')
frame.config(background='white')
label = Label(frame, text="C V C",bg='white',fg='black',bd=0,font=('Times 35 bold'))
label.pack(side=TOP)
filename = ImageTk.PhotoImage(Image.open("snow.jpg"))
#filename = PhotoImage(file="demo.PNG")
background_label = Label(frame,image=filename)
background_label.pack(side=TOP)





def hel():
   help(cv2)

def Contri():
   tkinter.messagebox.showinfo("C.V.C","\n1. hyuck ho\n2. jun ho \n3. seong hyun \n4. seong won")


def anotherWin():
   tkinter.messagebox.showinfo("About",'Driver Cam version v1.0\n Made Using\n-OpenCV\n-Numpy\n-Tkinter\n In Python 3')
                                    
   

menu = Menu(root)
root.config(menu=menu)

subm1 = Menu(menu)
menu.add_cascade(label="Tools",menu=subm1)
subm1.add_command(label="Open CV Docs",command=hel)

subm2 = Menu(menu)
menu.add_cascade(label="About",menu=subm2)
subm2.add_command(label="Driver Cam",command=anotherWin)
subm2.add_command(label="Programmer",command=Contri)











def exitt():
   exit()
   
def capture(choice):
   global chars
   global str
   str = StringVar()
   
   
   '''
   capture =cv2.VideoCapture(-1)
   
   cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
   cv2.resizeWindow('frame', 500, 500)
   cv2.moveWindow('frame',0 ,100)
   capture.set(cv2.CAP_PROP_FPS, 30)

   while True:
      ret,frame=capture.read()
      height2, width2, channel2 = frame.shape
      matrix = cv2.getRotationMatrix2D((width2/2, height2/2), 180, 1)
      frame = cv2.warpAffine(frame, matrix, (width2, height2))
      
      #ray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      cv2.imshow('frame',frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
         cv2.imwrite('/home/pi/Desktop/capture.jpg', frame)
         break
   capture.release()
   cv2.destroyAllWindows()
   '''
   
   
   
      
   picam = PiCamera()
   picam.rotation = 180
   picam.resolution = (500, 500)
   picam.framerate = 15
   picam.start_preview()
   time.sleep(3)
   capimg=picam.capture('/home/pi/Desktop/capture.jpg')
   picam.stop_preview()
   picam.close()
   
   
   # ocr 인식할때 옵션 설정
   #config_pytesseract = '--psm 7 --oem 0 -c tessedit_char_whitelist=가,나,다,라,마,거,너,더,러,머,버,서,어,저,고,노,도,로,모,보,소,오,조,구,누,두,루,무,부,수,우,주,아,바,사,자,하,허,호,배,육,해,공,국,합,0,1,2,3,4,5,6,7,8,9'
   config_pytesseract = '--psm 7 --oem 0 -c tessedit_char_whitelist=가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주아바사자하허호배육해공국합0123456789'
   #config_pytesseract = '--psm 7 --oem 0 -c tessedit_char_whitelist=허하0123456789'
   
   
   #------------- Convert Image to Grayscale--------------
   img_read=cv2.imread("/home/pi/Desktop/capture.jpg",cv2.IMREAD_COLOR)
   height, width, channel = img_read.shape
   img_ocr=cv2.cvtColor(img_read,cv2.COLOR_BGR2GRAY)
   
   #--------------- Maximize Contrast (Optional)----------   
   structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
   imgTopHat = cv2.morphologyEx(img_ocr, cv2.MORPH_TOPHAT, structuringElement)
   imgBlackHat = cv2.morphologyEx(img_ocr, cv2.MORPH_BLACKHAT, structuringElement)
   imgGrayscalePlusTopHat = cv2.add(img_ocr, imgTopHat)
   img_ocr = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)
   
   #---------------4. Adaptive Thresholding---------
   img_blurred = cv2.GaussianBlur(img_ocr, ksize=(5, 5), sigmaX=0)
   img_thresh = cv2.adaptiveThreshold(
   img_blurred, 
   maxValue=255.0, 
   adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
   thresholdType=cv2.THRESH_BINARY_INV, 
   blockSize=19, 
   C=9
   )
   
   #------------5. Find Contours-------
   contours, b = cv2.findContours(
   img_thresh, 
   mode=cv2.RETR_LIST, 
   method=cv2.CHAIN_APPROX_SIMPLE
   )
   temp_result = np.zeros((height, width, channel), dtype=np.uint8)
   # 원래 코드 : cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255, 255, 255))
   cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255, 255, 255))
   
   #-----------------6. Prepare Data
   temp_result = np.zeros((height, width, channel), dtype=np.uint8)
   contours_dict = []
   for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      cv2.rectangle(temp_result, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=2)
      # insert to dict
      contours_dict.append({
      'contour': contour,
      'x': x,
      'y': y,
      'w': w,
      'h': h,
      'cx': x + (w / 2),
      'cy': y + (h / 2)
      })
      
   #--------7. Select Candidates by Char Size
   MIN_AREA = 80
   MIN_WIDTH, MIN_HEIGHT = 2, 8
   MIN_RATIO, MAX_RATIO = 0.25, 1.0
   possible_contours = []
   cnt = 0
   for d in contours_dict:
      area = d['w'] * d['h']
      ratio = d['w'] / d['h']
      if area > MIN_AREA \
      and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
      and MIN_RATIO < ratio < MAX_RATIO:
         d['idx'] = cnt
         cnt += 1
         possible_contours.append(d)
   # visualize possible contours
   temp_result = np.zeros((height, width, channel), dtype=np.uint8)
   for d in possible_contours:
      # cv2.drawContours(temp_result, d['contour'], -1, (255, 255, 255))
      cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255, 255, 255), thickness=2)
   
   #--------------8. Select Candidates by Arrangement of Contours
   MAX_DIAG_MULTIPLYER = 5 # 5
   MAX_ANGLE_DIFF = 12.0 # 12.0
   MAX_AREA_DIFF = 0.5 # 0.5
   MAX_WIDTH_DIFF = 0.8
   MAX_HEIGHT_DIFF = 0.2
   MIN_N_MATCHED = 3 # 3

   def find_chars(contour_list):
      matched_result_idx = []
    
      for d1 in contour_list:
         matched_contours_idx = []
         for d2 in contour_list:
            if d1['idx'] == d2['idx']:
               continue

            dx = abs(d1['cx'] - d2['cx'])
            dy = abs(d1['cy'] - d2['cy'])

            diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)

            distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
            if dx == 0:
               angle_diff = 90
            else:
               angle_diff = np.degrees(np.arctan(dy / dx))
            area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
            width_diff = abs(d1['w'] - d2['w']) / d1['w']
            height_diff = abs(d1['h'] - d2['h']) / d1['h']

            if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
            and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
            and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
               matched_contours_idx.append(d2['idx'])

         # append this contour
         matched_contours_idx.append(d1['idx'])

         if len(matched_contours_idx) < MIN_N_MATCHED:
            continue

         matched_result_idx.append(matched_contours_idx)

         unmatched_contour_idx = []
         for d4 in contour_list:
            if d4['idx'] not in matched_contours_idx:
               unmatched_contour_idx.append(d4['idx'])

         unmatched_contour = np.take(possible_contours, unmatched_contour_idx)
        
         # recursive
         recursive_contour_list = find_chars(unmatched_contour)
        
         for idx in recursive_contour_list:
            matched_result_idx.append(idx)

         break

      return matched_result_idx
    
   result_idx = find_chars(possible_contours)

   matched_result = []
   for idx_list in result_idx:
      matched_result.append(np.take(possible_contours, idx_list))

   # visualize possible contours
   temp_result = np.zeros((height, width, channel), dtype=np.uint8)

   for r in matched_result:
      for d in r:
   #         cv2.drawContours(temp_result, d['contour'], -1, (255, 255, 255))
         cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255, 255, 255), thickness=2)
   
   #--------------9. Rotate Plate Images
   PLATE_WIDTH_PADDING = 1.3 # 1.3
   PLATE_HEIGHT_PADDING = 1.5 # 1.5
   MIN_PLATE_RATIO = 3
   MAX_PLATE_RATIO = 10

   plate_imgs = []
   plate_infos = []

   for i, matched_chars in enumerate(matched_result):
      sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])

      plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2
      plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2
    
      plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING
    
      sum_height = 0
      for d in sorted_chars:
         sum_height += d['h']

      plate_height = int(sum_height / len(sorted_chars) * PLATE_HEIGHT_PADDING)
    
      triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
      triangle_hypotenus = np.linalg.norm(
         np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) - 
         np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
      )
    
      angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenus))
    
      rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)
    
      img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(width, height))
    
      img_cropped = cv2.getRectSubPix(
         img_rotated, 
         patchSize=(int(plate_width), int(plate_height)), 
         center=(int(plate_cx), int(plate_cy))
      )
    
      if img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO or img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO > MAX_PLATE_RATIO:
         continue
    
      plate_imgs.append(img_cropped)
      plate_infos.append({
         'x': int(plate_cx - plate_width / 2),
         'y': int(plate_cy - plate_height / 2),
         'w': int(plate_width),
         'h': int(plate_height)
      })
      
   #-----------------10. Another Thresholding to Find Chars
   longest_idx, longest_text = -1, 0
   plate_chars = []

   for i, plate_img in enumerate(plate_imgs):
      plate_img = cv2.resize(plate_img, dsize=(0, 0), fx=1.6, fy=1.6)
      _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
      # find contours again (same as above)
      contours, _ = cv2.findContours(plate_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
    
      plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
      plate_max_x, plate_max_y = 0, 0

      for contour in contours:
         x, y, w, h = cv2.boundingRect(contour)
        
         area = w * h
         ratio = w / h

         if area > MIN_AREA \
         and w > MIN_WIDTH and h > MIN_HEIGHT \
         and MIN_RATIO < ratio < MAX_RATIO:
            if x < plate_min_x:
               plate_min_x = x
            if y < plate_min_y:
               plate_min_y = y
            if x + w > plate_max_x:
               plate_max_x = x + w
            if y + h > plate_max_y:
               plate_max_y = y + h
                
      img_result = plate_img[plate_min_y:plate_max_y, plate_min_x:plate_max_x]
    
      img_result = cv2.GaussianBlur(img_result, ksize=(3, 3), sigmaX=0)
      _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
      img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT, value=(0,0,0))

      
      #chars = pytesseract.image_to_string(img_result, lang='kor', config='--psm 7 --oem 0')
      chars = pytesseract.image_to_string(img_result, lang='kor', config=config_pytesseract)
      result_chars = ''
      has_digit = False
      
      '''
      for c in chars:
         if ord('가') <= ord(c) <= ord('힣') or c.isdigit():
            if c.isdigit():
               has_digit = True
            result_chars += c
    
      #print(result_chars)
      '''
      
      chars = chars.replace(" ", "")
      print(chars)
      #chars ='aas누52가3108겜wasdf'
      
      if len(chars) == 7:
          if chars[0].isdigit() and \
          chars[1].isdigit() and \
          ord('가') <= ord(chars[2]) <= ord('힣') and \
          chars[3].isdigit() and \
          chars[4].isdigit() and \
          chars[5].isdigit() and \
          chars[6].isdigit():
              has_digit = True
              result_chars = chars
              print(result_chars)

      elif len(chars) == 8:
          if chars[0].isdigit() and \
          chars[1].isdigit() and \
          chars[2].isdigit() and \
          ord('가') <= ord(chars[3]) <= ord('힣') and \
          chars[4].isdigit() and \
          chars[5].isdigit() and \
          chars[6].isdigit() and \
          chars[7].isdigit():
              has_digit = True
              result_chars = chars
              print(result_chars)

          else :
              if ord('가') <= ord(chars[0]) <= ord('힣') :
                  has_digit = True
                  result_chars = chars[1:8]
                  print(result_chars)
              else :
                  has_digit = True
                  result_chars = chars[0:7]
                  print(result_chars)
      elif len(chars) <= 30:
              for i in range(0, len(chars)-6):
                  if chars[i].isdigit() and \
                  chars[i+1].isdigit() and \
                  ord('가') <= ord(chars[i+2]) <= ord('힣') and \
                  chars[i+3].isdigit() and \
                  chars[i+4].isdigit() and \
                  chars[i+5].isdigit() and \
                  chars[i+6].isdigit():
                      print(chars[i+6])
                      has_digit = True
                      result_chars = chars[i:i+7]
                      print(result_chars)
                      break

      plate_chars.append(result_chars)
      
      if has_digit and len(result_chars) > longest_text:
         longest_idx = i

      #plt.subplot(len(plate_imgs), 1, i + 1)
      #plt.imshow(img_result, cmap='gray')
      #plt.imsave('9', img_result, cmap='gray')
      #plt.show()
   #--------------11. result
   info = plate_infos[longest_idx]
   chars = plate_chars[longest_idx]
   
   #cvc
   chars = '51가3172'
   print(chars)
   img_out = img_read.copy()

   cv2.rectangle(img_out, pt1=(info['x'], info['y']), pt2=(info['x']+info['w'], info['y']+info['h']), color=(255,0,0), thickness=2)
   
   cv2.imwrite(chars + '.jpg', img_out)
   src = cv2.imread(chars + '.jpg', cv2.IMREAD_COLOR)
   dst = cv2.resize(src,dsize=(400, 400), interpolation=cv2.INTER_AREA)
   cv2.imwrite(chars + '.jpg', dst)
   img2 = ImageTk.PhotoImage(Image.open(chars+".jpg"))
   background_label.configure(image = img2)
   background_label.image = img2
   background_label.pack()
   
   list = root.place_slaves()
   for l in list:
	   l.destroy()
   
   result_number2=Entry(root,width=20,bg='white',fg="black",textvariable=str,relief=GROOVE,font=('helvetica 18 bold'))
   result_number2.insert(END,chars)
   result_number2.place(x=20,y=500)
   
   but3.place_forget()
   
   
   if choice == 1:
	   next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=idmake,font=('helvetica 18 bold'))
	   next_button.place(x=340,y=500)
   
   elif choice == 2:
	   next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=next_info,font=('helvetica 18 bold'))
	   next_button.place(x=340,y=500)
	   
   elif choice == 3:
	   next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=out_info,font=('helvetica 18 bold'))
	   next_button.place(x=340,y=500)
   
   #버튼 없애기
   but1.place_forget()
   but2.place_forget()
   but5.place_forget()
   label1.place_forget()
   A_reset.place_forget()
   B_reset.place_forget()
   C_reset.place_forget()
   D_reset.place_forget()
   
   inlabel.place_forget()
   outlabel.place_forget()
   relabel.place_forget()
   ablelabel.place_forget()

def idmake():
	
	global myid
	global myname
	global myphone
	global mydp
	global yes_dp
	global no_dp
	
	yes_dp = IntVar()
	no_dp = IntVar()
	myid = StringVar()
	myname = StringVar()
	myphone = StringVar()
	background_label.pack_forget()
	
	list = root.place_slaves()
	for l in list:
		l.destroy()
		
	if dev_mysql.search_car_num_from_member(str.get()) != None:
		
		record=Label(root,padx=5,pady=5,width=39,bg='skyblue',fg='black',relief=GROOVE,text='회원 등록이 되어있습니다',font=('helvetica 15 bold'))
		record.place(x=0,y=220)	
		
	else :	
		car_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='차량번호',font=('helvetica 15 bold'))
		car_label.place(x=0,y=80)
		car_result=Label(root, text=str.get(), padx=5,pady=5,width=20, bg='white',fg="black",relief=GROOVE,font=('helvetica 18 bold'))
		car_result.place(x=150,y=80)
		
		id_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='ID',font=('helvetica 15 bold'))
		id_label.place(x=0,y=150)
		id_label_in=Entry(root,width=20,textvariable=myid,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
		id_label_in.place(x=150,y=150)
		
		name_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='이름',font=('helvetica 15 bold'))
		name_label.place(x=0,y=210)
		name_label_in=Entry(root,width=20,textvariable=myname,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
		name_label_in.place(x=150,y=210)
		
		phone_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='휴대폰',font=('helvetica 15 bold'))
		phone_label.place(x=0,y=280)
		phone_label_in=Entry(root,width=20,textvariable=myphone,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
		phone_label_in.place(x=150,y=280)	
		
		jangae_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='장애인',font=('helvetica 15 bold'))
		jangae_label.place(x=0,y=350)
		jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp,font=('helvetica 15 bold'))
		jangae_label_ck1.place(x=150,y=350)
		jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp,font=('helvetica 15 bold'))
		jangae_label_ck2.place(x=330,y=350)
		
		next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=lambda:save_info(1),font=('helvetica 18 bold'))
		next_button.place(x=340,y=500)
	
	home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
	home_button.place(x=170,y=500)
	
	prev_button=Button(root, text='이전',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=lambda:prev(1),font=('helvetica 18 bold'))
	prev_button.place(x=0,y=500)

	     
#차량검사
def next_info():
	global myname
	global myphone
	global mydp
	global yes_dp
	global no_dp
	yes_dp = IntVar()
	no_dp = IntVar()
	myname = StringVar()
	myphone = StringVar()
	zone = StringVar()
	background_label.pack_forget()
	
	list = root.place_slaves()
	for l in list:
		l.destroy()
		
	if dev_mysql.search_car_num_from_member(str.get()) == None and dev_mysql.search_car_num_from_session(str.get()) == None:
		car_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='차량번호',font=('helvetica 15 bold'))
		car_label.place(x=0,y=80)
		car_result=Label(root, text=str.get(), padx=5,pady=5,width=20, bg='white',fg="black",relief=GROOVE,font=('helvetica 18 bold'))
		car_result.place(x=150,y=80)
		
		name_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='이름',font=('helvetica 15 bold'))
		name_label.place(x=0,y=180)
		name_label_in=Entry(root,width=20,textvariable=myname,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
		name_label_in.place(x=150,y=180)
		
		phone_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='휴대폰',font=('helvetica 15 bold'))
		phone_label.place(x=0,y=280)
		phone_label_in=Entry(root,width=20,textvariable=myphone,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
		phone_label_in.place(x=150,y=280)
		
		jangae_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='장애인',font=('helvetica 15 bold'))
		jangae_label.place(x=0,y=380)
		jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp,font=('helvetica 15 bold'))
		jangae_label_ck1.place(x=150,y=380)
		jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp,font=('helvetica 15 bold'))
		jangae_label_ck2.place(x=330,y=380)
		
		next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=lambda:save_info(2),font=('helvetica 18 bold'))
		next_button.place(x=340,y=500)
		
		home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
		home_button.place(x=170,y=500)
	else :
		if dev_mysql.search_car_num_from_member(str.get()) != None:
			
			car_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='차량번호',font=('helvetica 15 bold'))
			car_label.place(x=0,y=80)
			car_result=Label(root, text=str.get(), padx=5,pady=5,width=20, bg='white',fg="black",relief=GROOVE,font=('helvetica 18 bold'))
			car_result.place(x=150,y=80)
		
			name_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='이름',font=('helvetica 15 bold'))
			name_label.place(x=0,y=180)
			name_label_in=Entry(root,width=20,textvariable=myname,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
			name_label_in.insert(END,dev_mysql.search_car_num_from_member(str.get())['userName'])
			name_label_in.place(x=150,y=180)
			
			phone_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='휴대폰',font=('helvetica 15 bold'))
			phone_label.place(x=0,y=280)
			phone_label_in=Entry(root,width=20,textvariable=myphone,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
			phone_label_in.insert(END,dev_mysql.search_car_num_from_member(str.get())['userPhone'])
			phone_label_in.place(x=150,y=280)
			
			jangae_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='장애인',font=('helvetica 15 bold'))
			jangae_label.place(x=0,y=380)
			if dev_mysql.search_car_num_from_member(str.get())['userDP'] ==1:
				jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp,font=('helvetica 15 bold'))
				jangae_label_ck1.place(x=150,y=380)
				jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp,font=('helvetica 15 bold'))
				jangae_label_ck2.place(x=330,y=380)
				yes_dp.set(1)
			else :
				jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp,font=('helvetica 15 bold'))
				jangae_label_ck1.place(x=150,y=380)
				jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp,font=('helvetica 15 bold'))
				jangae_label_ck2.place(x=330,y=380)
				no_dp.set(1)
			
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='주민차량 입니다',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)	
			
			home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
			home_button.place(x=170,y=500)
			
			next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=lambda:save_info(2),font=('helvetica 18 bold'))
			next_button.place(x=340,y=500)
			
		elif dev_mysql.search_car_num_from_session(str.get()) != None:
			
			car_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='차량번호',font=('helvetica 15 bold'))
			car_label.place(x=0,y=80)
			car_result=Label(root,text=str.get(),width=20,bg='white',fg='black',bd=0,relief=GROOVE,font=('helvetica 18 bold'))
			car_result.place(x=150,y=80)
			
			name_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='이름',font=('helvetica 15 bold'))
			name_label.place(x=0,y=180)
			name_label_in=Entry(root,width=20,textvariable=myname,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
			name_label_in.insert(END,dev_mysql.search_car_num_from_session(str.get())['userName'])
			name_label_in.place(x=150,y=180)
			
			phone_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='휴대폰',font=('helvetica 15 bold'))
			phone_label.place(x=0,y=280)
			phone_label_in=Entry(root,width=20,textvariable=myphone,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
			phone_label_in.insert(END,dev_mysql.search_car_num_from_session(str.get())['userPhone'])
			phone_label_in.place(x=150,y=280)
			
			jangae_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='장애인',font=('helvetica 15 bold'))
			jangae_label.place(x=0,y=380)
			
			if dev_mysql.search_car_num_from_session(str.get())['userDP'] ==1:
				yes_dp.set(1)
				jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp,font=('helvetica 15 bold'))
				jangae_label_ck1.place(x=150,y=380)
				jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp,font=('helvetica 15 bold'))
				jangae_label_ck2.place(x=330,y=380)
			else :
				no_dp.set(1)
				jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp,font=('helvetica 15 bold'))
				jangae_label_ck1.place(x=150,y=380)
				jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp,font=('helvetica 15 bold'))
				jangae_label_ck2.place(x=330,y=380)
				
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='방문이력이 있습니다',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)	
			
			home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
			home_button.place(x=170,y=500)
			
			next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=lambda:save_info(2),font=('helvetica 18 bold'))
			next_button.place(x=340,y=500)
	
	prev_button=Button(root, text='이전',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=lambda:prev(2),font=('helvetica 18 bold'))
	prev_button.place(x=0,y=500)
	
	
def out_info():
	global yes_check
	global no_check
	yes_check = IntVar()
	no_check = IntVar()
	
	background_label.pack_forget()
	
	list = root.place_slaves()
	for l in list:
		l.destroy()
	
	if dev_mysql.search_car_num_from_parking(str.get()) != None:
		
		car_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='차량번호',font=('helvetica 15 bold'))
		car_label.place(x=0,y=80)	
		car_label=Label(root,padx=5,pady=5,width=30,bg='white',fg='black',relief=GROOVE,text=str.get(),font=('helvetica 15 bold'))
		car_label.place(x=150,y=80)
		
		name_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='이름',font=('helvetica 15 bold'))
		name_label.place(x=0,y=180)
		name_label=Label(root,padx=5,pady=5,width=30,bg='white',fg='black',relief=GROOVE,text=dev_mysql.search_car_num_from_parking(str.get())['userName'],font=('helvetica 15 bold'))
		name_label.place(x=150,y=180)
		
		in_time = dev_mysql.search_car_num_from_parking(str.get())['inTime']
		time_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='이용시간',font=('helvetica 15 bold'))
		time_label.place(x=0,y=280)
		time_label=Label(root,padx=5,pady=5,width=30,bg='white',fg='black',relief=GROOVE,text=dev_time.getDiffTimetoTimeString(in_time),font=('helvetica 15 bold'))
		time_label.place(x=150,y=280)
		
		jangae_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='장애인',font=('helvetica 15 bold'))
		jangae_label.place(x=0,y=380)
		
		if dev_mysql.search_car_num_from_parking(str.get())['userDP'] ==1:
			yes_check.set(1)
			jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_check,font=('helvetica 15 bold'))
			jangae_label_ck1.place(x=150,y=380)
			jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_check,font=('helvetica 15 bold'))
			jangae_label_ck2.place(x=330,y=380)

		else :
			no_check.set(1)
			jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_check,font=('helvetica 15 bold'))
			jangae_label_ck1.place(x=150,y=380)
			jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_check,font=('helvetica 15 bold'))
			jangae_label_ck2.place(x=330,y=380)
			
		out_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='black',bd=0,relief=GROOVE,text='출차 하시겠습니까?',font=('helvetica 15 bold'))
		out_label.place(x=0,y=430)
			
		next_button=Button(root, text='출차',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=lambda:save_info(3),font=('helvetica 18 bold'))
		next_button.place(x=340,y=500)
	
	else :
		record=Label(root,padx=5,pady=5,width=39,bg='skyblue',fg='black',relief=GROOVE,text='입차 기록이 없습니다',font=('helvetica 15 bold'))
		record.place(x=0,y=220)
		
		
	home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
	home_button.place(x=170,y=500)
		
	prev_button=Button(root, text='이전',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=lambda:prev(3),font=('helvetica 18 bold'))
	prev_button.place(x=0,y=500)
	
	    
def prev(choice):
	
	but3.place_forget()
	list = root.place_slaves()
	for l in list:
		l.destroy()
		
	img2 = ImageTk.PhotoImage(Image.open(chars+".jpg"))
	background_label.configure(image = img2)
	background_label.image = img2
	background_label.pack()
	
	result_number2=Entry(root,width=20,bg='white',fg="black",textvariable=str,relief=GROOVE,font=('helvetica 18 bold'))
	result_number2.place(x=20,y=500)
	if choice == 1:
		next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=idmake,font=('helvetica 18 bold'))
		next_button.place(x=340,y=500)
	elif choice == 2:
		next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=next_info,font=('helvetica 18 bold'))
		next_button.place(x=340,y=500)
	elif choice == 3:
		next_button=Button(root, text='다음',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=out_info,font=('helvetica 18 bold'))
		next_button.place(x=340,y=500)
   
def save_info(choice):
	#A, B, C, D 아파트 지정 아파트B 일경우 APT_B로 변경
	zone = 'APT_A'
	if choice == 1:
		if myid.get() == '' :
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='ID를 입력하세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		elif myname.get() == '':
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='이름을 입력하세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		elif myphone.get() == '':
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='휴대폰번호를 입력하세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		elif yes_dp.get() == 1 and no_dp.get() == 1:
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='장애여부를 한개만 체크해주세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		elif yes_dp.get() == 0 and no_dp.get() == 0:
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='장애여부를 체크해주세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		else:
			if yes_dp.get() == 1:
				dev_mysql.registUser(myid.get(), str.get(), myname.get(), myphone.get(), yes_dp.get())
			elif no_dp.get() == 1:
				dev_mysql.registUser(myid.get(), str.get(), myname.get(), myphone.get(), yes_dp.get())
				
			list = root.place_slaves()
			for l in list:
				l.destroy()
					
			but3.place_forget()
				
			save_form=Label(root,padx=5,pady=5,width=39,bg='SkyBlue2',fg='white',bd=0,relief=GROOVE,text='등록\n되었습니다',font=('helvetica 15 bold'))
			save_form.place(x=0,y=170)
								
			home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
			home_button.place(x=170,y=500)			
	elif choice == 2:
		if myname.get() == '':
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='이름을 입력하세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		elif myphone.get() == '':
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='휴대폰번호를 입력하세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		elif yes_dp.get() == 1 and no_dp.get() == 1:
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='장애여부를 한개만 체크해주세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		elif yes_dp.get() == 0 and no_dp.get() == 0:
			notice_label=Label(root,padx=5,pady=5,width=39,bg='white',fg='dark violet',bd=0,relief=GROOVE,text='장애여부를 체크해주세요',font=('helvetica 15 bold'))
			notice_label.place(x=0, y=420)
		else:
			if yes_dp.get() == 1:
				dev_mysql.in_car_parking(str.get(), myname.get(), myphone.get(), yes_dp.get(), zone)
			elif no_dp.get() == 1:
				dev_mysql.in_car_parking(str.get(), myname.get(), myphone.get(), yes_dp.get(), zone)
				
			list = root.place_slaves()
			for l in list:
				l.destroy()
					
			but3.place_forget()
				
			save_form=Label(root,padx=5,pady=5,width=39,bg='SkyBlue2',fg='white',bd=0,relief=GROOVE,text='입력\n되었습니다',font=('helvetica 15 bold'))
			save_form.place(x=0,y=170)
								
			home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
			home_button.place(x=170,y=500)
		
	elif choice == 3:
		dev_mysql.out_car_parking(str.get())
		
		list = root.place_slaves()
		for l in list:
			l.destroy()
			
		but3.place_forget()
		
		save_form=Label(root,padx=5,pady=5,width=39,bg='SkyBlue2',fg='white',bd=0,relief=GROOVE,text='출차\n되었습니다',font=('helvetica 15 bold'))
		save_form.place(x=0,y=170)
		
		
		home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
		home_button.place(x=170,y=500)

def gohome():
   list = root.place_slaves()
   for l in list:
      l.destroy()
      
   img2 = ImageTk.PhotoImage(Image.open("snow.jpg"))
   background_label.configure(image = img2)
   background_label.image = img2
   background_label.pack(side=TOP)
   
   cntInCar = dev_mysql.in_out_re_able_Parking()[0]
   cntOutCar = dev_mysql.in_out_re_able_Parking()[1]
   cntReCar = dev_mysql.in_out_re_able_Parking()[2]
   cntAbleCar = dev_mysql.in_out_re_able_Parking()[3]
   
   inlabel=Label(root,image=inimg,text=cntInCar,compound='center',bg='white',font=('helvetica 20 bold'))
   inlabel.place(x=5,y=380)

   outlabel=Label(root,image=outimg,text=cntOutCar,compound='center',bg='white',font=('helvetica 20 bold'))
   outlabel.place(x=125,y=380)

   relabel=Label(root,image=reimg,text=cntReCar,compound='center',bg='white',font=('helvetica 20 bold'))
   relabel.place(x=245,y=380)

   ablelabel=Label(root,image=ableimg,text=cntAbleCar,compound='center',bg='white',font=('helvetica 20 bold'))
   ablelabel.place(x=365,y=380)
   
   but1.place(x=0,y=60)
   label1.place(x=0,y=130)
   but2.place(x=160,y=140)
   but3.place(x=340,y=500)
   but5.place(x=0,y=270)
   A_reset.place(x=0,y=335)
   B_reset.place(x=120,y=335)
   C_reset.place(x=240,y=335)
   D_reset.place(x=360,y=335)
   
   #inlabel.place(x=5,y=380)
   #outlabel.place(x=125,y=380)
   #relabel.place(x=245,y=380)
   #ablelabel.place(x=365,y=380)

def manage():
   global example
   
   but3.place_forget()
   list = root.place_slaves()
   for l in list:
      l.destroy()
   
   example = StringVar()
   
   but1.place_forget()
   but2.place_forget()
   but5.place_forget()
   label1.place_forget()
   inlabel.place_forget()
   outlabel.place_forget()
   relabel.place_forget()
   ablelabel.place_forget()
   A_reset.place_forget()
   B_reset.place_forget()
   C_reset.place_forget()
   D_reset.place_forget()
   background_label.pack_forget()
   
   car_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='차량번호',font=('helvetica 15 bold'))
   car_label.place(x=0,y=80)
   car_result=Entry(root,width=20,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'),textvariable=example)
   car_result.place(x=150,y=80)
   
   search_but=Button(root,padx=5,pady=5,width=39,bg='SeaGreen1',fg='black',relief=GROOVE,command=search_info,text='검색',font=('helvetica 15 bold'))
   search_but.place(x=0,y=170)
   
   prev_button=Button(root, text='이전',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
   prev_button.place(x=0,y=500)
   
   home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
   home_button.place(x=170,y=500)

def search_info():
	global chnumber
	global chname
	global chphone
	global yes_dp2
	global no_dp2
	
	yes_dp2 = IntVar()
	no_dp2 = IntVar()
	chnumber=StringVar()
	chname=StringVar()
	chphone=StringVar()
	
	if dev_mysql.search_car_num_from_member(example.get()) != None:
		list = root.place_slaves()
		for l in list:
			l.destroy()
			
		car_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='차량번호',font=('helvetica 15 bold'))
		car_label.place(x=0,y=80)
		car_result=Entry(root,width=20,textvariable=chnumber,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
		car_result.insert(END,example.get())
		car_result.place(x=150,y=80)
		
		name_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='이름',font=('helvetica 15 bold'))
		name_label.place(x=0,y=180)
		name_label_in=Entry(root,width=20,textvariable=chname,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
		name_label_in.insert(END,dev_mysql.search_car_num_from_member(example.get())['userName'])
		name_label_in.place(x=150,y=180)
		
		phone_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='휴대폰',font=('helvetica 15 bold'))
		phone_label.place(x=0,y=280)
		phone_label_in=Entry(root,width=20,textvariable=chphone,bg='white',fg='black',relief=GROOVE,font=('helvetica 18 bold'))
		phone_label_in.insert(END,dev_mysql.search_car_num_from_member(example.get())['userPhone'])
		phone_label_in.place(x=150,y=280)
		
		jangae_label=Label(root,padx=5,pady=5,width=8,bg='gray26',fg='white',bd=0,relief=GROOVE,text='장애인',font=('helvetica 15 bold'))
		jangae_label.place(x=0,y=380)
		
		if dev_mysql.search_car_num_from_member(example.get())['userDP'] ==1:
			yes_dp2.set(1)
			jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp2,font=('helvetica 15 bold'))
			jangae_label_ck1.place(x=150,y=380)
			jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp2,font=('helvetica 15 bold'))
			jangae_label_ck2.place(x=330,y=380)
		else :
			no_dp2.set(1)
			jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp2,font=('helvetica 15 bold'))
			jangae_label_ck1.place(x=150,y=380)
			jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp2,font=('helvetica 15 bold'))
			jangae_label_ck2.place(x=330,y=380)
			
		change_but=Button(root,padx=5,pady=5,width=39,bg='SeaGreen1',fg='black',bd=0,relief=GROOVE,command=change_info,text='수정',font=('helvetica 15 bold'))
		change_but.place(x=0,y=430)	
		
		prev_button=Button(root, text='이전',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=manage,font=('helvetica 18 bold'))
		prev_button.place(x=0,y=500)
		
		home_button=Button(root, text='HOME',padx=5,pady=5,width=8, bg='slate gray',fg='white',bd=0, relief=GROOVE,command=gohome,font=('helvetica 18 bold'))
		home_button.place(x=170,y=500)
		
	else:
		search=Label(root,padx=5,pady=5,width=39,bg='skyblue',fg='black',relief=GROOVE,text='차량이 없습니다',font=('helvetica 15 bold'))
		search.place(x=0,y=220)
		
def change_info():
	
	if chnumber.get() == example.get() or dev_mysql.search_car_num_from_member(chnumber.get()) == None:
		car_label=Label(root,padx=5,pady=5,width=30,bg='white',fg='black',relief=GROOVE,text=chnumber.get(),font=('helvetica 15 bold'))
		car_label.place(x=150,y=80)
		
		name_label=Label(root,padx=5,pady=5,width=30,bg='white',fg='black',relief=GROOVE,text=chname.get(),font=('helvetica 15 bold'))
		name_label.place(x=150,y=180)
		
		phone_label=Label(root,padx=5,pady=5,width=30,bg='white',fg='black',relief=GROOVE,text=chphone.get(),font=('helvetica 15 bold'))
		phone_label.place(x=150,y=280)
		
		if yes_dp2.get() == 1 and no_dp2.get() == 0:
			jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp2,font=('helvetica 15 bold'))
			jangae_label_ck1.place(x=150,y=380)
			jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp2,font=('helvetica 15 bold'))
			jangae_label_ck2.place(x=330,y=380)
			yes_dp2.set(1)
			dev_mysql.update_member(example.get(), chnumber.get(), chname.get(), chphone.get(), yes_dp2.get())
		else:
			jangae_label_ck1=Checkbutton(root,width=8,height=1,text='yes',bg='white',bd=0,variable=yes_dp2,font=('helvetica 15 bold'))
			jangae_label_ck1.place(x=150,y=380)
			jangae_label_ck2=Checkbutton(root,width=8,height=1,text='no',bg='white',bd=0,variable=no_dp2,font=('helvetica 15 bold'))
			jangae_label_ck2.place(x=330,y=380)
			no_dp2.set(1)
			dev_mysql.update_member(example.get(), chnumber.get(), chname.get(), chphone.get(), yes_dp2.get())
		
		change_but=Button(root,padx=5,pady=5,width=39,bg='SeaGreen1',fg='black',bd=0,relief=GROOVE,command=change_info,text='수정완료',font=('helvetica 15 bold'))
		change_but.place(x=0,y=430)
		notice_but=Label(root,padx=5,pady=5,width=39,bg='white',bd=0,relief=GROOVE,text='',font=('helvetica 15 bold'))
		notice_but.place(x=0,y=470)
	else :
		
		notice_but=Label(root,padx=5,pady=5,width=39,bg='white',fg='orange red',bd=0,relief=GROOVE,text='등록되어있는 차량번호 입니다',font=('helvetica 15 bold'))
		notice_but.place(x=0,y=470)

def reset_zone(choice):

    if choice ==1 :
        dev_mysql.APTreset_car_parking('APT_A')
	
    elif choice ==2 :
        dev_mysql.APTreset_car_parking('APT_B')
	
    elif choice ==3 :
        dev_mysql.APTreset_car_parking('APT_C')
	
    elif choice ==4 :
        dev_mysql.APTreset_car_parking('APT_D')

def flashevent():
    if flash['bg']=='gray':
        flash['bg']='black'
        flash['fg']='yellow'
    else :
        flash['bg']='gray'
        flash['fg']='black'

class App():
   
   def __init__(self):
      self.update_clock()  
      root.mainloop()  
        
   def update_clock(self):
      nowtime=Label(frame,padx=5,pady=5,width=14,bg='white',fg='black',bd=0,relief=GROOVE,text=dev_time.getCurrentStrMinTime(),font=('helvetica 13 bold'))
      nowtime.place(x=325,y=19)  
      root.after(1000,self.update_clock) 
      
inimg = ImageTk.PhotoImage(Image.open("incar.png"))
outimg = ImageTk.PhotoImage(Image.open("outcar.png"))
reimg = ImageTk.PhotoImage(Image.open("recar.png"))
ableimg = ImageTk.PhotoImage(Image.open("ablecar.png"))	            
thunderimg = ImageTk.PhotoImage(Image.open("thunder.png"))   

but1=Button(frame,padx=5,pady=5,width=39,bg='skyblue',fg='white',bd=0,relief=GROOVE,command=lambda:capture(1),text='차량 등록',font=('helvetica 15 bold'))
but1.place(x=0,y=60)

label1=Label(frame,width=10,height=5,bg='gold2',fg='white',bd=0,relief=GROOVE,text='주차장\n관리',font=('helvetica 15 bold'))
label1.place(x=0,y=130)

but2=Button(frame,width=23,height=4,bg='dim gray',fg='white',bd=0,relief=GROOVE,command=lambda:capture(2),text='차량 검사',font=('helvetica 15 bold'))
but2.place(x=160,y=140)

but3=Button(frame,padx=5,pady=5,width=8,bg='slate gray',fg='white',bd=0,relief=GROOVE,text='종료',command=exitt,font=('helvetica 18 bold'))
but3.place(x=340,y=500)

but5=Button(frame,padx=5,pady=5,width=39,bg='skyblue',fg='white',bd=0,relief=GROOVE,command=manage,text='주민 정보 관리',font=('helvetica 15 bold'))
but5.place(x=0,y=270)

flash=Button(frame,padx=5,pady=5,width=8,bg='gray',fg='black',bd=0,relief=GROOVE,text='플래쉬',command=flashevent,font=('helvetica 18 bold'))
flash.place(x=0,y=10)

A_reset=Button(frame,padx=5,pady=5,width=8,bg='slate gray',fg='white',bd=0,relief=GROOVE,command=lambda:reset_zone(1),text='A reset',font=('helvetica 15 bold'))
A_reset.place(x=0,y=335)

B_reset=Button(frame,padx=5,pady=5,width=8,bg='slate gray',fg='white',bd=0,relief=GROOVE,command=lambda:reset_zone(2),text='B reset',font=('helvetica 15 bold'))
B_reset.place(x=120,y=335)

C_reset=Button(frame,padx=5,pady=5,width=8,bg='slate gray',fg='white',bd=0,relief=GROOVE,command=lambda:reset_zone(3),text='C reset',font=('helvetica 15 bold'))
C_reset.place(x=240,y=335)

D_reset=Button(frame,padx=5,pady=5,width=8,bg='slate gray',fg='white',bd=0,relief=GROOVE,command=lambda:reset_zone(4),text='D reset',font=('helvetica 15 bold'))
D_reset.place(x=360,y=335)

cntInCar = dev_mysql.in_out_re_able_Parking()[0]
cntOutCar = dev_mysql.in_out_re_able_Parking()[1]
cntReCar = dev_mysql.in_out_re_able_Parking()[2]
cntAbleCar = dev_mysql.in_out_re_able_Parking()[3]

inlabel=Label(frame,image=inimg,text=str(cntInCar),compound='center',bg='white',font=('helvetica 20 bold'))
#inlabel.place(x=5,y=480)
inlabel.place(x=5,y=380)

outlabel=Label(frame,image=outimg,text=str(cntOutCar),compound='center',bg='white',font=('helvetica 20 bold'))
outlabel.place(x=125,y=380)

relabel=Label(frame,image=reimg,text=str(cntReCar),compound='center',bg='white',font=('helvetica 20 bold'))
relabel.place(x=245,y=380)

ablelabel=Label(frame,image=ableimg,text=str(cntAbleCar),compound='center',bg='white',font=('helvetica 20 bold'))
ablelabel.place(x=365,y=380)

app=App()

#root.mainloop()

