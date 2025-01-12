from novel_toy_tools.implementations.rendition_statistics_cv2 import RenditionStatisticsCv2
import cv2

IMAGE_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/Phoo/rendition_Phoo_25508_2021-01-08_009_Exp2B_30.2.png"

image_rendition = RenditionStatisticsCv2(IMAGE_PATH)
cv2.imshow('base image', image_rendition.image)
cv2.imshow('binarized image', image_rendition.image_binarized)
contours = cv2.drawContours(image_rendition.image, image_rendition.image_contours, -1, (0,255,0), 3)
cv2.imshow('contours', contours)

stats = image_rendition.get_rendition_statistics()
line_image = image_rendition.image
point1, point2 = stats['longest edge'][1:]
cv2.line(line_image, point1, point2, color=(0, 0, 255))

cv2.imshow('longest line', line_image)

cv2.waitKey(0)
cv2.destroyAllWindows()