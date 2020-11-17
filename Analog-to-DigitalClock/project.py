import cv2
import numpy as np
import math

def display_time(hour, mini, sec):
  for i in range(12):
    if hour>i*30 and hour < (i+1)*30:
      hours = i
      if hours == 0: hours = 12
  for i in range(60):
    if mini > i*6 and mini < (i+1)*6:
      minis = i
  for i in range(60):
    if sec > i*6 - 3 and sec < (i+1)*6 - 3:
      secs = i
  return [hours, minis, secs]

def m_len(center, point1, point2):
  if abs(center[0]-point1[0])**2+abs(center[1]-point1[1])**2 > abs(center[0]-point2[0])**2+abs(center[1]-point2[1])**2: return point1
  else: return point2

def find_center(image):
  dst = image.copy()
  gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
  circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1 = 250, param2 = 10, minRadius = 2, maxRadius = 40)
  print(circles)
  for i in circles[0]:
    if(abs(i[0]-i[1]) < 10):
      return [i[0],i[1]]

def find_12(image):
  dst = image.copy()
  gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
  circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1 = 250, param2 = 10, minRadius = 2, maxRadius = 20)
  for i in circles[0]:
    if(i[1]<190):
      return [i[0],i[1]]

def find_angle(center, point):
  pointed = [point[0]-center[0],point[1]-center[1]]
  if pointed[0]>0 and pointed[1]>0:
    angle = math.atan(pointed[1]/pointed[0])*180/math.pi + 90
  elif pointed[0]>0 and pointed[1]<0:
    angle = 90 - math.atan(-pointed[1]/pointed[0])*180/math.pi
  elif pointed[0]<0 and pointed[1]<0:
    angle = math.atan(pointed[1]/pointed[0])*180/math.pi + 270
  elif pointed[0]<0 and pointed[1]>0:
    angle = 270 - math.atan(pointed[1]/-pointed[0])*180/math.pi
  return angle

def find_point(image):
  blur = cv2.GaussianBlur(image,(3,3),0)
  canny = cv2.Canny(blur,100,200)
  lines = cv2.HoughLinesP(canny,2,np.pi/180,60,np.array([]), minLineLength=40, maxLineGap=3)
  avg_lines = np.average(lines, axis=0)
  if avg_lines is not None:
    for line in avg_lines:
      x1, y1, x2, y2 = line.reshape(4)
      point = m_len(center,[x1,y1],[x2,y2])
  return point

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1),(x2,y2), (255,0,0), 2)
    return line_image

#frame = cv2.imread('clock_s.png')
cap = cv2.VideoCapture('clock_f.mp4')
while(cap.isOpened()):
  _, frame = cap.read()
  copy_imag = frame.copy()
  lower_red = (90, 10, 190)
  upper_red = (130, 50, 255)
  img_mask_red = cv2.inRange(copy_imag, lower_red, upper_red)
  lower_blue = (180, 100, 0)
  upper_blue = (255, 190, 70)
  img_mask_blue = cv2.inRange(copy_imag, lower_blue, upper_blue)
  lower_white = (190, 190, 190)
  upper_white = (255, 255, 255)
  img_mask_white = cv2.inRange(copy_imag, lower_white, upper_white)

  #center = find_center(frame)
  center = [204,204]
  
  angle_red = find_angle(center, find_point(img_mask_red))
  angle_blue = find_angle(center, find_point(img_mask_blue))
  angle_white = find_angle(center, find_point(img_mask_white))

  times = display_time(angle_red, angle_white, angle_blue)

  print("지금 시간은 ",times[0],"시 ",times[1],"분 ",times[2],"초 입니다.")
  cv2.imshow('clock', frame)
  cv2.waitKey(1)


#line_image = display_lines(copy_imag, lines)
#cv2.imshow('result', line_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
