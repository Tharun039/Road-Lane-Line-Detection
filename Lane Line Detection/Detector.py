# Import necessary libraries
import matplotlib.pylab as plt
import cv2
import numpy as np

# Define a function to identify the region of interest in an image
def region_of_interest(img, vertices):
    # Create a mask of zeros with the same dimensions as the input image
    mask = np.zeros_like(img)
    # Set the color for the mask to match the input image
    match_mask_color = 255
    # Fill the region of interest defined by 'vertices' with the specified color
    cv2.fillPoly(mask, vertices, match_mask_color)
    # Apply the mask to the input image using bitwise AND operation
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# Define a function to draw lines on an image
def draw_the_lines(img, lines):
    # Create a copy of the input image
    img = np.copy(img)
    # Create a blank image with the same dimensions as the input image
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    # Iterate over the lines detected in the image
    for line in lines:
        for x1, y1, x2, y2 in line:
            # Draw a line on the blank image
            cv2.line(blank_image, (x1,y1), (x2,y2), (0, 255, 0), thickness=10)

    # Combine the original image and the blank image using weighted addition
    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img

# Define a function to process each frame of a video
def process(image):
    # Print the dimensions of the input image
    print(image.shape)
    # Get the height and width of the input image
    height = image.shape[0]
    width = image.shape[1]
    # Define the vertices of the region of interest
    region_of_interest_vertices = [
        (0, height),
        (width/2, height/2),
        (width, height)
    ]
    # Convert the input image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Apply Canny edge detection to the grayscale image
    canny_image = cv2.Canny(gray_image, 100, 120)
    # Extract the region of interest from the Canny image
    cropped_image = region_of_interest(canny_image,
                    np.array([region_of_interest_vertices], np.int32),)
    # Detect lines in the cropped image using Hough transform
    lines = cv2.HoughLinesP(cropped_image,
                            rho=2,
                            theta=np.pi/180,
                            threshold=50,
                            lines=np.array([]),
                            minLineLength=40,
                            maxLineGap=100)
    # Draw lines on the original image
    image_with_lines = draw_the_lines(image, lines)
    return image_with_lines

# Open a video file for processing
cap = cv2.VideoCapture('test.mp4')

# Loop through each frame of the video
while cap.isOpened():
    # Read a frame from the video
    ret, frame = cap.read()
    # Process the frame
    frame = process(frame)
    # Display the processed frame
    cv2.imshow('frame', frame)
    # Check if the user pressed 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
