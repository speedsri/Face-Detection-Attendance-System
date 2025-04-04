# Default profile image for employees
import cv2
import numpy as np
import os

# Create a simple default avatar
img_size = 400
img = np.ones((img_size, img_size, 3), dtype=np.uint8) * 240  # Light gray background

# Draw a silhouette
center = (img_size // 2, img_size // 2 - 30)
head_radius = img_size // 5
cv2.circle(img, center, head_radius, (200, 200, 200), -1)  # Head

# Body
body_pts = np.array([
    [center[0] - head_radius, center[1] + head_radius // 2],
    [center[0] + head_radius, center[1] + head_radius // 2],
    [center[0] + head_radius + 20, center[1] + head_radius * 3],
    [center[0] - head_radius - 20, center[1] + head_radius * 3]
])
cv2.fillPoly(img, [body_pts], (200, 200, 200))

# Save the image
output_path = 'static/images/default-avatar.png'
cv2.imwrite(output_path, img)

print(f"Default avatar created at {output_path}")
