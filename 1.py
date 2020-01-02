import cv2                             
import numpy as np 
import math
import vlc
import Block_face

player = vlc.MediaPlayer("song.mp3")


cap = cv2.VideoCapture(0) 
faceCascade = cv2.CascadeClassifier("/home/wajahat/Desktop/opencv/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
playing = False

while( cap.isOpened() ) :
	

	ret,img = cap.read() 
	img = cv2.flip(img, 1)


	cv2.rectangle(img, (100, 100), (300, 300), (0, 255, 0), 0)
	crop_image = img[100:300, 100:300]


	gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)


	cv2.putText(img,'3=>Play',(450,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 4, cv2.LINE_AA)
	cv2.putText(img,'5=>Pause',(450,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 4, cv2.LINE_AA)


	ret,thresh1 = cv2.threshold(gray,50,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	image, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	cnt = max(contours, key=lambda x: cv2.contourArea(x))

	hull = cv2.convexHull(cnt)
	try:

		#define area of hull and area of hand
		areahull = cv2.contourArea(hull)
		areacnt = cv2.contourArea(cnt)

		#find the percentage of area not covered by hand in convex hull
		arearatio=((areahull-areacnt)/areacnt)*100

		drawing = np.zeros(crop_image.shape,np.uint8)
		cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
		cv2.drawContours(drawing,[hull],0,(0,0,255),2)
		
		# finding convex hull
		hull = cv2.convexHull(cnt,returnPoints = False)
		defects = cv2.convexityDefects(cnt,hull)

		count_defects = 0

		# print("defects",type(defects))
		# if defects is not None:
			# print("working")
		for i in range(defects.shape[0]):

			s, e, f, d = defects[i, 0]
			start = tuple(cnt[s][0])
			end = tuple(cnt[e][0])
			far = tuple(cnt[f][0])

			a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
			b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
			c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
			# d=(2*ar)/a
		
			# apply cosine rule here
			angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
		
	
			# if angle > 90 draw a circle at the far point
			if angle <= 90:
				count_defects += 1
				cv2.circle(crop_image, far, 2, [0, 0, 255], 2)
			cv2.line(crop_image, start, end, [0, 255, 0], 2)

		print("defects",count_defects)
		# if areacnt<2000:
		# 		cv2.putText(img,'Put hand in the box',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
		# if count_defects == 0:
		# 	if areacnt<2000:
		# 		cv2.putText(img,'Put hand in the box',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
		# 	else:
		# 		pass
				# if arearatio<12:
				# 	cv2.putText(img,'0',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
				# elif arearatio<17.5:
				# 	cv2.putText(img,'Best of luck',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
					
				# else:
				# 	cv2.putText(img,'ONE',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
		# elif count_defects == 1:
		# 	cv2.putText(img, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		if count_defects == 2:
			player.play()
			playing = True

		# elif count_defects == 3:
		# 	cv2.putText(img, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		elif count_defects == 4:
			player.stop() 
			playing = False
		
		if playing:
			cv2.putText(img, "PLAYING...!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 3)
		else:
			cv2.putText(img, "STOP...!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 3)

		

	except:
		print("except")
		pass


	cv2.imshow('input',img)
	cv2.imshow('threshold',thresh1)   


	k = cv2.waitKey(1)
	if k == ord("q"):
		break



