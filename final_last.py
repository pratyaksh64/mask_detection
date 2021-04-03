import cv2
import dlib
import time
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
from datetime import datetime

#drive authorization
gauth = GoogleAuth()
# =============================================================================
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)
# =============================================================================

gauth.LoadCredentialsFile("mycreds_1.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds_1.txt")
drive = GoogleDrive(gauth)
folderName = input('date:')
n_folderName=folderName
path = r"E:/mask_recognition/{}".format(n_folderName)
os.mkdir(path)
file1 = drive.CreateFile({'title': folderName, 'mimeType': 'application/vnd.google-apps.folder'})
file1.Upload()

window_name = 'Image'
font = cv2.FONT_HERSHEY_SIMPLEX
org = (0, 50)
fontScale = 1
color = (0, 0, 255)
thickness = 2

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
  
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces: 
        x1 = face.left()
        y1 = face.top() 
        x2 = face.right() 
        y2 = face.bottom() 
        p = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        landmarks = predictor(gray, face)
        
        for n in range(31,36):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            t = cv2.circle(_,(x, y), 2, (255, 255, 0), -1)

        if t.any()==True:
              time.sleep(1)
              #cv2.imshow("frame",frame ) 
              photo = time.strftime(r"%Y-%m-%d_%H-%M-%S") 
              file = r'E:/mask_recognition/{}/{}.jpg'.format(
                  n_folderName, photo)
              cv2.imwrite(file,frame)
              time.sleep(2)
              continue

    if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

    cv2.imshow("frame",frame ) 
    now2 = datetime.now() 
    current = now2.strftime("%H:%M")
    if current == '21:58':
        break

cap.release()
cv2.destroyAllWindows()

now = datetime.now()
current_time = now.strftime("%H:%M")

while current_time != '22:01':
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    continue

folders = drive.ListFile(
{'q': "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
for folder in folders:
    if folder['title'] == folderName:
        for x in os.listdir(path):
            file2 = drive.CreateFile({'parents': [{'id': folder['id']}], 'title': x})
            file2.SetContentFile(os.path.join(path, x))
            file2.Upload()
