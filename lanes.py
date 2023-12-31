import cv2
import numpy as np
import os
import constants
from image_helper import region_of_interest, showAndDestroy, saveImageToFolder
from lines_helper import average_slope_intercept, display_lines

img = cv2.imread(f"images/{constants.IMAGE_NUM}.jpg")
saveImageToFolder("initial", img, "steps")
# showAndDestroy(gray_img)

lane_img = np.copy(img)

gray_img = cv2.cvtColor(lane_img, cv2.COLOR_BGR2GRAY)
saveImageToFolder("gray", gray_img, "steps")
# showAndDestroy(gray_img)

blur_img = cv2.GaussianBlur(gray_img, (5,5), 0)
saveImageToFolder("gaussian", blur_img, "steps")
# showAndDestroy(blur_img)

canny_img = cv2.Canny(blur_img, constants.CANNY_LOW_THRESHOLD, constants.CANNY_HIGH_THRESHOLD)
saveImageToFolder("canny", canny_img, "steps")
# showAndDestroy(canny_img)

mask = region_of_interest(canny_img)
saveImageToFolder("mask", mask, "steps")
# showAndDestroy(mask)

roi_img = cv2.bitwise_and(canny_img, mask)
saveImageToFolder("roi", roi_img, "steps")
# showAndDestroy(roi_img)

lines = cv2.HoughLinesP(roi_img, 2, np.pi/180, 100, np.array([]), minLineLength=constants.HOUGH_MIN_LINE_LEN, maxLineGap=constants.HOUGH_MAX_LINE_GAP)

# below requires diplay to be modified to reshape np array
# all_line_img = display_lines(lane_img, lines)
# lane_line_img = cv2.addWeighted(lane_img, 0.7, all_line_img, 1, 1)
# saveImageToFolder("lane_lines_pre", lane_line_img, "steps")
# showAndDestroy(lane_line_img)

avg_lines_coords, avg_lines_params = average_slope_intercept(lane_img, lines)
avg_line_img = display_lines(lane_img, avg_lines_coords)
lane_line_img = cv2.addWeighted(lane_img, constants.BG_IMG_OPACITY, avg_line_img, 1, 1)
saveImageToFolder("lane_lines", lane_line_img, "steps")
# showAndDestroy(lane_line_img)

car_classifier = cv2.CascadeClassifier("cars.xml")

car_boxes = car_classifier.detectMultiScale(blur_img)

cars_and_lanes_img = lane_line_img

# sort lane lines from left to right (at y = .75*image height)
# this allows us to walk through the lane cutoffs in order to place cars
avg_lines_params = sorted(avg_lines_params, key=lambda param: (lane_img.shape[0]*.75 - param[1]) / param[0])
avg_lines_params = np.array(avg_lines_params)

for i, box in enumerate(car_boxes):
    x, y, w, h = box
    start = (x,y)
    end = (x+w, y+h)

    cars_and_lanes_img = cv2.rectangle(cars_and_lanes_img, start, end, (0,0,255), 1)

    # middle of the base (ie where car touches road)
    mid_x = x + w/2
    bot_y = y + h

    # x = (y-b)/m, gives x coord lane divides for car's y
    lane_cutoffs = (bot_y - avg_lines_params[:,1]) / avg_lines_params[:,0]
    
    lane_num = 0

    while lane_num < len(lane_cutoffs) and mid_x > lane_cutoffs[lane_num]:
        lane_num += 1

    cv2.putText(cars_and_lanes_img, "Lane: " + str(lane_num), (x, y-10), cv2.FONT_HERSHEY_PLAIN, 0.9, (0,255,0), 1)

saveImageToFolder(constants.IMAGE_NUM, cars_and_lanes_img, "results")
showAndDestroy(cars_and_lanes_img)
