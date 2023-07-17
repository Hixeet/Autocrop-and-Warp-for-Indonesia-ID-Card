import numpy as np
import cv2

def auto_crop_blue(image):
    # Split the image into blue, green, and red channels
    b, g, r = cv2.split(image)

    # Thresholding the blue channel
    _, blue_threshold = cv2.threshold(b, 110, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(blue_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (blue region)
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a mask of the largest contour
    mask = np.zeros_like(b)
    cv2.drawContours(mask, [largest_contour], 0, 255, -1)

    # Apply the mask to the original image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Find the bounding box of the blue region
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Crop the image based on the bounding box
    cropped_image = result[y:y+h, x:x+w]

    #cv2.imwrite("cropped image4.jpg", cropped_image)

    return cropped_image

# Read the image
img = cv2.imread("5.jpeg")

# Auto crop the image to extract the blue region
cropped_img = auto_crop_blue(img)

# Resize the cropped image
resized_img = cv2.resize(cropped_img, (780, 600))

# Convert the images to grayscale
resized_gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
template_gray = cv2.imread('KTP_.jpg', 0)
template_resized = cv2.resize(template_gray, (0, 0), fx=0.9, fy=1.1)

h, w = template_resized.shape

methods = [cv2.TM_CCORR]

for method in methods:
    img2 = resized_gray.copy()

    result = cv2.matchTemplate(img2, template_resized, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    cv2.rectangle(resized_img, location, (location[0] + w, location[1] + h), 255, 5)
    cv2.imshow('Match', resized_img)
    print(location)
    cv2.waitKey(0)

    # Define the corner points of the matched region
    pts1 = np.float32([[12, 12], [730, 15], [4, 640], [750, 640]])
    pts2 = np.float32([[0, 0], [860, 0], [0, 620], [860, 620]])

    matrix = cv2.getPerspectiveTransform(pts1,pts2)

    final = cv2.warpPerspective(resized_img, matrix, (860, 560))

    # Show the warped image
    cv2.imwrite('Warped Image.jpg', final)
    cv2.imshow('Warped Image', final)
    cv2.waitKey(0)

cv2.destroyAllWindows()
