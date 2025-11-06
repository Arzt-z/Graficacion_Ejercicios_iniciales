import cv2 as cv

img=cv.imread('img01.jpg')

cv.imshow('img',img)

cv.waitKey()

cv.destroyallwindows()