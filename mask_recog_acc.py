import cv2  
import dlib 
import pyttsx3
import playsound

engine = pyttsx3.init()
true = 0
false = 0
# =============================================================================
# engine.say('wear a mask')
# engine.runandwait()
# =============================================================================
detector = dlib.get_frontal_face_detector() 
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
for l in range(1, 3001):
    frame = cv2.imread('t2 ({}).jpg'.format(l), 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray) 
    o = 0
    for face in faces:
        o=1
        x1 = face.left()
        y1 = face.top() 
        x2 = face.right()
        y2 = face.bottom() 
        p = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        landmarks = predictor(gray, face)       
        i = [31, 32, 33, 34, 35]
        for n in i:
                o = 2
                x = landmarks.part(n).x 
                y = landmarks.part(n).y 
                #cv2.rectangle(frame, (x, y), (x+5, y+5), (0, 255, 255))
                t = cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)
# =============================================================================
#             if t.any()==True:
#              engine.say('wear a mask')
#              engine.runAndWait()
#              break
# =============================================================================
#                playsound.playsound('audio.mp3')
#                break
    if o==2:
        true = true+1
        print('done t{}'.format(l))
    else:
        false = false+1
        print('done f{}'.format(l))
# =============================================================================
# cv2.imshow("Frame", frame) 
# cv2.waitKey(2000)
# cv2.destroyAllWindows
# =============================================================================
