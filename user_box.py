import cv2
import imutils
from screeninfo import get_monitors
from tess_img_optim import *
import pyautogui


# Function that begins the cropping function if user agrees to
def crop_start(img, type):
    answer = input(
        "Do you want to crop parts of the image to get better accuracy? (y/n) \n"
    )

    # https://tutorial.eyehunts.com/python/while-loop-yes-or-no-python-example-code/
    while answer.lower() not in ("y", "n"):
        answer = input(
            "Please enter either y or n to continue. y is to begin cropping process while n is to not. "
        )

    if answer == "y":
        img = get_image_data(img)
        names = get_crops(img)
        for name in names:
            img = cv2.imread(name)
            print_results(img, type)
    else:
        img = get_image_data(img)
        print_results(img, type)


# Function to retrieve the image data and resize image, while maintaining aspect ratio, if any parameter exceeds the monitor
def get_image_data(img):
    # Get the height, width, and channel. If the channel is 3 then it's an RGB(color) image, else it's grayscale/monochrome
    # https://stackoverflow.com/questions/23660929/how-to-check-whether-a-jpeg-image-is-color-or-gray-scale-using-only-python-stdli
    img_w = img.shape[1]
    print(img_w)

    img_h = img.shape[0]
    monitor = get_monitor_info()
    print(get_monitor_info())
    print(monitor[0])
    # Check to see if the image width or height is larger than the monitor's dimensions, if so resize it before continuing
    if img_w > monitor[0]:
        # Set the width to be the exact heigh of the monitor's width by subtracting the difference of the two from it
        img_w -= img_w - monitor[0]
        img = imutils.resize(img, width=int(img_w - 100))
    if img_h > monitor[1]:
        # Set the height to be the exact heigh of the monitor's height by subtracting the difference of the two from it
        img_h -= img_h - monitor[1]
        # To make sure the forefront of the desktop doesn't cover the image, an extra 100 pixels is subtracted before resizing
        img = imutils.resize(img, height=int(img_h - 100))

    return img

    # print("Image Height is ", h)
    # print("Image Width is ", w)
    # print("channel:", c)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)


# Gets the dimensions of the main monitor to know whether file needs to be re
def get_monitor_info():
    # Returns the primary monitor's width and height
    return (get_monitors()[0].width, get_monitors()[0].height)

    # print(pyautogui.size())
    # For multiple monitors gets the dimensions for them
    # for monitor in get_monitors():
    #     width = monitor.width
    #     height = monitor.height

    #     print(str(width) + "x" + str(height))


# Function to get user crops from their image
def get_crops(img):
    # Read image
    # img_raw = cv2.imread(img)

    # TODO: Make it so image is resized depending on how large it is while maintaining aspect ratio
    # img_raw = imutils.resize(img_raw, width=500)

    # Create window called "select crop sections" where user can select multipl ROIs
    ROIs = cv2.selectROIs("Select crop sections", img)
    crop_names = []

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
        img_cropped = img[y1 : y1 + y2, x1 : x1 + x2]

        # Create a window of the cropped image with a name corresponding to which sequential crop it was

        cv2.imshow("crop" + str(crop_number) + ".jpg", img_cropped)

        # Create and save the cropped image in the example_outputs folder with a corresponding numnbered name
        cv2.imwrite("example_outputs/crop" + str(crop_number) + ".jpg", img_cropped)
        file_name_path = "example_outputs/crop" + str(crop_number) + ".jpg"
        crop_names.append(file_name_path)
        # Increment the crop number so following, if there is any more, cropped images can be correctly numbered
        crop_number += 1
    cv2.waitKey(0)
    # Return an array containing the dimensions
    return crop_names
