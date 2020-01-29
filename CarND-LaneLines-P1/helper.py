import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def colorselect(image, red, green, blue):
    # Grab the x and y size and make a copy of the image
    ysize = image.shape[0]
    xsize = image.shape[1]
    color_select = np.copy(image)
    

    rgb_threshold = [red, green, blue]

    # Do a boolean or with the "|" character to identify
    # pixels below the thresholds
    thresholds = (image[:,:,0] < rgb_threshold[0]) \
            | (image[:,:,1] < rgb_threshold[1]) \
            | (image[:,:,2] < rgb_threshold[2])
    color_select[thresholds] = [0,0,0]
    return color_select

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    
    imshape = img.shape
    half = imshape[1]/2 # x-axis's half
    lengthleft = 0
    lengthright = 0
    slopeleft = 0
    sloperight = 0
    xright_min = 2147483647
    xleft_max = -2147483647
    yright_min = 2147483647
    yleft_min = 2147483647
    for line in lines:
        for x1,y1,x2,y2 in line:
            slope = (y2-y1)/(x2-x1)
            if slope > 0.5 and slope < 0.9 and x1 > half and x2 > half:
                    length = math.sqrt((x2-x1)**2+(y2-y1)**2)
                    lengthright += length
                    sloperight += (slope*length)
                    xright_min= min(xright_min, min(x1,x2))
                    yright_min = min(yright_min, min(y1,y2))
            if slope < -0.5 and slope > -0.8 and x1 < half and x2 < half:
                    length = math.sqrt((x2-x1)**2+(y2-y1)**2)
                    lengthleft += length
                    slopeleft += (slope*length)
                    xleft_max = max(xleft_max, max(x1,x2))
                    yleft_min = min(yleft_min, min(y1,y2))
                
    if lengthright!=0:
        sloperight = sloperight/lengthright
        xright_end = max(min(xright_min,half+70),half+50)
        yright_end = yright_min + sloperight*(xright_end - xright_min)
        xright_start = xright_min - (yright_min - imshape[0])/ sloperight
        cv2.line(img, (int(xright_start), imshape[0]), (int(xright_end), int(yright_end)), color, thickness)
    if lengthleft!=0:
        slopeleft = slopeleft/lengthleft
        xleft_end = max(xleft_max,half-50)
        yleft_end = yleft_min + slopeleft*(xleft_end - xleft_max)
        xleft_start = xleft_max - (yleft_min - imshape[0])/slopeleft
        cv2.line(img, (int(xleft_start), imshape[0]), (int(xleft_end), int(yleft_end)), color, thickness)     
    #cv2.line(image, start_point, end_point, color, thickness)
    
def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)