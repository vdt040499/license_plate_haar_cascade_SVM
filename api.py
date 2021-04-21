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
    # GPIO.setup(11, GPIO.OUT)
    # p = GPIO.PWM(11, 50)
    # p.start(2.5)
    # p.ChangeDutyCycle(7.5)
    # time.sleep(1.5)
    # p.ChangeDutyCycle(2.5)
    # time.sleep(1)
    # p.stop()
    

def main(argv):
    # Run on Win
    url = 'https://votan-sparking.herokuapp.com/tickets/createticket'
    # url = 'http://localhost:3000/tickets/createticket'
    userId = '17521022'
    pre_value = ''
    reset_temp = open("temp.txt", "w")
    reset_temp.write("noplate")
    reset_temp.close()
    while True:
        process = open("process.txt", "r")
        temp = open("temp.txt", "r")
        current_session = temp.read()
        plates = []
        values = []
        if len(current_session) > 7:
            if len(current_session) <=18:
                plates = current_session.split("]-[")[0][2:-1]
                values = current_session.split("]-[")[1][0:-1]
            else:
                plates = current_session.split("-")[0][2:-2].split("', '")
                values = current_session.split("-")[1][1:-1].split(", ")
            if (str(process.read()) == "DETECTING" and int(values[0]) > 7):
                    # print(len(current_session))
                    # print('Values: ', values)
                    # payload = { 'plates': plates, 'values': values, 'userId': userId} # nội dung payload chứa biển số xe + userId
                    # r = requests.post(url, data=payload)
                    # d = json.loads(r.text)
                    print('Hello: ', values[0])
                    process = open("process.txt", "w")
                    process.write("DONE")
                    process.close()

                    preplate = open("preplate.txt", "w")
                    preplate.write(plates[0])
                    preplate.close()
                    # successRes = d["success"]
                    # messRes = d["message"]

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