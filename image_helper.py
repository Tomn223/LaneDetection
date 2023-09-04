import cv2
import numpy as np
import constants

def showAndDestroy(image):
    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# return mask for only getting bottom ROAD_IMAGE_RATIO of image
def region_of_interest(image):
    height = int(image.shape[0])
    width = int(image.shape[1])

    upperLeft = (0, int((1-constants.ROAD_IMAGE_RATIO)*height))
    lowerRight = (width, height)

    mask = np.zeros_like(image)

    cv2.rectangle(mask, upperLeft, lowerRight, 255, -1)

    return mask