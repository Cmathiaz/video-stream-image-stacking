# A very simple streamed video image stacking code!
#
# improves statistical camera noise (and the resolution a little) by stacking
# many images captured from an rtsp protocol security camera.
#
# no frame to frame ECC motion vector estimation done here, only simple stacking
# and averaging! The built-in 3D noise reduction available in most cameras
# averages only over smaller number of frames. but it is done in real time
#
# a final stacked output image is produced after averaging the frames.
# press q in the displayed video window to abort during frame capture.
#
# resolution improvements are only marginal. Noise improvement is better.
# if there is any movement in the field of view, it will get blurred.
# Works correctly only if there is no movement.
#
# developed this simple python code using Pycharm in an M1 Macbook Air.
#
# C. Mathiazhagan, IIT Madras

import cv2
import numpy as np
import matplotlib.pyplot as plt

username = 'admin'  # usually the default username is admin
password = 'password'  # enter the password string here
ipaddress = '192.168.0.50'  # enter the ip address of the camera, use DHCP in
                            # your wifi router to hardwire it to some permanent value
portnumber = '554'  # rtsp video stream port address

print("Before URL")  # for checking

# look up correct rtsp address, it usually goes like these
# cap = cv2.VideoCapture('rtsp://admin:password@192.168.0.50:554')
# cap = cv2.VideoCapture('rtsp://admin:password@192.168.0.50')

# for special Imou cameras, LOOC 2, Ranger 2, Cue 2, this is the correct rtsp string!
# check this website: https://www.ispyconnect.com/camera/imou
# cap = cv2.VideoCapture('rtsp://admin:password@192.168.0.51/cam/realmonitor?channel=1&subtype=00&authbasic=YWRtaW46YWRtaW4=')

cap = cv2.VideoCapture('rtsp://'+username+':'+password+'@'+ipaddress+':'
                       + portnumber+'/cam/realmonitor?channel=1&subtype=00')

print("After URL")  # if you see this, the camera is streaming correctly!

count = 0  # frame count
ret, frame = cap.read()

if not ret:
    print('not able to capture the stream!')
    exit()

# initialize some empty arrays for use
img = np.zeros(frame.shape, np.uint8)
imgBGR = np.zeros(frame.shape, np.uint32)
imgFinal = np.zeros(frame.shape, np.uint32)
imgDiff = np.zeros(frame.shape, np.uint8)

# capture 100 frames and stop, camera fps is usually 25 frames per second
# so the capture time is 4 seconds

while count < 100:  # can change to higher number, but improvements are marginal

    # print('About to start the Read command')
    ret, frame = cap.read()
    # print('About to show frame of Video.')

    # copy frame to image for manipulation
    img = frame  # copy frame to image, not necessary, wasted some memory here
    H, W, Ch = img.shape  # get height, width and channel sizes
    imgBGR[:, :, 0:3] += img[:, :, 0:3]  # stack images by adding and accumulating BGR

    cv2.imshow("Capturing", img)

    count = count + 1  # count number of frames

    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to abort while capturing
        break

# capture done now
cap.release()
cv2.destroyAllWindows()

imgFinal = np.uint8(imgBGR[:, :, :]/count)  # find average and recast
                                                  # to integers
print('captured frame height, width and channels =', H, W, Ch)

imgDiff = cv2.absdiff(imgFinal, img)  # difference between the last frame and the stacked image

# recast bgr to rgb channels for matlabplot
b, g, r = cv2.split(imgFinal)
img_rgb = cv2.merge((r, g, b))

print('final image size =', img_rgb.shape)
plt.title('final stacked image!')
plt.imshow(img_rgb)
plt.show()

# now show the difference image
b, g, r = cv2.split(imgDiff)
img_rgb = cv2.merge((r, g, b))
plt.title('the difference from the last captured frame!')
plt.imshow(img_rgb)
plt.show()
