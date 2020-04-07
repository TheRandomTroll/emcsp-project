from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import argparse
import cv2
import numpy as np
import picamera


def detect_bright_spots(image):

    return


def main():
    camera = PiCamera()
    camera.color_effects = (128, 128)
    camera.resolution = (640, 480)
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(640, 480))

    sleep(0.1)
    print("Camera initialized")
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        raw_capture.truncate(0)
        if key == ord("q"):
            break
if __name__ == "__main__":
    main()
