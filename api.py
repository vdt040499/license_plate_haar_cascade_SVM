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
    # url = 'https://votan-sparking.herokuapp.com/tickets/createticket'
    url = 'http://localhost:3000/tickets/createticket'
    userId = '17521022'
    pre_value = ''
    reset_temp = open("temp.txt", "w")
    reset_temp.write("noplate")
    reset_temp.close()
    while True:
        file = open("temp.txt", "r") #lưu biển số và số lần lớn nhất
        number = str(file.read()) #đọc file
        if number != pre_value:
            pre_value = number
        else:
            if len(number) > 10: #nếu số lượng kí tự lớn hơn 10
                dataArr = number.split("-") #cắt chuỗi bỏ vào 1 mảng 2 phần tử
                # phần tử thứ nhất  dataArr[0]: biển sô
                # phần tử thứ 2     dataArr[1]: keymax
                payload = { 'numplate': dataArr[0], 'userId': userId} # nội dung payload chứa biển số xe + userId
                r = requests.post(url, data=payload)
                d = json.loads(r.text)
                successRes = d["success"]
                messRes = d["message"]
                if successRes == False:
                    print(messRes)
                    wrong_plate = open("wrongplate.txt", "w")
                    wrong_plate.write(dataArr[0])
                    wrong_plate.close()
                else:
                    print(str(userId) + 'TAO VE THANH CONG') #tạo vé thành công
                    reset_temp = open("temp.txt", "w")
                    reset_temp.write("noplate")
                    reset_temp.close()
                    preplate = open("preplate.txt", "w")
                    preplate.write(dataArr[0])
                    preplate.close()

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