from flask import Flask,render_template,Response,jsonify
import cv2
import webbrowser
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app1=Flask(__name__)
camera=cv2.VideoCapture(0)

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

countert = 0
counter1 = 0
counter2 =0

def generate_frames():
# Curl counter variables
    '''counterl = 0 
    counterr = 0
    stagel = None
    stager = None'''
    global countert
    global counter1
    global counter2
 #Squat counter variables
    count = 0
    stagell = None
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    ##while 
     while True:
        success,frame=camera.read()
        if not success:
            break
        else:
             # Recolor image to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            # Make detection
            results = pose.process(frame)
            # Recolor back to BGR
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # Render detections
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                         mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                         )
            
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                ## Coordinate Extraction

                # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
            
                 # Get coordinates for left curl 
                shoulderl = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbowl = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wristl = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
                # Get coordinates for right curl
                shoulderr = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbowr = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wristr = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]  
                
                
                # Calculate angle (left)
                anglel = calculate_angle(shoulderl, elbowl, wristl)
                # Calculate angle (right)
                angler = calculate_angle(shoulderr, elbowr, wristr)
            
                # Visualize angle (left)
                cv2.putText(frame, str(anglel), 
                           tuple(np.multiply(elbowl, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                # Visualize angle (right)
                cv2.putText(frame, str(angler), 
                           tuple(np.multiply(elbowr, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA   
                                )
                 # Get coordinates for squat
                hipl = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                kneel = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                anklel = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
                hipr = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                kneer = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankler = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
                # Calculate angle (left)
                anglell = calculate_angle(hipl,kneel,anklel)
                anglerl = calculate_angle(hipr,kneer,ankler)
                # Visualize angle (left)
                cv2.putText(frame, str(anglell), 
                           tuple(np.multiply(kneel, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, str(anglerl), 
                           tuple(np.multiply(kneer, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                ## Logical Part

                 # Curl counter logic(left)
                if anglel > 160:
                    stagel = "down"
                if anglel < 20 and stagel =='down':
                    stagel="up"
                    ##counterl +=1
                    countert +=1
                    ##print(counterl)
            
                # Curl counter logic(right)
                if angler > 160:
                    stager = "down"
                if angler < 20 and stager =='down':
                    stager="up"
                    ##counterr +=1
                    counter1 +=1
                    ##print(counterr)

                # squat counter logic(left)
                if anglell > 160:
                    stagell = "up"
                if anglell < 70 and stagell=='up' and anglerl < 70:
                    stagell="down"
                    count +=1
                    counter2 +=1
                    print(count)


            except:
                pass

            '''  cv2.rectangle(frame, (0,0), (225,73), (245,117,16), -1)
            
            cv2.putText(frame, 'SQ REPS', (10,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(count), (8,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            cv2.putText(frame, 'STAGE', (115,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame, stagell,(100,45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)'''

            

        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'
                    b'content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app1.route('/')
def index():        
        return render_template('index.html')

@app1.route('/video')
def video():
    return Response( generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app1.route('/counter')
def get_counter():
    countert
    return jsonify({'counter':countert})
@app1.route('/counterp')
def get_counterp():
    counter1
    return jsonify({'counterp':counter1})
@app1.route('/counters')
def get_counters():
    counter2
    return jsonify({'counters':counter2})


if __name__=="__main__":
    app1.run(debug=True)
