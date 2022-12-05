# import the builtin time module
import time
import cv2

import mediapipe as mp
import numpy as np
import pandas as pd
import time
import csv
from pandas import Timestamp
import pyautogui

# --------- CAMERA --------------
def superfitmario():
    cap = cv2.VideoCapture(0)

    pose = mp.solutions.pose #this is the model - it's for pose detection
    pose_o = pose.Pose() # it's to process our frame
    drawing = mp.solutions.drawing_utils #draws all the points and lines in the body


    jumps = 0
    imlist = []
    count = 0
    position = None

    runlist_extended = []
    time_running_instant = 0

    # *********************** COMMAND INSTRUCTIONS **************************
    l_down = False
    d_down = False
    s_down = False
    a_down = False

    def isJump(lst):
        if (lst[0].y*480)<=10:  # [0] is the nose position, y*480 is to de-normalize, < 60 to go up to count jump
            position = "up"
            return True
        return False

    def isBackward(lst):
        if (lst[16].y*480) <= 220 and (lst[15].y*480) <= 220:
            if abs(finalres[15].x*640 - finalres[16].x*640) > 200:
                return True
            return False

    def isfront(lst):
        if abs(finalres[15].x*640 - finalres[16].x*640) < 120:
            if (lst[16].y*480) > 1 and (lst[15].y*480) > 1:
                return True
            return False

    #  and lst[16].y*480)

    def inFrame(lst): # lst is the list of all the landmark positions
        if lst[24].visibility > 0.7 and lst[23].visibility > 0.7: #means it is visible in the frame
            return True #if all these landmarks/points are visible
        return False


    
    while(True):      
        ret, frame = cap.read() # in this video he has "_, frm =" 
        res = pose_o.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        drawing.draw_landmarks(frame, res.pose_landmarks, pose.POSE_CONNECTIONS) # this is to draw all the landmark positions in the video  

        # now we'll write code to check if the user is in the frame or not

        if res.pose_landmarks:
            finalres = res.pose_landmarks.landmark #this will be the list of all the landmarks (points)

        # ******* MAIN LOGIC ********* to check if the user is in the frame

        # now we're going to check if all those landmark positions are visible in the frame or not
        if res.pose_landmarks and inFrame(finalres): #this will return true if the landmarks we want are in the frame, otherwise return False
            # cv2.putText(frame, "You're good to PLAY", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # user in frame check done   

                
            # **********************************  COUNTING THE JUMPS ***************************************************
            if isJump(finalres):
                cv2.putText(frame, "jumping", (50,150), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
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


            # **********************************  BACKWARDS  ***************************************************
            if isBackward(finalres):
                cv2.putText(frame, "backwards", (300,300), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            
                if not(a_down):
                    pyautogui.keyDown("a")
                    a_down=True
            
            else:
                if (a_down):
                    pyautogui.keyUp("a")
                    a_down=False

            # **********************************  RUNNING  ***************************************************

            start = time.time()

            if isfront(finalres):
                cv2.putText(frame, "running", (300,300), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

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
                time_running_instant += (total_time * 1.76)
                print(time_running_instant)
                runlist_extended.append(time_running_instant)



        else: # put text on the screen to make sure body is in the frame
            cv2.putText(frame, "Make sure your full body is in the frame", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
                #(50,100) -> is the position of the text
                #the comes the font of the text
                # 1 is the font size
                #(0,0,255) is the color  


        cv2.imshow('frame', frame) # in the video he has ("window", frm)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


    print(imlist)
    print(len(imlist))

    total_time_run = runlist_extended[-1]
    print("\n", total_time_run)






    # cap = cv2.VideoCapture(0)
    # pose = mp.solutions.pose #this is the model - it's for pose detection
    # pose_o = pose.Pose() # it's to process our frame
    # drawing = mp.solutions.drawing_utils #draws all the points and lines in the body
    # # ---------- RUNNING LOGIC ----------

    # isInit = False
    # prevSum = 0
    # global sum_list
    # sum_list = np.array([0.0]*5)

    # def findSum(lst):
    #     sm = 0
    #     sm = lst[26].y*640 + lst[25].y*640 + lst[0].y*640 + lst[23].y*640 + lst[24].y*640 
    #     return sm

    
    # def push(sm):
    #     global sum_list
    #     for i in range(3, -1, -1):
    #         sum_list[i+1] = sum_list[i]

    #     sum_list[0] = abs(sm - prevSum)


    # def isRunning(lst):
    #     if (lst[20].y*480 and lst[19].y*480 >= lst[24].y*480 and lst[23].y*480):
    #         # if (lst[24].y*480) < 350 and (lst[23].y*480) < 350:
    #         if (lst[0].y*480)>=10:
    #             sm = 0
    #             for i in sum_list:
    #                 sm = sm + i

    #             if sm > 50:
    #                 return True 
    #             return False


    # # --------- KEYBOARD KEYS --------
    # l_down = False
    # d_down = False
    # a_down = False

    # # --------- COUNTERS & LISTS ----------
    # jumps = 0
    # imlist = []
    # count = 0
    # position = None
    # squats = 0
    # squat_count = 0
    # squat_list = []

    # runlist_extended = [0]
    # time_running_instant = 0

    # # --------- FUNCTIONS -----------

    # def inFrame(lst): # lst is the list of all the landmark positions
    #     if lst[24].visibility > 0.7 and lst[23].visibility > 0.7 and lst[15].visibility>0.7: #means it is visible in the frame
    #         position = "up"
    #         return True #if all these landmarks/points are visible
    #     return False

    # def isBackward(lst):
    #     if (lst[24].y*480) > 400 and (lst[23].y*480) > 400:
    #         return True
    #     return False

    # def isJump(lst):
    #     if (lst[0].y*480)<=10:  # [0] is the nose position, y*480 is to de-normalize, < 60 to go up to count jump
    #         return True
    #     return False

    # while(True):

    #     ret, frame = cap.read()

    #     cv2.namedWindow("Resize", cv2.WINDOW_NORMAL)
    #     cv2.resizeWindow("Resize", 900, 800)

    #     res = pose_o.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


    #     if res.pose_landmarks:
    #         finalres = res.pose_landmarks.landmark

    #     drawing.draw_landmarks(frame, res.pose_landmarks, pose.POSE_CONNECTIONS)

    #     if res.pose_landmarks and inFrame(finalres):
    # # ********************************************************** RUNNING WITH MOVEMENT *******************************************************
            
    #         if not(isInit):
    #             prevSum = findSum(finalres)
    #             isInit = True
    #         else:
    #             newSum = findSum(finalres)
    #             push(newSum)

    #             start = time.time()
    #             if isRunning(finalres): ##  running down the d key
    #                 cv2.putText(frame, "Running", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
    #                 if not(d_down):                  # --> commands to run
    #                     pyautogui.keyDown("d")
    #                     d_down=True            
    #                 else:
    #                     if (d_down):                  # --> commands to statick
    #                         pyautogui.keyUp("d")
    #                         d_down=False
                
    #             end = time.time()
    #             total_time = end - start
    #             if total_time > 0:
    #                 time_running_instant += (total_time * 1.70) #1.70 is he constant for real time running
    #                 print(time_running_instant)
    #                 runlist_extended.append(time_running_instant)

    #             # else: 
    #             #     cv2.putText(frame, "You are still", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)


    # # ****************************************************************** RUNNING ***********************************************************************

    #             # start = time.time()

    #             # if isForward(finalres):
    #             #     cv2.putText(frame, "running", (300,300), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    #             #     if not(d_down):                  # --> commands to run
    #             #             pyautogui.keyDown("d")
    #             #             d_down=True            
    #             #     else:
    #             #         if (d_down):                  # --> commands to statick
    #             #             pyautogui.keyUp("d")
    #             #             d_down=False

    #             # end = time.time()
    #             # total_time = end - start
    #             # if total_time > 0:
    #             #     time_running_instant += (total_time * 1.70)
    #             #     print(time_running_instant)
    #             #     runlist_extended.append(time_running_instant)

    #     # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ JUMPING +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #             if isJump(finalres):
    #                 cv2.putText(frame, "jumping", (50,150), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    #                 count += 1

    #                 if not(l_down):                  # --> commands to jump
    #                     pyautogui.keyDown("l")
    #                     l_down=True

    #                 if count > 0 and count < 2 :
    #                     jumps += 1
    #                     print(jumps)
    #                     imlist.append('jump')

    #             else:
    #                 cv2.putText(frame, "not jumping", (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    #                 count = 0

    #                 if l_down:                       # --> commands to NOT jump
    #                     pyautogui.keyUp("l")
    #                     l_down=False

    #     # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ SQUATING +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #             if isBackward(finalres):
    #                 cv2.putText(frame, "going back", (300,300), cv2.FONT_HERSHEY_PLAIN, 1, (255,6,89), 2)
    #                 squat_count += 1

    #                 if not(a_down):
    #                     pyautogui.keyDown("a")
    #                     a_down=True

    #                 if squat_count > 0 and squat_count < 2 :
    #                     squats += 1
    #                     print(squats)
    #                     squat_list.append("squat")
                    
    #             else:
    #                 squat_count = 0

    #                 if a_down:
    #                     pyautogui.keyUp("a")
    #                     a_down = False

    #             prevSum = newSum

    #             text_jump = f'Jumps: {jumps}'
    #             cv2.rectangle(frame,(20,320),(220,360),(255,0,0),-1)
    #             cv2.putText(frame,text_jump,(40,350),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)

    #             text_squat = f'Squats: {squats}'
    #             cv2.rectangle(frame,(20,370),(220,410),(255,0,0),-1)
    #             cv2.putText(frame,text_squat,(40,400),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)

    #             text_running = f'Running: {str(time_running_instant)[:4]}'
    #             cv2.rectangle(frame,(20,420),(280,460),(255,0,0),-1)
    #             cv2.putText(frame,text_running,(40,450),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)

    #     else: 
    #         cv2.putText(frame, "Make sure your full body is in the frame", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
        


    #     cv2.imshow("Resize", frame) # in the video he has ("window", frm)
    #     # cv2.setWindowProperty("Resize", cv2.WND_PROP_TOPMOST, 1)

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break



    # cap.release()
    # # Destroy all the windows
    # cv2.destroyAllWindows()


    # total_time_run = runlist_extended[-1]
    # print("\n", total_time_run)


    #                                         # # Grab Currrent Time Before Running the Code
    #                                         # start = time.time()




    #                                         # end = time.time()

    #                                         # #Subtract Start Time from The End Time
    #                                         # total_time = end - start
    #                                         # print("\n"+ str(total_time))

    # # ****************************************************************************     SAVING DATA OF MOVEMENTS *************************************************************************
    # heather = ["date", "total_jumps", "time_running", "total_squats"] # Columns of df
    # data = [Timestamp.today().isoformat().replace("T", " ")[:16], len(imlist), total_time_run, len(squat_list)] # Timeseries , number of jumps

    # # 1. step
    # with open('game_history_3.csv', 'a') as file:   # "a" is to append
    #     # 2. step
    #     writer = csv.writer(file)
    #     # 3. step
    #     # writer.writerow(heather)
    #     writer.writerow(data)

