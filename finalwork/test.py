# -*- coding: utf-8 -*-
"""
Created on Thu May 28 00:25:55 2020

@author: yyhaos
@github: 
"""

import matplotlib.pyplot as plt #用于图片展示
import numpy as np #fft
import cv2 #读取图片
#from tkinter import *
import tkinter as tk #简单gui

class MyDft(): #DFT实现
    def normal(input):
        return input
    def dft(input):
        return input

class MyHomomorphicFilter(): #同态滤波器实现
    def homofilter():
        return 0
    
class MyFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.pack()
        self.createWidgets()   
    def createWidgets(self):
        self.helloLabel = tk.Label(self,text="1")
        self.helloLabel.pack()
        #self.quitButton = Button(self,text="谁呢？",command=self.who)
        #self.quitButton.pack()


def main():
    a=MyFrame()
    a.master.title("1")
    a.mainloop()

if __name__ =='__main__':
    main()