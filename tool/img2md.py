#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyocr
import pyocr.builders
import cv2
from PIL import Image
import numpy as np

def img2wordbox(file):
    # Load Image
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    thresh, img = cv2.threshold(img, np.average(img), 255, cv2.THRESH_BINARY)
    
    img = Image.fromarray(np.uint8(img))
    
    tools = pyocr.get_available_tools()
    
    if len(tools) == 0:
        print("No OCR tool found")
        exit()
        
    tool = tools[0]
    # Word Recognition
    word_box = tool.image_to_string(
        img,
        lang="eng",
        builder=pyocr.builders.LineBoxBuilder()
        )
    
    return word_box

def img2md(file):
    word_box = img2wordbox(file)

    words = []
    for box in word_box:
        words.append(box.content)

    f = open("output.md", "w")
    for word in words:
        f.writelines("%s  \n" %(word))
    f.close()

img2md("sample2.png")