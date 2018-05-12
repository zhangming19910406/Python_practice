#! /usr/bin/env
# -*- coding: utf-8 -*-

import itchat
import io
import jieba
import re
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt

RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
def strip_emoji(text):
    return RE_EMOJI.sub(r'', text)

def parse_signature():
    itchat.login()
    siglist = []
    friends = itchat.get_friends(update=True)[1:]
    for friend in friends:
        signature = strip_emoji(friend['Signature'].strip().replace('span', '').replace('class', '').replace("emoji", ""))
        rep = re.compile('1f\d+\w*|[<>/=]')
        signature = rep.sub('', signature)
        siglist.append(signature)
    text = ''.join(siglist)
    with io.open('text.txt', 'a', encoding='utf-8') as f:
        wordlist = jieba.cut(text, cut_all=True)
        word_space_split = " ".join(wordlist)
        f.write(word_space_split)
        f.close()

def draw_signature():
    text = open('text.txt', encoding='utf-8').read()
    # import pdb
    # pdb.set_trace()
    coloring = np.array(Image.open('iron_man.jpg'))
    my_wordcloud = WordCloud(
        background_color="white",
        max_words=2000,
        mask=coloring,
        max_font_size=60,
        random_state=42,
        scale=2,
        font_path="DroidSansFallbackFull.ttf",
        )
    # my_wordcloud = WordCloud(max_words=2000)
    my_wordcloud.generate(text)
    my_wordcloud.to_file('signature_iron_man.png')

    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")


if __name__ == '__main__':
    if not os.path.isfile('text.txt'):
        parse_signature()
    draw_signature()
