import cv2
import numpy as np

def detect(img):

    # load classifier
    classifier = cv2.CascadeClassifier("cascade.xml")

    # convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = classifier.detectMultiScale(gray, 1.1, 3)
    print("faces", type(faces))

    # draw rectangles on image for every detected face
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img, (x,y), (x+w,y+h), (455, 0, 0), 4)
        print(x, y, w, h)
    
    #Crop plate
    if type(faces) == tuple:
        if not faces:
            return np.array([]), np.array([]) 
        else:
            cropped = img[y:y+h, x+20:x+w-20]

        #Crop half of plate (top and bottom)
            plate_upper = cropped[0:int(cropped.shape[0]/2), 0:int(cropped.shape[1])]
            plate_lower = cropped[int(cropped.shape[0]/2): int(cropped.shape[0]), 0:int(cropped.shape[1])]

            return plate_upper, plate_lower
    else:
        if faces.size == 0:
            return np.array([]), np.array([]) 
        else:
            cropped = img[y:y+h, x+20:x+w-20]

        #Crop half of plate (top and bottom)
            plate_upper = cropped[0:int(cropped.shape[0]/2), 0:int(cropped.shape[1])]
            plate_lower = cropped[int(cropped.shape[0]/2): int(cropped.shape[0]), 0:int(cropped.shape[1])]

            return plate_upper, plate_lower
