import cv2

img1 = cv2.imread('computer_vision/images/img1.png')
img2 = cv2.imread('computer_vision/images/img2.png')

# Get the dimensions of img1
height, width, _ = img1.shape

# Resize img2 to match the dimensions of img1
img2 = cv2.resize(img2, (width, height))

dst = cv2.addWeighted(img1, 0.3, img2, 0.7, 0)
cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()