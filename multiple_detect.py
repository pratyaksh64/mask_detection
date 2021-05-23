import cv2
import dlib
import time 

window_name = 'Image'
font = cv2.FONT_HERSHEY_SIMPLEX
org = (0, 50)
fontScale = 1
color = (0, 0, 255)
thickness = 2



cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
 
def detect_points(gray,face):
    x1 = face.left()
    y1 = face.top() 
    x2 = face.right() 
    y2 = face.bottom() 
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    landmarks = predictor(gray, face)
    
    for n in (29,31,35,58,51): 
       
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        t = cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)
        if t.any()==True:
            image = cv2.putText(frame, 'wear a mask', org, font,  
                   fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
        continue
        return image
    
    
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    start = time.time()
    faces = detector(gray)
    end = time.time()
    p = [detect_points(gray, f) for f in faces]
    cv2.imshow("frame",frame) 
    key = cv2.waitKey(1)
    if key == 27: 
        break