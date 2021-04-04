import cv2
import dlib
import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from imutils.video import WebcamVideoStream
import time

class VideoCamera(object):
    def __init__(self):
        self.stream = WebcamVideoStream(src=0).start()
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile("mycreds_1.txt")


        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()
        self.gauth.SaveCredentialsFile("mycreds_1.txt")
        self.drive = GoogleDrive(self.gauth)
        self.folderName = '24'
        self.n_folderName = self.folderName
        self.path = r"/home/asus/Desktop/mask_recog/without_mask2/{}".format(self.n_folderName)
        os.mkdir(self.path)
        self.file1 = self.drive.CreateFile(
            {'title': self.folderName, 'mimeType': 'application/vnd.google-apps.folder'})
        self.file1.Upload()

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        self.frame = self.stream.read()

        self.window_name = 'Image'
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (0, 50)
        self.fontScale = 1
        self.color = (0, 0, 255)
        self.thickness = 2

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.faces = self.detector(self.gray)
        for self.face in self.faces:
            self.x1 = self.face.left()
            self.y1 = self.face.top()
            self.x2 = self.face.right()
            self.y2 = self.face.bottom()
            self.p = cv2.rectangle(self.frame, (self.x1, self.y1),
                                   (self.x2, self.y2), (255, 0, 0), 3)
            self.landmarks = self.predictor(self.gray, self.face)

            for self.n in range(31,36):
                self.x = self.landmarks.part(self.n).x
                self.y = self.landmarks.part(self.n).y
                self.t = cv2.circle(self.frame, (self.x, self.y),
                                    2, (255, 255, 0), -1)

            if self.t.any() == True:
                time.sleep(2)
                self.photo = time.strftime(r"%Y-%m-%d_%H-%M-%S")
                self.file = r'/home/asus/Desktop/mask_recog/without_mask2/{}/{}.jpg'.format(
                    self.n_folderName, self.photo)
                cv2.imwrite(self.file, self.frame)
                time.sleep(5)
                continue

        
        _, jpeg = cv2.imencode('.jpg', self.frame)
        data = []
        data.append(jpeg.tobytes())
        return data
