import os
from camera import VideoCamera
from flask import Flask, render_template, Response
import webbrowser
import requests
from datetime import datetime
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth



app = Flask(__name__)


def drive_upload():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds_1.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds_1.txt")
    drive = GoogleDrive(gauth)

    folderName = '38'

    file1 = drive.CreateFile({'title': folderName, 'mimeType': 'application/vnd.google-apps.folder'})
    file1.Upload()

    folders = drive.ListFile(
        {'q': "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

    path = r"/home/asus/Desktop/mask_recog/without_mask2/{}".format(folderName)

    for folder in folders:
        if folder['title'] == folderName:
            for x in os.listdir(path):
                file2 = drive.CreateFile(
                    {'parents': [{'id': folder['id']}], 'title': x})
                file2.SetContentFile(os.path.join(path, x))
                file2.Upload()



@app.route('/')
def home():
    return render_template('index.html')


def gen(camera):
    while True:
        data = camera.get_frame()
        frame=data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)


'''
while(True):
    r = requests.get('http://127.0.0.1:5000/video_feed')
    if r.status_code==200:
        webbrowser.open('http://127.0.0.1:5000/video_feed')
        break
'''

while(True):
    if(not webbrowser.open('http://127.0.0.1:5000/video_feed')):
        continue
    else:
        webbrowser.open('http://127.0.0.1:5000/video_feed')
        break



now = datetime.now()

current_time = now.strftime("%H:%M")

'''
while current_time != '16:43':
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    continue
else:
    drive_upload()
'''
