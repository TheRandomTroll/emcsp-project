from imutils import contours
from picamera.array import PiRGBArray
from picamera import PiCamera
from skimage import measure
from time import sleep
import argparse
import cv2
import imutils
import numpy as np
import picamera


def detect_bright_spots(image):
    output = []
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    threshold = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

    threshold = cv2.erode(threshold, None, iterations=2)
    threshold = cv2.dilate(threshold, None, iterations=4)

    labels = measure.label(threshold, neighbors=8, background=0)
    mask = np.zeros(threshold.shape, dtype="uint8")

    for label in np.unique(labels):
        if label == 0:
            continue

        label_mask = np.zeros(threshold.shape, dtype="uint8")
        label_mask[labels == label] = 2555
        num_pixels = cv2.countNonZero(label_mask)

        if num_pixels > 300:
            mask = cv2.add(mask, label_mask)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if(len(cnts) != 0):
            cnts = contours.sort_contours(cnts)[0]

        for (i, c) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            output.append(((cX, cY), radius))
            cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
            cv2.putText(image, "#{}".format(i + 1),(x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255))

    cv2.namedWindow("Output")
    cv2.moveWindow("Output", 700, 30)
    cv2.imshow("Output", threshold)
    return output

def main():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(640, 480))

    sleep(0.1)
    print("Camera initialized")
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        bright_spots = detect_bright_spots(image)

        print("====================")
        for ((cX, cY), radius) in bright_spots:
            print("(%d, %d), radius = %d" % (cX, cY, radius))
        print("====================")

        cv2.namedWindow("Frame")
        cv2.moveWindow("Frame", 40, 30)
        cv2.imshow("Frame", image)

        key = cv2.waitKey(1) & 0xFF

        raw_capture.truncate(0)
        if key == ord("q"):
            break
if __name__ == "__main__":
    main()
