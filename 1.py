import cv2                             
import numpy as np 
import math
import vlc

player = vlc.MediaPlayer("hussain_badshah.mp3")


cap = cv2.VideoCapture(0)                	#creating camera object
while( cap.isOpened() ) :

	ret,img = cap.read() 
	img = cv2.flip(img, 1)

	cv2.rectangle(img, (100, 100), (300, 300), (0, 255, 0), 0)
	crop_image = img[100:300, 100:300]


	gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)

	ret,thresh1 = cv2.threshold(gray,40,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	image, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	cnt = max(contours, key=lambda x: cv2.contourArea(x))

	hull = cv2.convexHull(cnt)

	#define area of hull and area of hand
	areahull = cv2.contourArea(hull)
	areacnt = cv2.contourArea(cnt)

	#find the percentage of area not covered by hand in convex hull
	arearatio=((areahull-areacnt)/areacnt)*100

	# drawing = np.zeros(crop_image.shape,np.uint8)
	cv2.drawContours(crop_image,[cnt],0,(0,255,0),2)
	cv2.drawContours(crop_image,[hull],0,(0,0,255),2)
	
	# finding convex hull
	hull = cv2.convexHull(cnt,returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)

	count_defects = 0

	print("defects",defects)
	for i in range(defects.shape[0]):

		s, e, f, d = defects[i, 0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])

		a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
		b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
		c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
		angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14


		# if angle > 90 draw a circle at the far point
		if angle <= 90:
			count_defects += 1
			cv2.circle(crop_image, far, 1, [0, 0, 255], -1)
		cv2.line(crop_image, start, end, [0, 255, 0], 2)

	# print("areacnt",areacnt)
	# if areacnt<2000:
	# 		cv2.putText(img,'Put hand in the box',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
	if count_defects == 0:
		if areacnt<2000:
			cv2.putText(img,'Put hand in the box',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
		else:
			if arearatio<12:
				cv2.putText(img,'0',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
			elif arearatio<17.5:
				cv2.putText(img,'Best of luck',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
				
			else:
				cv2.putText(img,'ONE',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
	elif count_defects == 1:
		cv2.putText(img, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
	elif count_defects == 2:
		player.play()
		cv2.putText(img, "THREE", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)

	elif count_defects == 3:
		cv2.putText(img, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
	elif count_defects == 4:
		player.stop()
	 	cv2.putText(img, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
	else:
		pass
	
	
	cv2.imshow('input',img)
	cv2.imshow('threshold',thresh4)   






	k = cv2.waitKey(1)
	if k == ord("q"):
		break



