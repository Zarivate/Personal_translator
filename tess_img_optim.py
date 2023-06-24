# File that contains all the various tesseract methods to optimize image and display results

import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from deepl_api_call import *
import re


# Custom recommended Japanese settings from documentation found here: https://tesseract-ocr.github.io/tessdoc/tess3/ControlParams.html
# Overall page sementation method (psm) 6 seems to work best overall for horizontal text. 5 works best for vertical although sometimes if
# image is too low res won't capture anything. TODO: Test out lower res crops with opimization methods.
# TODO: Add a feature where can detect orientation of text so can swap to vertical japanese, 'jpn-vert'
# Tesseract options can be found in detail here: https://muthu.co/all-tesseract-ocr-options/
custom_config = r"""--oem 3 --psm 5 -c 
edges_max_children_per_outline=40 
chop_enable=T 
use_new_state_cost=F 
segment_segcost_rating=F 
enable_new_segsearch=0 
language_model_ngram_on=0 
textord_force_make_prop_words=F"""

# Want to make sure all output text is on a single line for best translation so making list that holds which characters
# to remove. Will need to replace any white space and new lines with ""
chars_remove = [" ", "\n"]


# Function to read image
def set_image(image_path):
    return cv2.imread(image_path)


# Functions to adjust image for better readability
# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


# Function to get the regular tesseract output
def get_tess_string(img):
    result = pytesseract.image_to_string(img, lang="jpn_vert", config=custom_config)
    for char in chars_remove:
        result = result.replace(char, "")
    return result


# Function to clear up whatever the user input as the crops to adjust
def clear_user_string(input):
    print("The user input before clearing is " + input)

    input = re.sub(r"\D", "", input)

    print("The user input after edits is " + input)
    return input


def get_tess_data(img):
    return pytesseract.image_to_data(
        img, lang="jpn_vert", config=custom_config, output_type=Output.DICT
    )


# Function to just print out the list of characters found, was how discovered wasn't displaying the discovered characters correctly
def print_chars(img):
    result = pytesseract.image_to_data(
        img, lang="jpn_vert", config=custom_config, output_type=Output.DICT
    )
    # Print out every character in the 'text' array within the result matrix, all on the same line due to "end="""
    for i in range(len(result["text"])):
        print(result["text"][i], end="")


# Function to display the characters found alongside their confidence scores
def display_characters(img, data, n_boxes):
    for i in range(n_boxes):
        # Currently will display any bounding boxes and scores for anything found with a confidence score of above 60
        if int(data["conf"][i]) > 60:
            (x, y, w, h) = (
                data["left"][i],
                data["top"][i],
                data["width"][i],
                data["height"][i],
            )
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # It just puts question marks on any Japanese characters, even if the characters print correctly in the run console so ignore for now
            # TODO: Look into why this is and see if there's a possible fix
            # img = cv2.putText(
            #     img,
            #     data["text"][i],
            #     (x, y + h + 20),
            #     cv2.FONT_HERSHEY_COMPLEX,
            #     0.7,
            #     (0, 255, 0),
            #     2,
            #     cv2.LINE_AA,
            # )
            img = cv2.putText(
                img,
                str(data["conf"][i]),
                (x, y + h + 20),
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

    cv2.imshow("img", img)
    cv2.waitKey(0)


# Function to print the captured text from tesseract alongside it's translation and display the
# image with bounding boxes and confidence scores drawn on.
def print_results(img, type):
    output_tess = get_tess_string(img)
    print("Result with " + type + " is \n" + output_tess + "\n")
    print("Translated it becomes \n" + translate(output_tess))

    data_normal = get_tess_data(img)
    display_characters(img, data_normal, len(data_normal["text"]))
