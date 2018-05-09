#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import itchat
import re
import io
from os import path
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
import os
from matplotlib import pyplot as plt

def draw(datas):
    data = []
    for key in datas.keys():
        data.append(datas[key])
    # import pdb
    # pdb.set_trace()
    fig, ax = plt.subplots()
    ind = np.arange(1, 4)
    pm, pc, pn = plt.bar(ind, data)

    pm.set_facecolor('r')
    pc.set_facecolor('g')
    pn.set_facecolor('b')
    ax.set_xticks(ind)
    ax.set_xticklabels(['female', 'male', 'don\'t know'])
    ax.set_ylim([0, 250])
    ax.set_ylabel('number')
    ax.set_title('sex')
    ax.set_title('Gender of zhangming\'s friends')
    plt.show()

def parse_friends():
    itchat.login()
    text = dict()
    friends = itchat.get_friends(update=True)[0:]
    # print(friends)
    male = "male"
    female = "female"
    other = "other"
    for friend in friends[1:]:
        sex = friend['Sex']
        if sex == 1:
            text[male] = text.get(male, 0) + 1  # if it is Nan, it will be ZERO.
        elif sex == 2:
            text[female] = text.get(female, 0) + 1
        else:
            text[other] = text.get(other, 0) + 1
    total = len(friends[1:])
    print("男性好友： %.2f%%" % (float(text[male]) / total * 100) + "\n" +
          "女性好友： %.2f%%" % (float(text[female]) / total * 100) + "\n" +
          "不明性别好友： %.2f%%" % (float(text[other]) / total * 100))
    draw(text)

parse_friends()
