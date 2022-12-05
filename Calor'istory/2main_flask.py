from flask import Flask, render_template, request, Response
from scripts.calories_function_3 import jump_calories_count
from scripts.calories_function_3T import total_calories_counter
from scripts.play_function_3 import superfitmario
from scripts.finalDfToPlot import cleanAndPick


import mediapipe as mp
import numpy as np
import pandas as pd
import time
import csv
from pandas import Timestamp

import pyautogui


import cv2

app = Flask(__name__)


# ------------------previous functions--------------------------------------------------------------------------------------------
prevSum = 0  

# --------- FUNCTIONS -----------

def inFrame(lst): # lst is the list of all the landmark positions
    if lst[24].visibility > 0.7 and lst[23].visibility > 0.7 and lst[15].visibility>0.7: #means it is visible in the frame
        position = "up"
        return True #if all these landmarks/points are visible
    return False

def isBackward(lst):
    if (lst[24].y*480) > 400 and (lst[23].y*480) > 400:
        return True
    return False

def isJump(lst):
    if (lst[0].y*480)<=10:  # [0] is the nose position, y*480 is to de-normalize, < 60 to go up to count jump
        return True
    return False


def findSum(lst):
    sm = 0
    sm = lst[26].y*640 + lst[25].y*640 + lst[0].y*640 + lst[23].y*640 + lst[24].y*640 
    return sm


def push(sm):
    global sum_list
    for i in range(3, -1, -1):
        sum_list[i+1] = sum_list[i]

    sum_list[0] = abs(sm - prevSum)


def isRunning(lst):
    if (lst[20].y*480 and lst[19].y*480 >= lst[24].y*480 and lst[23].y*480):
        # if (lst[24].y*480) < 350 and (lst[23].y*480) < 350:
        if (lst[0].y*480)>=10:
            sm = 0
            for i in sum_list:
                sm = sm + i

            if sm > 150:
                return True 
            return False
