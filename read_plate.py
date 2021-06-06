
import cv2
import json
import time
import detect
import requests
import save_temp
import threading
import similarity
import check_plate
import numpy as np
from tkinter import *
from tkinter.ttk import *
import handle_halfofplate
# import RPi.GPIO as GPIO
from absl import app, logging
from tkinter import messagebox
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
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
quit = open("quit.txt", "w")
quit.write("no")
quit.close()

# Global var
quit_var = False
text_plate = '' # Current plate text
global plateNumberDict 
plateNumberDict = {} # Curent plate list
img = np.array([])
frame = np.array([])
temp_frame = np.array([])

# Define file
vid = cv2.VideoCapture("test/video2.h264")

# Reset txt file
def reset():
    reset_temp = open("temp.txt", "w")
    reset_temp.write("")
    reset_temp.close()
    reset_preplate = open("preplate.txt", "w")
    reset_preplate.write("")
    reset_preplate.close()
    reset_process = open("process.txt", "w")
    reset_process.write("")
    reset_process.close()

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

def run_rp():
    global temp_frame
    global text_plate
    global plateNumberDict

    # Read video
    while True:
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            temp_frame = frame

            # Modify the frame size => Optimize the FPS
            scale_percent = 20 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)     

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

        # Reverse current plate number list
        plateNumberDict = dict(sorted(plateNumberDict.items(), key=lambda item: item[1], reverse=True))
        print('current Dict: ', str(plateNumberDict))

        process = open("process.txt", "r")
        temp = open("temp.txt", "r")
        if not not bool (plateNumberDict):
            keyMax = max(plateNumberDict, key=plateNumberDict.get)
            if (process.read() == 'DETECTING' and int(plateNumberDict[keyMax]) > 1 and len(plateNumberDict) != 0):
                frame = cv2.putText(frame, "MOI QUET MA", (20, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                temp_frame = cv2.putText(frame, "MOI QUET MA", (20, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # if (process.read() == 'DONE' or (len(plateNumberDict) == 0 and temp.read() != '')):
            # frame = cv2.putText(frame, "MOI XE QUA", (20, 100),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # temp_frame = cv2.putText(frame, "MOI XE QUA", (20, 100),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        fps = 1.0 / (time.time() - start_time)
        print("FPS: %.2f" % fps)
        print('------------------------------------------------------------------------------------------------------------')
        quit = open("quit.txt", "r")
        if quit.read() == 'yes':
            reset()
            break

def run_api():
    global img

    # Api url
    # url = 'https://votan-sparking.herokuapp.com/tickets/createticket'
    url = 'http://localhost:5000/tickets/'

    # Init status
    reset_temp = open("temp.txt", "w")
    reset_temp.write("")
    reset_temp.close()

    # Configure QR Cam
    cap = cv2.VideoCapture(0)
    cap.set(3,300)
    cap.set(4,300)

    while True:
        # Read QR Code
        success, img = cap.read()

        plate_code = ''
        id_code = ''
        for barcode in decode(img):
            code = barcode.data.decode('utf-8')
            plate_code = code.split('-')[0]
            id_code = code.split('-')[1]
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img,[pts],True,(255,0,255),5)
            pts2= barcode.rect
            cv2.putText(img, code,(pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
        # cv2.imshow('QR Cam', img)
        cv2.waitKey(1)
        
        # Read temp plate
        process = open("process.txt", "r")
        temp = open("temp.txt", "r")
        current_plate = temp.read()
        if (current_plate != ''):
            plate = current_plate.split("-")[0]
            plate_value = current_plate.split("-")[1]

            # Check condition for create ticket
            if (str(process.read()) == "DETECTING" and int(plate_value) > 1):
                if (plate_code != '' and id_code != ''):
                    if similarity.plate_similarity(str(plate_code), str(plate)) > 0.8:
                        print('Plate: ', plate)
                        print('Code: ', plate_code)
                        print('User ID: ', id_code)
                        print('THANH CONG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        r = requests.post(url+str(id_code))
                        d = json.loads(r.text)
                        process = open("process.txt", "w")
                        process.write("DONE")
                        process.close()

                        preplate = open("preplate.txt", "w")
                        preplate.write(plate)
                        preplate.close()
        quit = open("quit.txt", "r")
        if quit.read() == 'yes':
            reset()
            break

    # Run on RFID
    # url = 'https://votan-sparking.herokuapp.com/tickets/createticket'
    # while True:
    #     file = open("temp.txt", "r")
    #     number = str(file.read())
    #     if len(number) > 10:
    #         dataArr = number.split("-")
    #         if (int(dataArr[1]) >= 5):
    #             while True:
    #                 reader = SimpleMFRC522()
    #                 id, text = reader.read()
    #                 print('IDcard: ', id)
    #                 print('User: ', text)
    #                 infoArr = text.split(' - ')
    #                 studentId = str(infoArr[0])
    #                 payload = { 'numplate': dataArr[0], 'userId': studentId }    
    #                 r = requests.post(url, data=payload)
    #                 d = json.loads(r.text)
    #                 successRes = d["success"]
    #                 messRes = d["message"]
    #                 if successRes == False:
    #                     print(messRes)
    #                     break
    #                 else:
    #                     print(str(studentId) + 'TAO VE THANH CONG')
    #                     unlock_cooler()
    #                     break

def show_cam():
    global img                            
    if not img.size == 0:
        img = cv2.resize(img,(500,300))
        pic = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                      
        timg = Image.fromarray(pic)
        imgtk = ImageTk.PhotoImage(image=timg)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    lmain.after(5, show_cam)

def show_vid():
    global temp_frame
    if not temp_frame.size == 0:
        temp_frame = cv2.resize(temp_frame,(500,300))
        img2 = Image.fromarray(temp_frame)
        img2tk = ImageTk.PhotoImage(image=img2)
        lmain2.img2tk = img2tk
        lmain2.configure(image=img2tk)
    lmain2.after(5, show_vid)

if __name__ == '__main__':
    api_thread = threading.Thread(target=run_api)
    rp_thread = threading.Thread(target=run_rp)
    api_thread.start()
    rp_thread.start()

    def Exit():
        sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=root)
        if sure == True:
            root.destroy()
            quit = open("quit.txt", "w")
            quit.write("yes")
            quit.close()

    root = Tk()
    root.geometry("1366x768")
    root.title("sParking License Plate Detector")
    root.resizable(0, 0)
    root.protocol("WM_DELETE_WINDOW", Exit)

    # Background
    background = Label(root)
    background.place(relx=0, rely=0, width=1366, height=768)
    bg = PhotoImage(file="./images/main_screen.png")
    background.configure(image=bg)

    # QR frame
    lmain = Label(master=root)
    lmain.place(relx=0.123, rely=0.190, width=500, height=300)

    # Video frame
    lmain2 = Label(master=root)
    lmain2.place(relx=0.523, rely=0.190, width=500, height=300)

    threading.Thread(target=show_cam).start()
    threading.Thread(target=show_vid).start()

    root.mainloop()