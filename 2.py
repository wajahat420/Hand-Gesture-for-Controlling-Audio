import cv2                             
import numpy as np   
import math
                        #importing libraries
cap = cv2.VideoCapture(0)                #creating camera object
while( cap.isOpened() ) :

	ret,img = cap.read()  
	img =  cv2.flip(img, 1)                       #reading the frames
	cv2.imshow('input',img)

	cv2.rectangle(img, (100, 100), (300, 300), (0, 255, 0), 0)
	crop_image = img[100:300, 100:300]

	gray = cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)

	ret,thresh1 = cv2.threshold(blur,50,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	image,contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	cnt = max(contours, key=lambda x: cv2.contourArea(x))
	hull = cv2.convexHull(cnt)

	drawing = np.zeros(crop_image.shape,np.uint8)
	cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
	cv2.drawContours(drawing,[hull],0,(0,0,255),3)

	hull = cv2.convexHull(cnt,returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)

	count_defects = 0

	for i in range(defects.shape[0]):
		s,e,f,d = defects[i,0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])

		a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
		b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
		c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
	
		angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57


		calculate = s*(s-a)*(s-b)*(s-c)
		if calculate > a and calculate > b and calculate > c:
			ar = math.sqrt(calculate)
			d=(2*ar)/a
			# print("d",d)
			# if d < 30:
			# 	count_defects -= 1
		else:
			# print("else")
			d = 5

		if angle <= 90 :
			count_defects += 1
			cv2.circle(crop_image, far, 2, [0, 0, 255], 2)
		cv2.line(crop_image,start,end,[0,255,0],2)                
		# cv2.circle(crop_image,far,5,[0,0,255],-1)
	if count_defects == 0:
		cv2.putText(img, "ONE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2)
	elif count_defects == 1:
		cv2.putText(img, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
	elif count_defects == 2:
		cv2.putText(img, "THREE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
	elif count_defects == 3:
		cv2.putText(img, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
	elif count_defects == 4:
		cv2.putText(img, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
	else:
		pass

	print("defects",count_defects)	
	# except:
	# 	print("except")
	# 	pass
	cv2.imshow('threshold',thresh1) 
	cv2.imshow("contour and hull",drawing)  
	cv2.imshow('input',img)



	k = cv2.waitKey(1)
	if k == 27:
		break
