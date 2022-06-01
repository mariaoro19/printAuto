# Libreries
import datetime
import sys
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cups
import time

# Initialing API
app = Flask(__name__)

# Calling principal html index
@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('index.html', **templateData)

@app.route('/upload')
def upload_file():
   return render_template('index.html')

# Printing after uploading the file	
@app.route('/Send', methods = ['GET', 'POST'])
def send_file():
   print("Send")
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      # conn = cups.Connection ()
      # printers = conn.getPrinters ()
      # for printer in printers:
      #    print (printer, printers[printer]["device-uri"])
      #    printer_name=printer
      # print(f.filename)
      # file =f.filename
      # conn.printFile (printer_name, file, "Project Report", {})  
      return render_template('send.html')
# Connecting to the localhost
if __name__ == '__main__':

   app.run(debug=True, port=3003, host='192.168.1.15')