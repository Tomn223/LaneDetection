IMAGE_NUM = 3 # which image to read from images folder 
CANNY_LOW_THRESHOLD = 50 # lower threshold for canny edge detection (deriv is lower than, throw away)
CANNY_HIGH_THRESHOLD = 150 # upper threshold for canny edge detection (deriv is hgiher than, keep)
ROAD_IMAGE_RATIO = 0.5 # road/lane lines generally in bottom half of image
SLOPE_DIFF_THRESHOLD = 0.3 # max diff of slopes for lane line to be considered same, 0.3 seemed to work well
HOUGH_MIN_LINE_LEN = 100 # min edge line length for line to be found from hough transform
HOUGH_MAX_LINE_GAP = 5 # max length of break in edge line segments to be bridged
BG_IMAGE_OPACITY = 0.7 # opacity of background driving image