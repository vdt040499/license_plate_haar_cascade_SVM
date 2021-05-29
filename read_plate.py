
import cv2
import time
import detect
import difflib
import save_temp
import preprocess
import check_plate
import numpy as np
import handle_halfofplate
from lib_detection import load_model, detect_lp, im2single

# Define characters on plate number
char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ'

# Parameter configuration for SVM model
digit_w = 30 # Characters' width
digit_h = 60 # Characters' height
model_svm = cv2.ml.SVM_load('svm.xml')

# Init status and variables
process = open("process.txt", "w")
process.write("DETECTING")
process.close()
process = open("preplate.txt", "w")
process.write("noplate")
process.close()
text_plate = '' # Current plate text
global plateNumberDict 
plateNumberDict = {} # Curent plate list
vid = cv2.VideoCapture("test/video2.h264")

# Sort contour from left to right
def sort_contours(cnts):
    reverse = False
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts

# Fine tune number plate => remove improper characters
def fine_tune(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString

# Read video
while True:
    return_value, frame = vid.read()
    if return_value:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        temp_frame = frame

        # Modify the frame size => Optimize the FPS
        scale_percent = 40 # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)     
        temp_frame = frame 
    else:
        print('Video has ended or failed, try a different video format!')
        break

    start_time = time.time()

    # Detect plate
    plate_upper, plate_lower = detect.detect(frame)
    if plate_lower.size != 0 and plate_upper.size != 0:
        upper_text = handle_halfofplate.handle(plate_upper)
        lower_text = handle_halfofplate.handle(plate_lower)
        text_plate = str(upper_text) + " " + str(lower_text)

        if (check_plate.check_plate(upper_text, lower_text)):
            if (check_plate.check_four_chars(lower_text)):
                save_temp.save_temp(plateNumberDict, text_plate)
            if (check_plate.check_five_chars(lower_text)):
                save_temp.save_temp(plateNumberDict, text_plate)

    if str(text_plate) == '' and len(plateNumberDict) == 0:
        plateNumberDict.clear()
    text_plate = ''

    plateNumberDict = dict(sorted(plateNumberDict.items(), key=lambda item: item[1], reverse=True))
    print('current Dict: ', str(plateNumberDict))

    process = open("process.txt", "r")
    if not not bool (plateNumberDict):
        keyMax = max(plateNumberDict, key=plateNumberDict.get)
        if (process.read() == 'DETECTING' and int(plateNumberDict[keyMax]) > 1 and len(plateNumberDict) != 0):
            frame = cv2.putText(frame, "MOI QUET MA", (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    if (process.read() == 'DONE'):
        frame = cv2.putText(frame, "MOI XE QUA", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    fps = 1.0 / (time.time() - start_time)
    print("FPS: %.2f" % fps)
    result = np.asarray(frame)
    cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
    result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("result", result)
    print('------------------------------------------------------------------------------------------------------------')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()