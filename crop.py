#!/usr/bin/env -S uv run -q -s
# /// script
# requires-python = "==3.13.3"
# dependencies = [
#     "opencv-python==4.11.0.86",
#     "opencv-contrib-python==4.11.0.86",
#     "numpy==2.2.4",
# ]
# ///

import cv2
import numpy as np
import argparse
import os

# Parse arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to scanned image')
args = vars(ap.parse_args())

# Prepare filenames
input_image = args['image']
input_image_name, input_image_ext = os.path.splitext(input_image)
output_image = f"{input_image_name}_crop{input_image_ext}"

# Load the image
image = cv2.imread(input_image)
if image is None:
    raise ValueError(f"Could not load image: {input_image}")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply slight blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use edge detection
edges = cv2.Canny(blurred, 30, 100)

# Morphological closing to connect broken edges
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# Find contours
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if not contours:
    raise ValueError("No contours found!")

# Get the largest contour assuming it's the photo + white border
c = max(contours, key=cv2.contourArea)

# Fit a rotated rectangle
rot_rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rot_rect)
box = box.astype(np.int32)

# Get the angle to deskew
angle = rot_rect[2]
if angle < -45:
    angle += 90

# Rotate the image to deskew
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# Transform the box points to match the rotated image
rotated_box = cv2.transform(np.array([box]), M)[0]
x, y, w, h = cv2.boundingRect(rotated_box)

# Crop using the transformed bounding box
final = rotated[y:y+h, x:x+w]

# Save the result
cv2.imwrite(output_image, final)
print(f"Saved cropped image with border to: {output_image}")

