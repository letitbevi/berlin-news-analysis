#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
import nltk
import numpy as np
from matplotlib import pyplot as plt
plt.style.use('ggplot')

def collect_news_tags(news):
    """collect news from the data folder"""
    year = news['results'][0]['publicationDate'][:4]
    print (year)
    tags_nested = [article['tags'] for article in news['results']]
    tags_flat = [tag for sublist in tags_nested for tag in sublist]
    tags_fdist = nltk.FreqDist(tags_flat)
    print ('Top 5 common tags and its frequencey: \n{}'.format(tags_fdist.most_common(5)))
    common_tags = tags_fdist.most_common(20) ### ex. [('Culture', 471), ('World news', 325), ('Football', 318), ...]
    return common_tags

def collect_fig_title(news):
    year = news['results'][0]['publicationDate'][:4]
    fig_title = '{} Berlin Top 20 News Categories'.format(year)
    return fig_title

def plot_trending(tags_n_freq, fig_title):
    """Plot top tags in each year"""
    
    ### plot x, y
    tag_labels = [tag for tag, _ in tags_n_freq]
    x = np.array(range(20))
    y = [freq for _, freq in tags_n_freq]
    
    plt.xticks(x, tag_labels, rotation=45, ha='right')

    plt.bar(x, y, color='blue', alpha=0.6, align='center')
    plt.ylabel('Frequency')
    plt.title(fig_title)
    plt.tight_layout() ### to make room for labels
    
    ### save fig
    if not os.path.exists('fig'):
        os.makedirs('fig')
    else: pass
    fig = plt.gcf()
    fig.savefig('fig/{}'.format(re.sub(' ', '_', fig_title)))
    plt.close(fig)

def main():
    if not os.path.exists('data'):
        os.makedirs('data')
    else: pass
    paths = glob.glob("data/*.json")
    for path in paths:
        with open(path) as f:
            berlin_news_one_year = json.load(f)
            common_tags = collect_news_tags(berlin_news_one_year)
            title = collect_fig_title(berlin_news_one_year)
            plot_trending(common_tags, title)

if __name__ == '__main__':
    main()
