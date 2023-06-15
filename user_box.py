import cv2
import numpy as np

# Set image path
img_path = "examples/example_12.jpg"

# Read image
img_raw = cv2.imread(img_path)

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
