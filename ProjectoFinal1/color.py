import cv2
import numpy as np

# Choose HSV color to visualize
hsv_color = np.uint8([[[40, 100, 100]]])   # Example: bright green (H=60)

# Convert HSV → BGR so OpenCV can display it
bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)

# Create an image filled with that color
img = np.full((300, 300, 3), bgr_color[0][0], dtype=np.uint8)

# Show the figure
cv2.imshow("HSV Color", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
