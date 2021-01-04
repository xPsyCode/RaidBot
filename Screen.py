from capture import win_cap
import cv2
import time
from PIL import Image, ImageGrab

crip = (751,611,854,630)
x = 0
while True:
    cv2.imshow("Img", win_cap())
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
    if key == ord('m'):
        x += 1
        cv2.imwrite("img2.jpg", win_cap())







