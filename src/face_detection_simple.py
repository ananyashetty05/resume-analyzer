import cv2

# Get image and cascade names
imagePath = "/Users/ananyashetty/Downloads/PHOTO-2024-01-07-14-56-08.jpg"
cascPath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
if image is None:
    print("Error: Could not load image")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print(f"Image loaded: {image.shape[1]}x{image.shape[0]} pixels")

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags=cv2.CASCADE_SCALE_IMAGE
)

print("Found {0} faces!".format(len(faces)))

# Print face coordinates
for i, (x, y, w, h) in enumerate(faces):
    print(f"Face {i+1}: Position({x}, {y}), Size({w}x{h})")
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(image, f"Face {i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display in OpenCV window
cv2.imshow(f"Detected {len(faces)} Faces", image)
print("Press any key to close the window...")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Detection complete!")