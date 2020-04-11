from imutils import contours
from picamera.array import PiRGBArray
from picamera import PiCamera
from skimage import measure
from time import sleep
import argparse
import cv2
import enum
import imutils
import numpy as np
import picamera

def enum(**enums):
    return type("Enum", (), enums)

LightPosition = enum(none = 0, left = 1, right = 2, center = 3)

def detect_bright_spots(image, sensitivity, min_thresh):
    output = []
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    threshold = cv2.threshold(blurred, min_thresh, 255, cv2.THRESH_BINARY)[1]

    threshold = cv2.erode(threshold, None, iterations=2)
    threshold = cv2.dilate(threshold, None, iterations=4)

    labels = measure.label(threshold, neighbors=8, background=0)
    mask = np.zeros(threshold.shape, dtype="uint8")

    for label in np.unique(labels):
        if label == 0:
            continue

        label_mask = np.zeros(threshold.shape, dtype="uint8")
        label_mask[labels == label] = 255
        num_pixels = cv2.countNonZero(label_mask)

        if num_pixels > sensitivity:
            mask = cv2.add(mask, label_mask)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if(len(cnts) != 0):
            cnts = contours.sort_contours(cnts)[0]

        for (i, c) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            tl = (x, y)
            br = (x + w, y + h)
            if (tl, br) in output:
                continue
            output.append((tl, br))
            cv2.rectangle(image, tl, br, (0, 0, 255), 3)
            cv2.putText(image, "#{}".format(i + 1),(x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255))

    return output

def determine_light_position(bright_spots):
    def intersection(a,b):

        x1 = max(a[0], b[0])
        y1 = max(a[1], b[1])
        x2 = min(a[2], b[2])
        y2 = min(a[3], b[3])
        w = x2 - x1
        h = y2 - y1

        if w<0 or h<0:
            return ()

        return (x1, y1, x2, y2)

    output = LightPosition.none
    left_rectangle = (0, 0, 200, 479)
    right_rectangle = (440, 0, 639, 480)
    for (tl, br) in bright_spots:
        rectangle = (tl[0], tl[1], br[0], br[1])
        if intersection(rectangle, left_rectangle) == rectangle:
            if output == LightPosition.right:
                output = LightPosition.center
                break
            else:
                output = LightPosition.left

        elif intersection(rectangle, right_rectangle) == rectangle:
            if output == LightPosition.left:
                output = LightPosition.center
                break
            else:
                output = LightPosition.right
        else:
            output = LightPosition.center
            break

    return output


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("-s", "--sensitivity", required=False,help="number of pixels required to be considered a \"bright spot\"", default=300, type=float)
    ap.add_argument("-t", "--threshold", required=False,help="how bright a pixel has to be to be considered \"bright\"", default=200, type=int)

    args = ap.parse_args()
    sensitivity = args.sensitivity
    threshold = args.threshold
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(640, 480))

    sleep(0.1)
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        bright_spots = detect_bright_spots(image, sensitivity, threshold)

        for (tl, br) in bright_spots:
            print("(%d, %d), (%d, %d)" % (tl[0], tl[1], br[0], br[1]))
        print("====================")

        light_position = determine_light_position(bright_spots)
        print(light_position)

        cv2.namedWindow("Frame")
        cv2.moveWindow("Frame", 40, 30)
        cv2.imshow("Frame", image)

        key = cv2.waitKey(1) & 0xFF

        raw_capture.truncate(0)
        if key == ord("q"):
            break
if __name__ == "__main__":
    main()
