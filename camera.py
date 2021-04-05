import cv2
import dlib
import os
from imutils.video import WebcamVideoStream
import time


class VideoCamera(object):
    def __init__(self):
        self.stream = WebcamVideoStream(src=0).start()
        
        self.folderName = '38'
        self.n_folderName = self.folderName
        self.path = r"/home/asus/Desktop/mask_recog/without_mask2/{}".format(self.n_folderName)
        os.mkdir(self.path)
        
        


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

        
        _, self.jpeg = cv2.imencode('.jpg', self.frame)
        self.data = []
        self.data.append(self.jpeg.tobytes())

        return self.data

    
