import os
import cv2
import time
import json
import difflib
import requests
import similarity
import numpy as np
# import RPi.GPIO as GPIO
from absl import app, logging
from pyzbar.pyzbar import decode
#from mfrc522 import SimpleMFRC522

# def unlock_cooler():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(17, GPIO.OUT)
#     try:
#         p = GPIO.PWM(17, 50)
#         p.start(2.5)
#         p.ChangeDutyCycle(7.5)
#         time.sleep(1.5)
#         p.ChangeDutyCycle(2.5)
#         time.sleep(1)
#         p.stop()
#     except KeyboardInterrupt: # If CTRL+C is pressed
#         print("Keyboard interrupt")
#     except:
#         print("some error")
#     finally:
#         print("clean up")
#         GPIO.cleanup() # cleanup all GPIO

def main(argv):
    # Run on QR CAM

    # Info for create ticket request
    # url = 'https://votan-sparking.herokuapp.com/tickets/createticket'
    url = 'http://localhost:5000/tickets/'
    # userId = '17521022'
    # pre_value = ''

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
        
        # Modify the frame size => Optimize FPS
        scale_percent = 50 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

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
        cv2.imshow('QR Cam', img)
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

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
     
if __name__ == '__main__':
    app.run(main)