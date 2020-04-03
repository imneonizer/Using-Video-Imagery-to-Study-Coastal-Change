import cv2
import time
import imutils

cap = cv2.VideoCapture("timelapse.mp4")

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

#calculate video fps
if int(major_ver) < 3:
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
else:
    fps = cap.get(cv2.CAP_PROP_FPS)

#time at which video processing started
st = time.time()

frames = {}
frame_num = 0
while True:
    success, frame = cap.read()
    if not success: break
    frame = imutils.resize(frame, width=800)

    if frame_num == 0:
        cv2.imwrite("snapshot.jpg", frame)

    #convert image to B&W and calculate mean
    luminosity = round(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).mean())

    #calculate relative time lapsed
    sec = frame_num/fps

    #store luminosity as key and frame as value in a dictionary
    #if another frame had same means (brightness) then old key value pair will be replaced
    #this method is efficient since we don't have to store every single frame in the memory
    frames[luminosity] = (frame, frame_num, round(sec))
    frame_num += 1

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"): break

#time elapsed while processing the video
print(">> Elapsed: {} sec".format(round(time.time()-st, 3)))

#finding brightest frame in the video
frame = frames[max(frames)]
bright = cv2.putText(frame[0], "bright, frame number: {}, time: {} sec".format(frame[1], frame[2]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#finding darkest frame in the video
frame = frames[min(frames)]
dark = cv2.putText(frame[0], "dark, frame number: {}, time: {} sec".format(frame[1], frame[2]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#write to disk
cv2.imwrite("brightest.jpg", bright)
cv2.imwrite("darkest.jpg", dark)

#showing image
cv2.imshow("brightest", bright)
cv2.imshow("darkest", dark)
cv2.waitKey(0)
