#!/usr/bin/python2

import numpy as np
import cv2
import thread
from math import *

import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT_X = 5005

sock_x = socket.socket(socket.AF_INET,    # Internet
                       socket.SOCK_DGRAM) # UDP



cap = cv2.VideoCapture(0)

cap_width = cap.get(3)
cap_height = cap.get(3)

#print(str(width))
#print(str(height))
#cap.set(3, 320)
#for i in range(2, 256):
#        cap.set(i, 0)

#print(str(cap.get(3)))
#print(str(cap.get(4)))

def nothing(x):
	pass

cv2.namedWindow('image')
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.set_xlabel("y")
#ax.set_ylabel("x")
#ax.set_zlabel("z")

#cv2.createTrackbar('max', 'image', 0, 255, nothing)
#cv2.createTrackbar('min', 'image', 0, 255, nothing)

bufsize = 20
points = list()
for i in range(0, bufsize):
	points.append([0, 0, 0])

x = 0
y = 0
z = 0
width = 0
height = 0


while (True):
	#global x, y, z, width, height
	# Capture frame-by-frame
	ret, frame = cap.read()
	if ret is False:
		continue

	frame = cv2.flip(frame, 1)


	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#min = cv2.getTrackbarPos('min','image')
	#max = cv2.getTrackbarPos('max','image')
	min = 100
	max = 255

	#blank = np.zeros((480,640,3), np.uint8)

	ret, thresh = cv2.threshold(gray, min, max, cv2.THRESH_BINARY)
	thresh = cv2.GaussianBlur(thresh, (9, 9), 0)
	#thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

	#keypoints = detector.detect(thresh)
	#bimg = cv2.drawKeypoints(blank, keypoints, np.array([]), (0,0,255),\
	#cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	cont = thresh.copy()
	contours, hierarchy = cv2.findContours(cont, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


	#big1 = 0
	#big2 = 0
	#big1i = 0
	#big2i = 0
	#i = 0
	#for cnt in contours:
		#i += 1
		#x, y, w, h = cv2.boundingRect(cnt)
		#size = w*h
		#if size > big1:
			#big1 = size
			#big1i = i
		#elif size > big2:
			#big2 = size
			#big2i = i



	r = 0
	l = width
	ri = 0
	li = 0
	i = 0
	for cnt in contours:
		i += 1
		x, y, w, h = cv2.boundingRect(cnt)
		if x > r:
			r = x
			ri = i
		if x < l:
			l = x
			li = i
		#cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

	if i > 0:
		x1, y1, w1, h1 = cv2.boundingRect(contours[ri-1])
		#print("Right: "+str(x1)+" "+str(y1))
		x2, y2, w2, h2 = cv2.boundingRect(contours[li-1])
		#print("Left: "+str(x2)+" "+str(y2))


		x = -.5+(x1/cap_width)
		y = .5-(y1/cap_height)
		#z = -.5+((w1*h1)/2000)
		z = -.5
		points[-1] = [x, y, z]

		print(str(points[-1][0])+","+str(points[-1][1])+","+str(points[-1][2]))
		sock_x.sendto(str(points[-1][0])+","+str(points[-1][1])+","+str(points[-1][2]), (UDP_IP, UDP_PORT_X))

		#font = cv2.FONT_HERSHEY_SIMPLEX
		#cv2.putText(frame, str(angle), (x, y), font, 2, (255,255,255), 2)

			#ax.plot([points[2][0], points[1][1]],
			#        [points[2][1], points[1][1]],
			#        [points[2][2], points[1][2]], c = "r")


		for i in range(0, bufsize-1):
			points[i] = points[i+1]



		cv2.rectangle(frame, (x1,y1), (x1+w1,y1+h1), (0,255,255), 2)
		cv2.rectangle(frame, (x2,y2), (x2+w2,y2+h2), (255,0,255), 2)
	else:
		sock_x.sendto(str(points[-1][0])+","+str(points[-1][1])+","+str(points[-1][2]), (UDP_IP, UDP_PORT_X))

	for i in range(0, bufsize-1):
		cv2.line(frame, (int(points[i+1][0]),   int(points[i+1][1])),
		                (int(points[i][0]), int(points[i][1])),
		                (int(points[i][2]), 0, 0), 5)



	#max = cv2.minMaxLoc(gray)[3]
	#cv2.circle(gray, max, 20, (255,0,255), -1)


	# Display the resulting frame
	#cv2.imshow('boxes', blank)
	cv2.imshow('image', frame)
	#cv2.imshow('image2', thresh)
	#cv2.imshow('image3', cont)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	#raw_input()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
