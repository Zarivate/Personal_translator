import pytesseract
from pytesseract import Output
import cv2
import numpy as np

# Works well with all real life images, document snippet example, but only properly on example 6 for game snippets
img = cv2.imread("examples/example_12.jpg")


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


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


# Custom recommended Japanese settings from documentation found here: https://tesseract-ocr.github.io/tessdoc/tess3/ControlParams.html
# Overall page sementation method (psm) 6 seems to work best overall.
# TODO: Add a feature where can detect orientation of text so can swap to vertical japanese, 'jpn-vert'
custom_config = r"""--oem 3 --psm 6 -c 
edges_max_children_per_outline=40 
chop_enable=T 
use_new_state_cost=F 
segment_segcost_rating=F 
enable_new_segsearch=0 
language_model_ngram_on=0 
textord_force_make_prop_words=F"""


# Preprocess the images using the various methods for greater accuracy
gray = get_grayscale(img)
noise_removal_image = remove_noise(gray)
threshed_image = thresholding(gray)
dilation_image = dilate(gray)
erosion_image = erode(img)
opening_image = opening(img)
canny_image = canny(img)
skew_corrected_image = deskew(gray)


# Function to display the characters found alongside their confidence scores
def display_characters(img, data, n_boxes):
    for i in range(n_boxes):
        if int(data["conf"][i]) > 60:
            (x, y, w, h) = (
                data["left"][i],
                data["top"][i],
                data["width"][i],
                data["height"][i],
            )
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img = cv2.putText(
                img,
                data["text"][i],
                (x, y + h + 20),
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
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


# Example with no preprocessing
print(
    "Result with no preprocessing is \n"
    + pytesseract.image_to_string(img, lang="jpn", config=custom_config)
    + "\n"
)
data_normal = pytesseract.image_to_data(
    img, lang="jpn", config=custom_config, output_type=Output.DICT
)
n_boxes_normal = len(data_normal["text"])
display_characters(img, data_normal, n_boxes_normal)

# for char in d['text']:
#     print(char)


# Example with grayscale preprocessing
print(
    "Result with grayscale preprocessing is \n"
    + pytesseract.image_to_string(gray, lang="jpn", config=custom_config)
)
data_gray = pytesseract.image_to_data(
    gray, lang="jpn", config=custom_config, output_type=Output.DICT
)

display_characters(gray, data_gray, len(data_gray["text"]))

# Example with noise removal preprocessing
# print("Result with noise removal preprocessing is \n" + pytesseract.image_to_string(noise_removal_image, lang='jpn', config=custom_config))


# Example with threshold preprocessing
# print("Result with threshold preprocessing is \n" + pytesseract.image_to_string(threshed_image, lang='jpn', config=custom_config))


# Example with dilation preprocessing
# print("Result with dilation preprocessing is \n" + pytesseract.image_to_string(dilation_image, lang='jpn', config=custom_config))


# Example with erosion preprocessing
# print("Result with erosion preprocessing is \n" + pytesseract.image_to_string(erosion_image, lang='jpn', config=custom_config))


# Example with opening preprocessing
# print("Result with opening preprocessing is \n" + pytesseract.image_to_string(opening_image, lang='jpn', config=custom_config))


# Example with canny edge detection preprocessing
# print("Result with canny edge detection preprocessing is \n" + pytesseract.image_to_string(canny_image, lang='jpn', config=custom_config))


# Example with skew correction preprocessing
# print("Result with skew correction preprocessing is \n" + pytesseract.image_to_string(skew_corrected_image, lang='jpn', config=custom_config))


# Get the characters found and print bounding boxes out for them
# h, w, c = img.shape
# boxes = pytesseract.image_to_boxes(img)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# cv2.imshow('img', img)
# cv2.waitKey(0)
