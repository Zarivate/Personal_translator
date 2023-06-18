from time import perf_counter
from easyocr import Reader
import cv2
from matplotlib import pyplot as plt
import numpy as np


# Load model for English and Japanese
reader_en_ja = Reader(["en", "ja"])

# Start the counters
t1_start = perf_counter()


result = reader_en_ja.readtext("examples/example_8.jpg")

print(str(result) + "\n")
print(str(result[0]) + "\n")
print(str(result[0][0]) + "\n")
print(str(result[0][0][0]) + "\n")

# Stop the stopwatch / counter
t1_stop = perf_counter()


def read_text(image_name, model_name, in_line=True):
    # Read the data
    text = model_name.readtext(image_name, detail=0, paragraph=in_line)

    # Join texts writing each text in new line
    return "\n".join(text)


jp_example_1 = read_text("examples/example_12.jpg", reader_en_ja)
print("\n" + jp_example_1)

print("Elapsed time:", t1_stop, t1_start)


print("Elapsed time during the whole program in seconds:", t1_stop - t1_start)
