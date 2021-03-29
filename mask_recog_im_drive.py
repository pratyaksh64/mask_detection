import cv2
import dlib 
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds_1.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Creates local webserver and auto
# handles authentication.

gauth.SaveCredentialsFile("mycreds_1.txt")

path = r"C:\Users\siddant bhalla\with_mask"

drive = GoogleDrive(gauth)

folderName = 'test4'  # Please set the folder name.

file1 = drive.CreateFile({'title': folderName, 'mimeType': 'application/vnd.google-apps.folder'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
 # Set content of the file from given string.
file1.Upload()

window_name = 'Image'
font = cv2.FONT_HERSHEY_SIMPLEX 
org = (0, 50) 
fontScale = 1
color = (0, 0, 255)
thickness = 2

detector = dlib.get_frontal_face_detector() 
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
  
frame = cv2.imread('C:/Users/siddant bhalla/without_mask2/t2 (100).jpg', 1)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = detector(gray) 
o = 0

if o==2 or o==1:
   image = cv2.putText(frame, 'mask detected', org, font,  
                   fontScale, color, thickness, cv2.LINE_AA)
   cv2.imshow("Frame", frame) 
else:
   folders = drive.ListFile(
    {'q': "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
   for folder in folders:
        if folder['title'] == folderName:
            file2 = drive.CreateFile({'parents': [{'id': folder['id']}]})
            file2.SetContentFile('C:/Users/siddant bhalla/without_mask2/t2 (100).jpg')
            file2.Upload()

# =============================================================================
# cv2.imshow("Frame", frame) 
# cv2.waitKey(2000)
# cv2.destroyAllWindows
# =============================================================================
