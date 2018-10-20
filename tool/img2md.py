#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyocr
import pyocr.builders
import cv2
from PIL import Image
import numpy as np

def img2wordbox(img):
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

def img2md(input_path, output_path):
    # Load Image
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    thresh, img = cv2.threshold(img, np.average(img), 255, cv2.THRESH_BINARY)
    
    img = Image.fromarray(np.uint8(img))

    word_box = img2wordbox(img)

    words = []
    for box in word_box:
        words.append(box.content)

    f = open(output_path, "w")
    for word in words:
        f.writelines("%s  \n" %(word))
    f.close()

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path',  type=str)
    parser.add_argument('output_path', type=str)
    return parser.parse_args()

def main():
    args = get_args()
    img2md(args.input_path, args.output_path)

if __name__ == "__main__":
    main()
