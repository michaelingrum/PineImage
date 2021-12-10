import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@server.route("/")
def hello():
    return "Hello World!"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@server.route('/api/traffic', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(server.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            processFile(path)

            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory

@server.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(server.config["UPLOAD_FOLDER"], name)

import subprocess
def processFile(path):
    print(path)
    os.system("python3 yolov5/detect.py --weights ./best.pt --source " + path + " --img 720 --conf .25")
    os.system("cp -r yolov5/runs/detect/exp/. uploads")
    os.system("rm -r yolov5/runs/detect/exp")




if __name__ == "__main__":
   server.run(host='0.0.0.0')