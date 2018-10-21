#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyocr
import pyocr.builders
import cv2
from PIL import Image
import numpy as np

import sys
import os


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


def delwords(img, word_box):
    for box in word_box:
        hight = box.position[1][0] - box.position[0][0]
        width = box.position[1][1] - box.position[0][1]
        white_img = Image.new("L", (hight, width), 255)

        img.paste(white_img, (box.position[0][0], box.position[0][1]))

    return img


def img2figure(img, output_path):
    if(os.path.exists(output_path + "/fig") == False):
        os.mkdir(output_path + "/fig")

    edge = np.asarray(img)
    edge = cv2.cvtColor(edge, cv2.COLOR_BGR2GRAY)
    ret, edge = cv2.threshold(edge, np.average(edge), 255, 0)
    edge = cv2.bitwise_not(edge)
    
    edge, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    fig_pos = []
    figure = np.asarray(img)
    idx = 0

    MINIMUM_FIGURE_SIZE = 100

    for (i, cnt) in enumerate(contours):
        if(hierarchy[0][i][3] != -1): continue

        x,y,w,h = cv2.boundingRect(cnt)
        if w * h < MINIMUM_FIGURE_SIZE: continue

        fig_pos.append([x,y,w,h])
        cv2.imwrite((output_path + "/fig/%d.png" %(idx)), figure[y:y+h, x:x+w])
        idx += 1
    
    return fig_pos


def img2md(input_path, output_path):
    if(os.path.exists(output_path) == False):
        os.mkdir(output_path)
    
    # Load Image
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if(img is None):
        sys.stderr.write("Cannot open file!!")
        exit(1)
    thresh, img = cv2.threshold(img, np.average(img), 255, cv2.THRESH_BINARY)
    
    img = Image.fromarray(np.uint8(img))

    word_box = img2wordbox(img)
    img = delwords(Image.open(input_path), word_box)
    fig_box = img2figure(img, output_path)

    words = []
    for box in word_box:
        words.append(box.content)

    f = open((output_path + "/output.md"), "w")
    word_idx = 0
    figure_idx = 0
    while(word_idx < len(word_box) or figure_idx < len(fig_box)):
        if(word_idx >= len(word_box)):
            f.writelines("![figure %d](fig/%d.png)  \n" %(figure_idx, figure_idx))
            figure_idx += 1
        elif(figure_idx >= len(fig_box)):
            f.writelines("%s  \n" %(word_box[word_idx].content))
            word_idx += 1
        else:
            if(word_box[word_idx].position[0][1] <= fig_box[figure_idx][0]):
                f.writelines("%s  \n" %(word_box[word_idx].content))
                word_idx += 1
            else: 
                f.writelines("![figure %d](fig/%d.png)  \n" %(figure_idx, figure_idx))
                figure_idx += 1
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
