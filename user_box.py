import cv2
import numpy as np
import imutils
from screeninfo import get_monitors
import pyautogui


# Function to retrieve the image data
def get_image_data(img_path):
    img = cv2.imread(img_path)
    print(type(img))
    h, w, c = img.shape
    print("Height is ", h)
    print("Width is ", w)
    print("channel:", c)
    print(type(img.shape))


def get_monitor_info():
    print(pyautogui.size())
    monitors = get_monitors()
    print(monitors[0].width)
    print(monitors[0].height)
    for monitor in get_monitors():
        width = monitor.width
        height = monitor.height

        print(str(width) + "x" + str(height))


# Function to resize the image
def resize_image(img):
    img = imutils.resize(img, width=500)


# Function to get user crops from their image
def get_crops(img_path):
    # Read image
    img_raw = cv2.imread(img_path)

    # TODO: Make it so image is resized depending on how large it is while maintaining aspect ratio
    img_raw = imutils.resize(img_raw, width=500)

    # Create window called "select crop sections" where user can select multipl ROIs
    ROIs = cv2.selectROIs("Select crop sections", img_raw)

    # Print rectangle points of selected roi
    print(ROIs)

    # Created a variable to increment that represents the current number of the cropped image
    crop_number = 0

    # Loop through every crop created and stored within ROIs
    for crop in ROIs:
        # Get the 4 points/regions of interest from the drawn rectangle on the image
        x1 = crop[0]
        y1 = crop[1]
        x2 = crop[2]
        y2 = crop[3]

        # Crop selected roi from raw image
        img_cropped = img_raw[y1 : y1 + y2, x1 : x1 + x2]
        # Create a window of the cropped image with a name corresponding to which sequential crop it was
        cv2.imshow("crop" + str(crop_number) + ".jpg", img_cropped)
        # Create and save the cropped image in the example_outputs folder with a corresponding numnbered name
        cv2.imwrite("example_outputs/crop" + str(crop_number) + ".jpg", img_cropped)
        # Increment the crop number so following, if there is any more, cropped images can be correctly numbered
        crop_number += 1
    cv2.waitKey(0)
