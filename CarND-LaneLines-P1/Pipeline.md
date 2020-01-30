# **Finding Lane Lines on the Road** 
----
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)



**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)


[color]: ./process/colorselect.png "colorselect"
[origin]: ./process/original.png "origin"
[grayscale]: ./process/grayscale.png "grayscale"
[Gussian]: ./process/gussian_blur.png "blur"
[edge]: ./process/edges.png "edges"
[masked]: ./process/masked_edges.png "masked"
[hough]: ./process/hough_line.png "hough"

----

### Reflection

### 1. My pipeline consisted of 5 steps.


   ![Alt Text][origin]
   
   ![Alt Text][color]
   
   ![Alt Text][grayscale]
   
   ![Alt Text][gussian]
   
   ![Alt Text][edge]
   
   ![Alt Text][masked]
   
   ![Alt Text][hough]
   
  - Selected the yellow and white collor from the original images, by setting the rgbthreshold [220,180,0]
  - I converted the images to grayscale using the helper function with `grayscale`.
  - Degined a kernel size of 5 to make a Gaussian blurring to the grayscale image. This is mainly to avoid the noise and make the image more clearly.
  - Used the helper function `canny` to detect the edge of the grayscale image.
  - Used the region_of_interest fucntion to only consider pixels for color selection in the region where I expect to find the lane lines.
  - Implenmented Hough Transformation to find lines.
  - Implentmented to the video.

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by: 

  - Used the slope and the location of a single line to decide whther it is on the left or on the right.
  - Find the middle value of x axis, set the limit to make sure that the line from different side will not crossover
  - Weighted the slope and choose the endpoint of the lane lines
  - Extend the lane lines to make it look normally
  - Draw the lane lines



### 2. Identify potential shortcomings with your current pipeline


The challenge part I faced in this project is that when I set the threshold too high, the image all black out, but if I set the threshold too small, the image contained a lot of noise and make the lines inaccurate. Another shortcoming could be the shade. If the lines under the shadow, they would be hardly detected. 
