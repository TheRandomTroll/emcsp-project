from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import argparse
import cv2
import numpy as np
import picamera


def detect_bright_spots():
    return


def main():
    camera = picamera.PiCamera()
    camera.color_effects = (128, 128)

    camera.start_preview()
    print("Warming up camera...")
    sleep(0.1)
    print("Camera initialized.")
    while True:
        print("Capturing image...")
        camera.capture("foo.jpg")
        print("Detecting bright spots...")
        detect_bright_spots()

if __name__ == "__main__":
    main()
