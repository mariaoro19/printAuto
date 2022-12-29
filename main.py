# Libreries

import os
import cups
from flask import Flask, session, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import PyPDF2
import glob
import subprocess
import time
#Variables
UPLOAD_FOLDER = 'static/uploads/'



# Initialing API
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


#Formats of files allowed to print
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])
ALLOWED_EXTENSIONS = set([ 'pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Display the main page
@app.route('/')
def upload_form():
    return render_template('upload.html')

#Display and do a Post in the API for choosing the file
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No ha seleccionado archivo','error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if filename.rsplit('.', 1)[1].lower() == 'pdf':
            filepdf='static/uploads/'+filename
            file2 = open(filepdf, 'rb')
            readpdf = PyPDF2.PdfFileReader(file2)
            totalpages = readpdf.numPages
            countLetter=0
            countLegal=0
            sizeFileVector=[]
            #Loop to check the bigger page
            for i in range(totalpages):
                sizeFileV = readpdf.getPage(i).mediaBox
                print(sizeFileV[3])
                sizeFileVector.append(sizeFileV)
            sizeFileV= max(sizeFileVector)
            
            # We have that Letter is 612x792 and Legal is 612x939
            if sizeFileV[3]>792:
                #sizeFile="Custom.612x936"
                sizeFile="Legal"
                session['size'] = sizeFile
                flash('Imagen cargada exitosamente')
                return render_template('pay.html', filename=filename,totalpages=totalpages, sizeFile=sizeFile)
            elif sizeFileV[2]>612 and sizeFileV[3]>936: 
                flash('Tamaño del documento deben ser Carta u Oficio', 'error')
                return redirect(request.url)
            else:
                sizeFile="Letter"
                session['size'] = sizeFile
                flash('Imagen cargada exitosamente')
                return render_template('pay.html', filename=filename,totalpages=totalpages, sizeFile=sizeFile)
                    
            
        #For now this else doesn work, its for images
        else:
            totalpages = 1
            sizeFile="Letter"   
    
    else:
        flash('Formato del documento no admitido', 'error')
        return redirect(request.url)
    
    
#Function to display file
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

# # Printing after uploading the file	
@app.route('/payProcess/<filename>', methods=['GET','POST'])
def pay(filename):
   color=request.form.get('color')
   numCopies=str(request.form.get('numCopies'))
   pages=request.form.get('pages')
   sides= request.form.get('side')	
   #size  = sizeFile.get('sizeFile',None)
   sizeFile = session.get('size', None)
   print(sizeFile)
   if request.method == 'POST':
       #f = request.files['file']
       #f.save(secure_filename(f.filename))
       conn = cups.Connection ()
       printers = conn.getPrinters ()
       #print('printer',printers)
       for printer in printers:
           print ("printer:"+printer, printers[printer]["device-uri"])
           printer_name=printer
       #print(f.filename)
       #file =f.filename
       file="static/uploads/"+filename
       #print(file)
      
       #conn.printFile (printer_name, file, "Project Report", {"Duplex":"DuplexTumble"}) 
    
    #    if pages=="":
            
    #       printid = conn.printFile (printer_name, file, "Project Report", {"print-color-mode":color,"copies":numCopies,"sides":sides, "media":sizeFile}) 
    #    else:

    #       printid= conn.printFile (printer_name, file, "Project Report", {"print-color-mode":color,"copies":numCopies,"sides":sides, "media":sizeFile,"page-ranges":pages}) 
       
          
       
   #print(printid)
   #printjob=conn.getJobAttributes(printid)["job-state"]
   #printid = conn.printFile(printer_name, file, 'test', {})
   #Checking if the print was suscessfull
   #print(printid)
   #print(printjob)
   stop = 0
   TIMEOUT = 50
    
#    while str(subprocess.check_output(["lpstat"])).find(str(printid)) > 0 and    stop < TIMEOUT:
#        stop+= 1
#        time.sleep(1)
#    if stop < TIMEOUT:
#        print ("PRINT SUCCESS")
#    else:
#        print ("PRINT FAILURE")

   #Removing files after print
   filesRemove=glob.glob('static/uploads/*')
   for f in filesRemove:
       os.remove(f)

   
   return render_template('payProcess.html')

# Connecting to the localhost
if __name__ == '__main__':
   
   app.run(debug=True, port=3003, host='192.168.1.21')
   #app.run(debug=True, port=3003, host='127.0.0.2')
   
   #app.config['SERVER_NAME']= "printexp.dev:3003"
   #app.url_map.host_matching=True
   #app.run(debug=True, host='printexp.dev:3003')
   