import cv2
import numpy as np
import constants

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    for x1, y1, x2, y2 in lines:
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

    return line_image

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*constants.ROAD_IMAGE_RATIO)
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    lane_lines = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        foundExistingLaneLine = False
        for lane_line in lane_lines:
            # separate lines into buckets of lines with similar slope
            if abs(lane_line[0][0] - slope) < constants.SLOPE_DIFF_THRESHOLD:
                lane_line.append((slope, intercept))
                foundExistingLaneLine = True
                break
        if not foundExistingLaneLine:
            lane_lines.append([(slope, intercept)])

    lane_line_coords = []
    for line in lane_lines:
        line_average = np.average(line, axis=0)
        line_coords = make_coordinates(image, line_average)
        lane_line_coords.append(line_coords)
    return np.array(lane_line_coords)