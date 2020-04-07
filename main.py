from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import argparse
import cv2
import numpy as np
import picamera


def detect_bright_spots(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    threshold = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.erode(threshold, None, iterations=2)
    threshold = cv2.dilate(threshold, None, iterations=4)

    cv2.namedWindow("Output")
    cv2.moveWindow("Output", 700, 30)
    cv2.imshow("Output", threshold)

def main():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(640, 480))

    sleep(0.1)
    print("Camera initialized")
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        detect_bright_spots(image)
        cv2.namedWindow("Frame")
        cv2.moveWindow("Frame", 40, 30)
        cv2.imshow("Frame", image)

        key = cv2.waitKey(1) & 0xFF

        raw_capture.truncate(0)
        if key == ord("q"):
            break
if __name__ == "__main__":
    main()
