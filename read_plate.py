
import cv2
import Preprocess
import detect
import handlehalfofplate
import numpy as np
import time
import difflib
from lib_detection import load_model, detect_lp, im2single

# Hàm so sánh độ tương đồng biển sô
def plate_similarity(a, b):
    seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
    return seq.ratio()

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
# img_path = "test/xemay.jpg"

# Đọc file ảnh
# img = cv2.imread("Plate_Data/0478.jpg")
# img = cv2.imread(img_path)

# Đường dẫn video hoặc webcam
# vid = cv2.VideoCapture(0)
vid = cv2.VideoCapture("test/video5.h264")

text_plate = '' #biển số trong frame hiện tại
global plateNumberDict
plateNumberDict = {}

# Đọc video
while True:
    return_value, frame = vid.read()
    if return_value:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Thay đổi kích thước frame hình => Tăng FPS
        scale_percent = 40 # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)      
    else:
        print('Video has ended or failed, try a different video format!')
        break

    start_time = time.time()

    # Set số lượng bằng 0 cho biển số sai sau khi gửi request tạo vé
    wrongplate = open("wrongplate.txt", "r")
    wrong_plate = wrongplate.read()
    if str(wrong_plate) in plateNumberDict.keys():
        plateNumberDict[str(wrong_plate)] = 0
        temp = open("temp.txt", "w")
        temp.write("noplate")
        temp.close()

    # Detect biển số
    plate_upper, plate_lower = detect.detect(frame)

    if plate_lower.size != 0 and plate_upper.size != 0:
        #Xử lí nửa trên biển số
        upper_text = handlehalfofplate.handle(plate_upper)

        #Xử lí nửa biển dưới
        lower_text = handlehalfofplate.handle(plate_lower)

        text_plate = str(upper_text) + " " + str(lower_text)

        # Xét điều kiện nửa biển số trên có 4 kí tự, nửa biển số dưới có 4 hoặc 5 kí tự
        if len(upper_text) == 4 and (len(lower_text) == 4 or len(lower_text) == 5):
                # check char at index 2 is character
                if ord(upper_text[2]) > 64 and ord(upper_text[2]) < 91:
                    # Xét điều kiện hai kí tự đầu phải là số
                    if (ord(upper_text[0]) > 47 and ord(upper_text[0]) < 58) and (ord(upper_text[1]) > 47 and ord(upper_text[1]) < 58):
                        
                        if len(lower_text) == 4: # trường hợp số lượng kí tự nửa biển số dưới bẳng 4
                            # Xét điều kiện các kí tự ở nửa dưới biển số bắt buộc phải là số
                            if (ord(lower_text[0]) > 47 and ord(lower_text[0]) < 58) and (ord(lower_text[1]) > 47 and ord(lower_text[1]) < 58) and (ord(lower_text[2]) > 47 and ord(lower_text[2]) < 58) and (ord(lower_text[3]) > 47 and ord(lower_text[3]) < 58):
                                similar_plate_count = 0
                                if len(plateNumberDict) > 0:

                                    # Kiểm tra biển số hiện tại có tương đồng với các biển số trong Dict hay không ?
                                    for plate in plateNumberDict.keys():
                                        # print('plateinarray: ', str(plate))
                                        # print('current: ', text_plate)
                                        # print('simimarity: ', plate_similarity(str(text_plate), str(plate)))
                                        if plate_similarity(str(text_plate), str(plate)) > 0.7:
                                            similar_plate_count += 1
                                    # Nếu không tương đồng 1 trong số biển số sẽ clear Dict
                                    if similar_plate_count != len(plateNumberDict):
                                        plateNumberDict.clear()

                                    # Khi biển số tương đồng với các biển số trong Dict
                                    else:

                                        # Lấy biển số có số lượng lớn nhất trong Dict để so sánh với prePlate
                                        # Nếu = prePlate - biển số đã được tạo vé => chứng tỏ đã tạo vé thành công nên sẽ xóa Dict
                                        # Để thực hiện quá trình detect biển số khác
                                        keyMax = max(plateNumberDict, key=plateNumberDict.get)
                                        pre_plate = open("preplate.txt", "r")
                                        if str(pre_plate) == str(keyMax):
                                            plateNumberDict.clear()

                                        # Nếu không trùng thì lấy biển số đó để đem đi tạo vé (lưu vào temp.txt)
                                        else:
                                            if plateNumberDict[keyMax] > 4:
                                                temp = open("temp.txt", "w")
                                                temp.write(keyMax + "-" + str(plateNumberDict[keyMax]))
                                                temp.close()
                                
                                # Lưu biển số vào Dict
                                if text_plate in plateNumberDict.keys():
                                    plateNumberDict[str(text_plate)] += 1
                                else:
                                    plateNumberDict[str(text_plate)] = 1

                        if len(lower_text) == 5: # trường hợp số lượng kí tự nửa biển số dưới bẳng 5
                            # Xét điều kiện các kí tự ở nửa dưới biển số bắt buộc phải là số
                            if (ord(lower_text[0]) > 47 and ord(lower_text[0]) < 58) and (ord(lower_text[1]) > 47 and ord(lower_text[1]) < 58) and (ord(lower_text[2]) > 47 and ord(lower_text[2]) < 58) and (ord(lower_text[3]) > 47 and ord(lower_text[3]) < 58) and (ord(lower_text[4]) > 47 and ord(lower_text[4]) < 58):
                                similar_plate_count = 0
                                if len(plateNumberDict) > 0:
                                    for plate in plateNumberDict.keys():
                                        if plate_similarity(str(text_plate), str(plate)) > 0.7:
                                            similar_plate_count += 1

                                    if similar_plate_count != len(plateNumberDict):
                                        plateNumberDict.clear()

                                    else:
                                        keyMax = max(plateNumberDict, key=plateNumberDict.get)
                                        pre_plate = open("preplate.txt", "r")
                                        if str(pre_plate) == str(keyMax):
                                            plateNumberDict.clear()
                                        else:
                                            if plateNumberDict[keyMax] > 4:
                                                temp = open("temp.txt", "w")
                                                temp.write(keyMax + "-" + str(plateNumberDict[keyMax]))
                                                temp.close()
                                if text_plate in plateNumberDict.keys():
                                    plateNumberDict[str(text_plate)] += 1
                                else:
                                    plateNumberDict[str(text_plate)] = 1

    print('current Dict: ', str(plateNumberDict))
    preplate = open("preplate.txt", 'r')
    pre_plate = preplate.read()
    if (plate_similarity(str(pre_plate), str(text_plate)) > 0.7):
        frame = cv2.putText(frame, str(pre_plate) + " XIN MOI QUET THE", (20, 30),
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