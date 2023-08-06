# siddcompares.py>

import cv2

def CompareImageExact(original, dupe) -> bool:
    '''
    Performs an exact comparison of 2 images. This does not resize and only looks for exact matches. Use CompareImageProbability() if comparing 2 images that are not the same resolution. \r\n
    \r\n
    Parameters
    ------------------------
    original : []
        The original image retval.
    dupe : []
        The potental duplicate image retval.

    \r\n
    Returns
    ------------------------ \r\n
    bool
        True if exact match. \r\n
    '''
    if original.shape[:2] == dupe.shape[:2]:
        difference = cv2.subtract(original, dupe)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            return True
        else:
            return False
    else:
        return False
        
        
def CompareImageProbability(original, dupe, prob_threshold = .1) -> bool:
    '''
    Performs probabalistic comparison of 2 images. To change probability threshold, set prob_threshold (default is .1). \r\n
    \r\n
    Parameters
    ------------------------
    original : []
        The original image retval.
    dupe : []
        The potental duplicate image retval.

    \r\n
    Returns
    ------------------------ \r\n
    bool
        True if match. Threshold based off prob_match property. \r\n
    '''
    original_img_hist = cv2.calcHist([original], [0], None, [256], [0, 256])
    dupe_img_hist = cv2.calcHist([dupe], [0], None, [256], [0, 256])
    
    img_hist_diff = cv2.compareHist(original_img_hist, dupe_img_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_prob_match = cv2.matchTemplate(original_img_hist, dupe_img_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_temp_diff = 1 - img_prob_match
    
    diff = (img_hist_diff / 10) + img_temp_diff
    if diff < prob_threshold:
        return True
    else:
        return False    


def CompareImage(original, dupe, comp_method = CompareImageProbability) -> bool:
    '''
    Wrapper comparison function. Can use this instead of calling CompareImageExact or CompareImageProbability. Accepts either function as a parameter.
    \r\n
    Parameters
    ------------------------
    original : str
        The original image full file path.
    dupe : []
        The potental duplicate image full file path.
    comp_method:
        Use CompareImageProbability (default) or CompareImageExact

    \r\n
    Returns
    ------------------------ \r\n
    bool
        True if exact match. \r\n
    '''
    original_img = cv2.imread(original)
    dupe_img = cv2.imread(dupe)
    return comp_method(original_img, dupe_img)