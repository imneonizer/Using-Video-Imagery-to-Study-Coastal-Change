import numpy as np
import cv2
import imutils
import time

#reading video file
cap = cv2.VideoCapture('timelapse.mp4')

#background subtractor object
bgsub = cv2.createBackgroundSubtractorMOG2()

idx = 0
st = time.time()
while True:
    success, frame = cap.read()
    if not success: break

    #resize frame for faster processing
    frame = imutils.resize(frame, width=800)

    # if first frame
    if idx == 0:
        first_frame = frame.copy()
        height, width = frame.shape[:2]
        accum_image = np.zeros((height, width), np.uint8)
        idx +=1

    else:
        #remove the background
        bgsub_mask = bgsub.apply(frame)

        #threashold image to remove noises from subtracted background mask
        ret, th1 = cv2.threshold(bgsub_mask, 2, 2, cv2.THRESH_BINARY)

        # add to the accumulated image
        accum_image = cv2.add(accum_image, th1)

        #use first frame of video and apply background subtracted mask
        color_image = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
        variance = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)

        #showing output
        cv2.imshow("original", frame)
        cv2.imshow("variance", variance)

        if cv2.waitKey(1) & 0xFF == ord('q'): break

print(">> Elapsed: {} sec".format(round(time.time()-st, 3)))

#save to the disk
cv2.imwrite('variance.jpg', variance)
