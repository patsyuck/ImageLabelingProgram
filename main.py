# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 10:49:14 2021
Script for images (multi)labeling.
@author: o.patsiuk
"""
import csv, math, os, sys
import tkinter as tk
from tkinter import messagebox # must be imported separately from tkinter
from PIL import Image, ImageTk # to import the JPEG photo

PATH = './images/' # JPEG images folder
LABELS = './labels.txt' # all labels list
FILE = 'result.csv' # result markup file

resultFile = os.path.join(PATH, FILE)

files = [file for file in os.listdir(PATH) if file.endswith('.jpg') or
         file.endswith('.jpeg') or file.endswith('.jpe') or file.endswith('.jif') 
         or file.endswith('.jfif') or file.endswith('.jfi')]
filesLength = len(files)

l = []
for line in open(LABELS, "r"):
    l.append(line.strip())

if os.path.isfile(resultFile):
    os.remove(resultFile)
with open(resultFile, 'a', encoding = 'utf-8', newline = '') as file:
    writer = csv.DictWriter(file, fieldnames = ['image'] + l)
    writer.writeheader()

i = 0 # index for files

def readImage(idx, rotate=0):
    image = Image.open(os.path.join(PATH, files[idx]))
    if abs(rotate) == 90:
        height, width = image.size
    else:
        width, height = image.size
    if rotate: # rotate image
        image = image.rotate(rotate, expand = 1, fillcolor='dodgerblue')
    
    if (width > 540) or (height > 720):
        ratio = math.ceil(max(width/540, height/720))
        width = int(round(width/ratio))
        height = int(round(height/ratio))
    else:
        ratio = math.floor(min(540/width, 720/height))
        width = int(round(width*ratio))
        height = int(round(height*ratio))

    image = image.resize((width, height), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    return image

def moveToNext(idx):
    if idx < filesLength:
        img = readImage(idx)
        label.configure(image=img) # update the image
        label.image = img # to prevent garbage collection from deleting the image
        for status in labelsStatus:
            status.set(0)
    else:
        if messagebox.showinfo('THE END', 'All images are marked. Closing...'):
            root.destroy()

def addLabels():
    global i
    statuses = [x.get() for x in labelsStatus]
    if sum(statuses):
        dictTable = dict(zip(l, statuses))
        dictTable['image'] = files[i]
        with open(resultFile, 'a', encoding = 'cp1251', newline = '') as file: 
            writer = csv.DictWriter(file, fieldnames = ['image'] + l) 
            writer.writerow(dictTable)
        i += 1
        moveToNext(i)
    else:
        if messagebox.askokcancel('WARNING', 'Do you not want to mark the image?'):
            i += 1
            moveToNext(i)
    
def addCheckbox(item, statusList, h):
    status = tk.IntVar()
    statusBox = tk.Checkbutton(frame, text=item, variable=status)
    statusBox.place(width=150, height=33, x=100, y=h)
    statusList.append(status)
    return statusList

def rotate_p90():
    img = readImage(i, rotate=90)
    label.configure(image=img) # update the image
    label.image = img # to prevent garbage collection from deleting the image
    
def rotate_m90():
    img = readImage(i, rotate=-90)
    label.configure(image=img) # update the image
    label.image = img # to prevent garbage collection from deleting the image
    
def rotate_180():
    img = readImage(i, rotate=180)
    label.configure(image=img) # update the image
    label.image = img # to prevent garbage collection from deleting the image

def onClosing():
    if messagebox.askokcancel('EXIT', 'Do you want to close the program?'):
        root.destroy()

root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', onClosing)
root.title('Image Labeling Program')
root['bg'] = 'dodgerblue'
root.geometry('1000x800+100+100')
root.resizable(width=False, height=False) # forbid resizing

canvas = tk.Canvas(root, height=800, width=1000)
canvas.pack()

frameTitle = tk.Frame(canvas, bg='dodgerblue')
frameTitle.place(width=1000, height=50)
frameImage = tk.Frame(canvas, bg='dodgerblue')
frameImage.place(width=700, height=750, y=50)
frame = tk.Frame(canvas, bg='dodgerblue')
frame.place(width=500, height=750, x=700, y=50)

title = tk.Label(frameTitle, text='Select labels for this photo', bg='yellow', font='Arial 20')
title.place(width=400, x=300, y=10)

img=readImage(i)
label = tk.Label(frameImage, image=img)
label.image = img # to prevent garbage collection from deleting the image
label.place(x=80, y=15)

btnRotate_p90 = tk.Button(frame, text='Rotate +90\xb0 (counterclockwise)', command=rotate_p90)
btnRotate_p90.place(width=230, x=50, y=30)
btnRotate_180 = tk.Button(frame, text='Rotate 180\xb0 (upside down)', command=rotate_180)
btnRotate_180.place(width=230, x=50, y=60)
btnRotate_m90 = tk.Button(frame, text='Rotate -90\xb0 (clockwise)', command=rotate_m90)
btnRotate_m90.place(width=230, x=50, y=90)

labelsStatus = []
for j in range(len(l)):
    labelsStatus = addCheckbox(l[j], labelsStatus, h=140+35*j)

btn = tk.Button(frame, text='Add labels', font=40, bg='magenta', command=addLabels)
btn.place(width=150, x=100, y=180+30*len(l))

root.mainloop()
