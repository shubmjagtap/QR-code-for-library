import sqlite3
import hashlib
from tkinter.tix import Tree
from sqlalchemy import false, true
import sys
import qrcode
from cgi import print_environ
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
from csv import reader
from tkinter import *

# connection = sqlite3.connect("shubham.db")
# crsr = connection.cursor()
# sql_command = """CREATE TABLE emp (serial_value INTEGER PRIMARY KEY,hash_value VARCHAR(20));"""
# crsr.execute(sql_command)


# string = 'jaychitale'
# hash_value = str(int(hashlib.sha1(string.encode("utf-8")).hexdigest(), 16) % (10 ** 8))
# format_string = """INSERT INTO emp(serial_value,hash_value) VALUES (NULL, "{hash}");"""
# sql_command = format_string.format(hash = hash_value)
# crsr.execute(sql_command)
# connection.commit()

# crsr.execute("SELECT * FROM emp")
# ans = crsr.fetchall()
# for i in ans:
#     print(i)

# connection.close()

number = 0

def insert(string):
    connection = sqlite3.connect("shubham.db")
    crsr = connection.cursor()
    print("Connected to the database")

    hash_value = str(int(hashlib.sha1(string.encode("utf-8")).hexdigest(), 16) % (10 ** 8))
    format_string = """INSERT INTO emp(serial_value,hash_value) VALUES (NULL, "{hash}");"""
    sql_command = format_string.format(hash = hash_value)
    crsr.execute(sql_command)
    connection.commit()
    connection.close()

# list = ["ashutosh moharir","amogh joghleker","harsh pitale"]
# for i in list:
#     insert(i)

def showDataBase():
    connection = sqlite3.connect("shubham.db")
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM emp")
    ans = crsr.fetchall()
    for i in ans:
        print(i)
    connection.close()

def find(hash_value):
    #hash_value = str(int(hashlib.sha1(string.encode("utf-8")).hexdigest(), 16) % (10 ** 8))
    connection = sqlite3.connect("shubham.db")
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM emp")
    ans = crsr.fetchall()
    for i in ans:
        if i[1] == hash_value:
            return 1
    connection.close()
    return 0

# def sendEmail(id,img):
#     #code

def makeQr(number):
    name = input("Enter first and last name => ")
    mis = input("mis number => ")
    phn =  input("phn number => ")


    details_string = f"{name}\n{mis}\n{phn}\n"
    hash_string = name+mis+phn
    print(hash_string)
    insert(hash_string)
    img = qrcode.make(details_string)
    img.save(f"qr{number}.png")
    number+=1

def pop_window(string):
    
    top = Tk()  
    text = Text(top)  
    text.insert(INSERT,string)    
    text.pack()  
    top.mainloop()  

def checkQr():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
        help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    # vs = VideoStream(src=0).start()
    vs = VideoStream(src = 0).start()
    time.sleep(2.0)
    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far
    csv = open(args["output"], "w")
    found = set()
    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)
    # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if barcodeData not in found:
                x = str(datetime.datetime.now())
                csv.write("{}{}\n".format(x+"\n",barcodeData))
                csv.flush()
                found.add(barcodeData)
                # show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
    
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    # close the output CSV file do a bit of cleanup
    print("[INFO] cleaning up...")
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()

    string  = ""
    string_to_show = ""
    import csv
    file_obj = open('barcodes.csv')
    heading = next(file_obj)
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        new_string = str(row)[2:-2]
        new_string_1 = new_string + "\n"
        string+=new_string
        string_to_show+=new_string_1
    hash_value = str(int(hashlib.sha1(string.encode("utf-8")).hexdigest(), 16) % (10 ** 8))
    print(hash_value)
    flag = find(hash_value)
    if flag == 1:
        string_to_show = "Student Present in database\n"+string_to_show
    else:
        string_to_show = "Student Not Present in database !!!\n"
    pop_window(string_to_show)


showDataBase()
while(true):
    print("1.New user ?\n2.Scan QRcode\n3.Quit\n");
    key = int(input("Enter the key => "))
    if key == 1:
        makeQr(number)
        showDataBase()
    elif key == 2:
        checkQr()
    
