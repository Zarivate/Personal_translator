from easyocr import Reader
import cv2
from matplotlib import pyplot as plt
import numpy as np


# Load model for English and Japanese
reader_en_ja = Reader(["en", "ja"])
result = reader_en_ja.readtext("examples/example_1.jpg")
print(result)
print(result[0])
print(result[0][0])
print(result[0][0][0])


def read_text(image_name, model_name, in_line=True):
    # Read the data
    text = model_name.readtext(image_name, detail=0, paragraph=in_line)

    # Join texts writing each text in new line
    return "\n".join(text)


jp_example_1 = read_text("examples/example_1.jpg", reader_en_ja)
print("\n" + jp_example_1)
