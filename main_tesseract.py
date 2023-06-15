import cv2
from tess_img_optim import *


# Test image
img = cv2.imread("examples/example_12.jpg")


# Preprocess the images using the various methods in tess_img_optim for greater accuracy
gray = get_grayscale(img)
noise_removal_image = remove_noise(gray)
threshed_image = thresholding(gray)
dilation_image = dilate(gray)
erosion_image = erode(img)
opening_image = opening(img)
canny_image = canny(img)
skew_corrected_image = deskew(gray)


# Example with no preprocessing
print_results(img, "no preprocessing")


# # Example with grayscale preprocessing
# print_results(gray, "grayscale")


# # Example with noise removal preprocessing
# print_results(noise_removal_image, "noise removal")


# # Example with threshold preprocessing
# print_results(threshed_image, "thresholding")


# # Example with dilation preprocessing
# # print_results(dilation_image, "dilation")


# # Example with erosion preprocessing
# print_results(erosion_image, "erosion")


# Example with opening preprocessing
# print_results(opening_image, "opening")


# Example with canny edge detection preprocessing
# print_results(canny_image, "canny edge detection")


# Example with skew correction preprocessing
# print_results(canny_image, "skew correction")


# Get the characters found and print bounding boxes out for them
# h, w, c = img.shape
# boxes = pytesseract.image_to_boxes(img)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# cv2.imshow('img', img)
# cv2.waitKey(0)