# ************************************OPENING CAMERA**********************************
runlist_extended = [0]
def gen_frame():
    global runlist_extended
    global prevSum

    cap = cv2.VideoCapture(0)
    pose = mp.solutions.pose #this is the model - it's for pose detection
    pose_o = pose.Pose() # it's to process our frame
    drawing = mp.solutions.drawing_utils #draws all the points and lines in the body
    # ---------- RUNNING LOGIC ----------

    isInit = False
    global sum_list
    sum_list = np.array([0.0]*5)




    # --------- KEYBOARD KEYS --------
    l_down = False
    d_down = False
    a_down = False

    # --------- COUNTERS & LISTS ----------
    jumps = 0
    imlist = []
    count = 0
    position = None
    squats = 0
    squat_count = 0
    squat_list = []

    
    time_running_instant = 0


    while cap.isOpened():

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # cv2.namedWindow("Resize", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Resize", 900, 800)

        res = pose_o.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


        if res.pose_landmarks:
            finalres = res.pose_landmarks.landmark

        drawing.draw_landmarks(frame, res.pose_landmarks, pose.POSE_CONNECTIONS)

        if res.pose_landmarks and inFrame(finalres):
    # ********************************************************** RUNNING WITH MOVEMENT *******************************************************
            
            if not(isInit):
                prevSum = findSum(finalres)
                isInit = True
            else:
                newSum = findSum(finalres)
                push(newSum)

                start = time.time()
                if isRunning(finalres): ##  running down the d key
                    # cv2.putText(frame, "Running", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                    if not(d_down):                  # --> commands to run
                        pyautogui.keyDown("d")
                        d_down=True            
                    else:
                        if (d_down):                  # --> commands to statick
                            pyautogui.keyUp("d")
                            d_down=False
                
                end = time.time()
                total_time = end - start
                if total_time > 0:
                    time_running_instant += (total_time * 1.80) #1.70 is he constant for real time running
                    print(time_running_instant)
                    runlist_extended.append(time_running_instant)

                

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ JUMPING +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                if isJump(finalres):
                    # cv2.putText(frame, "jumping", (50,150), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                    count += 1

                    if not(l_down):                  # --> commands to jump
                        pyautogui.keyDown("w")
                        l_down=True

                    if count > 0 and count < 2 :
                        jumps += 1
                        print(jumps)
                        imlist.append('jump')

                else:
                   # cv2.putText(frame, "not jumping", (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    count = 0

                    if l_down:                       # --> commands to NOT jump
                        pyautogui.keyUp("w")
                        l_down=False

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ SQUATING +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if isBackward(finalres):
                    # cv2.putText(frame, "going back", (300,300), cv2.FONT_HERSHEY_PLAIN, 1, (255,6,89), 2)
                    squat_count += 1

                    if not(a_down):
                        pyautogui.keyDown("a")
                        a_down=True

                    if squat_count > 0 and squat_count < 2 :
                        squats += 1
                        print(squats)
                        squat_list.append("squat")
                    
                else:
                    squat_count = 0

                    if a_down:
                        pyautogui.keyUp("a")
                        a_down = False

                prevSum = newSum

                text_jump = f'Jumps: {jumps}'
                cv2.rectangle(frame,(20,320),(220,360),(0,200,0),-1)
                cv2.putText(frame,text_jump,(40,350),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

                text_squat = f'Squats: {squats}'
                cv2.rectangle(frame,(20,370),(220,410),(235,0,0),-1)
                cv2.putText(frame,text_squat,(40,400),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

                text_running = f'Running: {str(time_running_instant)[:4]}'
                cv2.rectangle(frame,(20,420),(280,460),(0,200,200),-1)
                cv2.putText(frame,text_running,(40,450),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

        # else: 
            # cv2.putText(frame, "Make sure your full body is in the frame", (250,250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)
        







        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        total_time_run = runlist_extended[-1]
        print("\n", total_time_run)

        heather = ["date", "total_jumps", "time_running", "total_squats"] # Columns of df
        data = [Timestamp.today().isoformat().replace("T", " ")[:16], len(imlist), total_time_run, len(squat_list)] # Timeseries , number of jumps

        # 1. step
        with open('game_history_3.csv', 'w') as file:   # "a" is to append
            # 2. step
            writer = csv.writer(file)
            # 3. step
            writer.writerow(heather)
            writer.writerow(data)

    # cap.release()
    # # Destroy all the windows
    # cv2.destroyAllWindows()




# ****************************************************************************     SAVING DATA OF MOVEMENTS *************************************************************************

# *** FIRST PAGE*****
@app.route('/')
def firstpage():
    return render_template("dash.html")

#************************ MAIN PAGE ********************** 

@app.route('/warmup', methods = ["POST", "GET"])
def warmup():

    francisco = pd.read_csv("final-data.csv")
    francisco["Calories_jumping"] = francisco["total_jumps"]/6 #adding the column calories spent jumping
    francisco["Calories_running"] = francisco["time_running"]/6.41 #adding the column calories spent jumping
    francisco["Calories_squating"] = francisco["total_squats"]/3.125 #adding the column calories spent squating 
    francisco["Total_calories_session"] = francisco["Calories_jumping"] + francisco["Calories_running"] + francisco["Calories_squating"]
    
    francisco.columns = ["Session", "# Jumps", "Time Running", "# Squats", "Calories Jumping", "Calories Running", "Calories Squating", "TOTAL CALORIES LOST"]
    laureano = francisco["TOTAL CALORIES LOST"].sum()
    df = {"Total Calories Lost with CALOR'ISTORY": laureano}
    final_df=pd.DataFrame(df, index=[0])
    
    
    martins = francisco.tail(1)
    martins.columns = ["Last Session", "# Jumps", "Time Running", "# Squats", "Calories Jumping", "Calories Running", "Calories Squating", "TOTAL CALORIES LOST"]
    # martins = martins.set_index('date')



    cleanAndPick('game_history_3.csv', 'final-data.csv')


    return render_template("main.html", final_df=[final_df.to_html(classes='data', index=False)], martins=[martins.to_html(classes="data", index=False)], titles=[final_df.columns.values, martins.columns.values])

#************************ CALORIES GRAPH PAGE ********************** 


@app.route("/calories", methods = ["POST", "GET"])
def calories():


    francisco = pd.read_csv("final-data.csv")
    francisco["Calories_jumping"] = francisco["total_jumps"]/6 #adding the column calories spent jumping
    francisco["Calories_running"] = francisco["time_running"]/6.41 #adding the column calories spent jumping
    francisco["Calories_squating"] = francisco["total_squats"]/3.125 #adding the column calories spent squating 
    francisco["Total_calories_session"] = francisco["Calories_jumping"] + francisco["Calories_running"] + francisco["Calories_squating"]
    francisco.columns = ["Session", "# Jumps", "Time Running", "# Squats", "Calories Jumping", "Calories Running", "Calories Squating", "TOTAL CALORIES LOST"]

    cleanAndPick('game_history_3.csv', 'final-data.csv')
 

    jump_calories_count('final-data.csv')
        
    return render_template("function_cal.html", tables=[francisco.to_html(classes='data', index=False)], titles=francisco.columns.values)


#************************ OPEN VIDEO PC PAGE ********************** 

@app.route("/own_video", methods = ["POST", "GET"])
def own_video():
    if request.method == "GET":
        try:
            superfitmario()
            return render_template("function_video_3.html")
        except:
            return render_template("function_video_3.html")
    else:
        return render_template("function_video_3.html")

@app.route("/video_online") # , methods = ["POST", "GET"])
def video(): 
    return render_template('function_video_3.html')


@app.route("/play_video") # , methods = ["POST", "GET"])
def video_online(): 

    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=False, port=2396)

