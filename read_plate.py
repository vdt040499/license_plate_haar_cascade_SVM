
import cv2
import Preprocess
import detect
import handlehalfofplate
import numpy as np
import time
from lib_detection import load_model, detect_lp, im2single

# Ham sap xep contour tu trai sang phai
def sort_contours(cnts):

    reverse = False
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts

# Dinh nghia cac ky tu tren bien so
char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ'

# Ham fine tune bien so, loai bo cac ki tu khong hop ly
def fine_tune(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString


# Cau hinh tham so cho model SVM
digit_w = 30 # Kich thuoc ki tu
digit_h = 60 # Kich thuoc ki tu
model_svm = cv2.ml.SVM_load('svm.xml')

# Đường dẫn ảnh
img_path = "test/xemay.jpg"

# Đọc file ảnh
# img = cv2.imread("Plate_Data/0478.jpg")
# img = cv2.imread(img_path)

# Đường dẫn video hoặc webcam
vid = cv2.VideoCapture(0)
# vid = cv2.VideoCapture("test/VID_plate_3_cut.mp4")
text_plate = ''
plateNumberDict = {}

# Đọc video
while True:
    return_value, frame = vid.read()
    if return_value:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    else:
        print('Video has ended or failed, try a different video format!')
        break

    start_time = time.time()

    plate_upper, plate_lower = detect.detect(frame)

    if plate_lower.size != 0 and plate_upper.size != 0:
        upper_text = ""

        #Xử lí nửa trên biển số
        upper_text = handlehalfofplate.handle(plate_upper)
        print ("Upper_Text = " + upper_text)

        #Xử lí nửa biển dưới
        lower_text = handlehalfofplate.handle(plate_lower)
        print ("Lower_text = " + lower_text)

        if len(upper_text) == 4 and (len(lower_text) == 4 or len(lower_text) == 5):
                # check char at index 2 is character
                if ord(upper_text[2]) > 64 and ord(upper_text[2]) < 91:
                    if (ord(upper_text[0]) > 47 and ord(upper_text[0]) < 58) and (ord(upper_text[1]) > 47 and ord(upper_text[1]) < 58) and (ord(upper_text[3]) > 47 and ord(upper_text[3]) < 58):
                        if len(lower_text) == 4:
                            print("Bằng 4")
                            if (ord(lower_text[0]) > 47 and ord(lower_text[0]) < 58) and (ord(lower_text[1]) > 47 and ord(lower_text[1]) < 58) and (ord(lower_text[2]) > 47 and ord(lower_text[2]) < 58) and (ord(lower_text[3]) > 47 and ord(lower_text[3]) < 58):
                                text_plate = upper_text + " " + lower_text
                                if text_plate in plateNumberDict.keys():
                                    plateNumberDict[str(text_plate)] += 1
                                else:
                                    plateNumberDict[str(text_plate)] = 1
                        if len(lower_text) == 5:
                            print("Bằng 5")
                            if (ord(lower_text[0]) > 47 and ord(lower_text[0]) < 58) and (ord(lower_text[1]) > 47 and ord(lower_text[1]) < 58) and (ord(lower_text[2]) > 47 and ord(lower_text[2]) < 58) and (ord(lower_text[3]) > 47 and ord(lower_text[3]) < 58) and (ord(lower_text[4]) > 47 and ord(lower_text[4]) < 58):
                                text_plate = upper_text + " " + lower_text
                                if text_plate in plateNumberDict.keys():
                                    plateNumberDict[str(text_plate)] += 1
                                else:
                                    plateNumberDict[str(text_plate)] = 1

    if not not bool(plateNumberDict):
        print("Dict: " + str(plateNumberDict))
        keyMax = max(plateNumberDict, key=plateNumberDict.get)
        print("KeyMax: " + str(keyMax))
        if plateNumberDict[keyMax] > 4:
            file = open("temp.txt", "w")
            file.write(keyMax + "-" + str(plateNumberDict[keyMax]))
            file.close()
            frame = cv2.putText(frame, keyMax + " XIN MOI QUET THE", (20, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    fps = 1.0 / (time.time() - start_time)
    print("FPS: %.2f" % fps)
    result = np.asarray(frame)
    cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
    result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("result", result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()