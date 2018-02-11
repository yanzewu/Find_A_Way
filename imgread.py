import numpy as np
import cv2  

def read_img(img):
    """ Recognize image to matrix object.
        img: 2D np.array (0-255)
        returns: 2D np.array. 0==> empty, 1==> block
            xcenters: absolute position of x centers at image;
            ycenters: absolute position of y centers at image;
    """

    x1, y1, x2, y2  = locate_boundary(img, 225) # upleft, downright

    img_rec = img[y1:y2, x1:x2]

    xcenters = locate_centers(img_rec[5], 225)
    ycenters = locate_centers(img_rec[:, 5].flatten(), 225)

    ret = np.zeros((len(xcenters), len(ycenters)), dtype=int)
    for i in range(len(xcenters)):
        for j in range(len(ycenters)):
            ret[i, j] = classify_dot(img_rec[ycenters[j], xcenters[i]], 160, 80)

    return ret, xcenters + x1, ycenters + y1 


def locate_boundary(img, cutoff):

    # we assume center of image is in the region

    yave = np.min(img, axis=1) < cutoff 
    haspoint = np.where(yave)[0]
    
    yi = len(haspoint)//2
    interval = None 
    while yi < len(haspoint):
        if haspoint[yi+1] - haspoint[yi] > 5:
            interval = haspoint[yi+1] - haspoint[yi]
            break 
        yi += 1

    y1i = y2i = len(haspoint) // 2
    y1 = y2 = x1 = x2 = None 

    while y1i > 0:
        if haspoint[y1i] - haspoint[y1i-1] > interval * 1.2:
            break
        y1i -= 1
    while y2i < len(haspoint):
        if haspoint[y2i+1] - haspoint[y2i] > interval * 1.2:
            break
        y2i += 1

    x1, y1, x2, y2 = 0, haspoint[y1i], img.shape[1]-1, haspoint[y2i]

    # adjust border

    while y1 > 0:
        if np.min(img[y1]) < cutoff:
            y1 -= 1
        else:
            break
    while y2 < len(img):
        if np.min(img[y2]) < cutoff:
            y2 += 1
        else:
            break
    while x1 < x2:
        if np.min(img[y1:y2, x1]) > cutoff:
            x1 += 1
        else:
            break
    while x2 > x1:
        if np.min(img[y1:y2, x2]) > cutoff:
            x2 -= 1
        else:
            break

    return x1, y1, x2, y2


def locate_centers(line, cutoff):
    
    centers = []
    seg_tmp = []

    for i in range(len(line)):
        if line[i] > cutoff and seg_tmp:
            centers.append(int(np.average(seg_tmp)))
            seg_tmp.clear()
        elif line[i] < cutoff:
            seg_tmp.append(i)
            
    return np.array(centers)

def classify_dot(val, cut_hi, cut_lo):
    if val > cut_hi:
        return 0
    elif val > cut_lo:
        return 2
    else:
        return 1