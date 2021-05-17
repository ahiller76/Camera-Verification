### Aaron Hiller Kit Sloan
import cv2
import numpy as np

File = open("CameraParams.txt", 'r')
data = []
data_temp = []

for data_line in File:
    line = data_line.strip()
    if not line.startswith('#'):
        input_data = data_line.rstrip().split()
        for val in input_data:
            data_temp.append(float(val))
        data.append(data_temp)
        data_temp = []
File.close()

# Number of images taken
Img_Num = data[1][0]
# Intrinsics matrix K
K = np.array(data[2:5])
# Store data for extrensics matrix
Rot_Mat = np.array(data[5:8][:])
Trans_Vec = np.array(data[5+int(Img_Num)*3:8+int(Img_Num)*3][:])

# Extrinsics matrix for world to camera frame
Ext_Mat = np.concatenate((Rot_Mat, np.transpose(Trans_Vec)), axis=0)

# Distance away from camera in mm
Z = 520

# World to camera frame
Cam_Mat = np.dot(Ext_Mat, K)/Z

# Matrix for camera to world calculations
Cam_Mat_Inv = np.linalg.pinv(Cam_Mat)

def Find_World(event, r, c, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        RC_Coords = np.array([r, c, 1])
        World_Coords = np.dot(RC_Coords, Cam_Mat_Inv)
        Cam_Coords = np.dot([World_Coords[0],World_Coords[1],0,1], Cam_Mat)
        print("World Coordinates")
        print("(" + str(World_Coords[0]) + ", " + str(World_Coords[1]) + ")")
        print("Camera Coordinates")
        print("(" + str(Cam_Coords[0]) + ", " + str(Cam_Coords[1]) + ")")
        cv2.circle(image, (int(RC_Coords[0]), int(RC_Coords[1])), 1, (0, 0, 255), thickness=-1)
        cv2.putText(image, "(" + str(round(World_Coords[0], 2)) + "," + str(round(World_Coords[1],2)) + ")",
                    (int(RC_Coords[0] - 25), int(RC_Coords[1] - 10)),
                    cv2.FONT_HERSHEY_COMPLEX, .4 , (0, 0, 255))
        cv2.imshow("Click anywhere to create a point", image)

capture = cv2.VideoCapture(0)
escape = False
while not escape:
    has_frame, frame = capture.read()
    if not has_frame:
        print('Can\'t get frame')
        break
    cv2.imshow('Press ESC to determine world space coordinates', frame)

    key = cv2.waitKey(3)
    if key == 27:
        print('Pressed esc')
        image = frame
        escape = True
capture.release()
cv2.destroyAllWindows()
escape = False
while not escape:
    cv2.imshow('Click anywhere to create a point', image)
    cv2.setMouseCallback('Click anywhere to create a point', Find_World)
    key = cv2.waitKey(0)
    if key == 27:
        print('Pressed esc')
        escape = True
cv2.destroyAllWindows()