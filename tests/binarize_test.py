from novel_toy_tools.implementations.rendition_statistics_cv2 import RenditionStatisticsCv2
import cv2
import os

IMAGE_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/FrogMan/rendition_FrogMan_25532_2017-07-04_152_Exp2A_30.6.png"
IMAGE_PATH2 = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/HoleBlock2QuaterBlocks/rendition_HoleBlock2QuaterBlocks_25508_2021-01-08_019_Exp2B_30.2.png"
IMAGE_PATH3 = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/BlockGiraffe/rendition_BlockGiraffe_25601_2017-11-25_059_Exp2B_25.8.png"
IMAGE_PATH4 = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/BowlingTrapWithCookie/rendition_BowlingTrapWithCookie_25532_2017-07-04_016_Exp2A_30.6.png"
IMAGE_PATH5 = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/LightBulbStickx2/rendition_LightBulbStickx2_25532_2017-07-04_051_Exp2A_30.6.png"
IMAGE_PATH6 = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/Phoo/rendition_Phoo_25508_2021-01-08_012_Exp2B_30.2.png"
IMAGE_PATH7 = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/PrickleBallPointy/rendition_PrickleBallPointy_25508_2021-01-08_005_Exp2B_30.2.png"
IMAGE_PATH8 = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/XmasTreeBallyWhirl/rendition_XmasTreeBallyWhirl_25802_2021-01-08_012_Exp2A_23.1.png"

OUT_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/notebooks/charts"

paths = [IMAGE_PATH, IMAGE_PATH2, IMAGE_PATH3, IMAGE_PATH4, IMAGE_PATH5, IMAGE_PATH6, IMAGE_PATH7, IMAGE_PATH8]

i = 0
for image in paths:
    image_rendition = RenditionStatisticsCv2(image)
    stats = image_rendition.get_rendition_statistics()
    line_image = image_rendition.image
    point1, point2 = stats['longest edge'][1:]
    cv2.line(line_image, point1, point2, color=(0, 0, 255))
    filename = os.path.join(OUT_PATH, f"image{i}.png")
    cv2.imwrite(filename=filename, img=line_image)
    i += 1