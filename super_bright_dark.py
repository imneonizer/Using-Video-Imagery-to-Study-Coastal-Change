import cv2
import time
import imutils
import numpy as np
from PIL import Image
from tqdm import tqdm

#video capture object
cap = cv2.VideoCapture("timelapse.mp4")
st = time.time()

#progressbar for reading frames

frames = []
output_shape = None
print("reading frames")
while True:
    success, frame = cap.read()
    if not success: break

    #resize frames for faster processing
    frame = imutils.resize(frame, width=800)

    #storing frame shape for later array reshaping
    if len(frames) == 0:
        #store frame shape, for reshaping flatten arrays later
        output_shape = frame.shape

        #start progressbar
        pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), initial=0)

    #flattening frame and storing every pixel
    #of current frame as 1d array inside a list
    frames.append(frame.flatten())
    pbar.update(1)

#close progressbar
pbar.close()

#converting list to array
#first column of array stores first pixel from every frames
# similarly second column stores 2nd pixel and so on..
frames = np.array(frames)


bright_frame, dark_frame = [], []
print("\nprocessing frames")
for column in tqdm(frames.T):
    bright_frame.append(np.max(column))
    dark_frame.append(np.min(column))

bright_frame = np.array(bright_frame).reshape(output_shape)
dark_frame = np.array(dark_frame).reshape(output_shape)

print("\nelapsed: {} sec".format(round(time.time()-st, 2)))

cv2.imwrite("super_bright_frame.jpg", bright_frame)
cv2.imwrite("super_dark_frame.jpg", dark_frame)

#cv2.imshow("bright_frame", bright_frame)
#cv2.imshow("dark_frame", dark_frame)
#cv2.waitKey(0)
