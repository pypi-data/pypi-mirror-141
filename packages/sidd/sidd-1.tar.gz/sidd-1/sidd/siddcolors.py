# siddcolors.py>

import numpy as np

def FrequentColor(img):
    '''
    Performs an exact comparison of 2 images. This does not resize and only looks for exact matches. Use CompareImageProbability() if comparing 2 images that are not the same resolution. \r\n
    \r\n
    Parameters
    ------------------------
    image : []
        The image retval.

    \r\n
    Returns
    ------------------------ \r\n
    array[int]
        RGB value of most requent color. \r\n
    '''
    colors, count = np.unique(np.vstack(img), return_counts=True, axis=0)
    sorted_by_freq = colors[np.argsort(count)]
    return sorted_by_freq[0]


def ClosestColor(color, list_of_colors) -> list[int]:
    '''
    Compares @color with list_of_colors \r\n
    \r\n
    Parameters
    ------------------------
    color : list[int]
        The color value.

    \r\n
    Returns
    ------------------------ \r\n
    list[int]
        Returns closest color from list_of_colors. \r\n
    '''
    _colors = np.array(list_of_colors)
    _color = np.array(color)
    distances = np.sqrt(np.sum((_colors-_color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = _colors[index_of_smallest]
    return smallest_distance[0]