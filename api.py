from absl import app, logging
import cv2
import numpy as np
import os
import requests
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
import time
import json

# def unlock_cooler():
#     GPIO.setup(11, GPIO.OUT)
#     p = GPIO.PWM(11, 50)
#     p.start(2.5)
#     p.ChangeDutyCycle(7.5)
#     time.sleep(1.5)
#     p.ChangeDutyCycle(2.5)
#     time.sleep(1)
#     p.stop()

def main(argv):
    # Run on Win
    # url = 'https://votan-sparking.herokuapp.com/tickets/createticket'
    url = 'http://localhost:3000/tickets/createticket'
    userId = '17521022'
    while True:
        file = open("temp.txt", "r")
        number = str(file.read())
        if len(number) > 10:
            dataArr = number.split("-")
            # dataArr[0]: biển sô
            # dataArr[1]: keymax
            if (int(dataArr[1]) == 5):
                payload = { 'numplate': dataArr[0], 'userId': userId}
                r = requests.post(url, data=payload)
                d = json.loads(r.text)
                successRes = d["success"]
                messRes = d["message"]
                if successRes == False:
                    print(messRes)
                    break
                else:
                    print(str(userId) + 'TAO VE THANH CONG')
                    preplate = open("preplate.txt", "w")
                    preplate.write(dataArr[0])
                    deldic = open("deldic.txt", "r")
                    if str(deldic.read()) == "DETECT":
                        print("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
                        deldic = open("deldic.txt", "w")
                        deldic.write("OK")
                        deldic.close()
                        break

    # Run on Raspberry Pi
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