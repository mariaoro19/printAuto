#from flask import Flask
from flask import Flask, render_template
import datetime
import sys
import os
#import tkinter as tk
#from tkinter import ttk
import cups
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
import time

#ws = Tk()
#ws.title('PythonGuides')
#ws.geometry('400x200') 
#app = Flask(__name__)
#@app.route('/')
#def index():
 #   return 'Hello world'
app = Flask(__name__)
@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('index.html', **templateData)
@app.route('/my-link/')
def my_link():
  conn = cups.Connection ()
  printers = conn.getPrinters ()
  for printer in printers:
      print (printer, printers[printer]["device-uri"])
      printer_name=printer
  print(printer_name)
  file = "impriir.txt"
  print(printer)
  conn.printFile (printer_name, file, "Project Report", {})  


  return 'Click.'

if __name__ == '__main__':
    app.run(debug=True, port=3003, host='192.168.1.15')