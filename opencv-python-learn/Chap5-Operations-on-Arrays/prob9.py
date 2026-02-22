import cv2, numpy as np


image = np.random.randint(0, 255, (3,6), dtype=np.uint8)
avg_row = cv2.reduce(image, 0, cv2.REDUCE_AVG)
avg_col = cv2.reduce(image, 1, cv2.REDUCE_AVG)
print("image : \n", image)
print("image - row avg : \n",avg_row)
print("image - col avg : \n",avg_col)
