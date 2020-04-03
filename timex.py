import numpy as np
import cv2
import time
import imutils

#open the video file
cap = cv2.VideoCapture("timelapse.mp4")

rAvg, gAvg, bAvg = None, None, None
avg = None
idx = 0
st = time.time()
while True:
    success, frame = cap.read()
    if not success: break

    #resize frame for faster processing
    frame = imutils.resize(frame, width=800)

    #split bgr
    (B, G, R) = cv2.split(frame.astype("float"))

    if rAvg is None:
        rAvg = R
        bAvg = B
        gAvg = G

    else:
        # operations for the full r g b channels per image
        rAvg = ((idx * rAvg) + (1 * R)) / (idx + 1.1)
        gAvg = ((idx * gAvg) + (1 * G)) / (idx + 1.1)
        bAvg = ((idx * bAvg) + (1 * B)) / (idx + 1.1)

    idx += 1

    # merge the RGB averages together and write the output image to disk
    avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")

    avg_demo = cv2.putText(avg.copy(), 'Frames added:'+str(idx), (10, 30), cv2.FONT_HERSHEY_PLAIN,2,(128, 255, 0),2)

    # Display the resulting frame
    cv2.imshow('Long Exposure', avg_demo)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

#time elapsed while processing the video
print(">> Elapsed: {} sec".format(round(time.time()-st, 3)))

#writing to disk
cv2.imwrite("timex.jpg", avg)
