import pandas as pd
import numpy as np
from pandas import Timestamp
import matplotlib.pyplot as plt



def total_calories_counter():
    francisco = pd.read_csv("final-data.csv")
    francisco["Calories_jumping"] = francisco["total_jumps"]/6 #adding the column calories spent jumping
    francisco["Calories_running"] = francisco["time_running"]/6.41 #adding the column calories spent jumping
    francisco["Calories_squating"] = francisco["total_squats"]/3.125 #adding the column calories spent squating 
    francisco["Total_calories_session"] = francisco["Calories_jumping"] + francisco["Calories_running"] + francisco["Calories_squating"]
    

    
    # plt.plot(francisco["date"], francisco["Total_calories_session"], color="grey", marker="$T$")
    # plt.xlabel("date")
    # plt.ylabel("Total Calories/session")
    # plt.xticks(fontsize=5, rotation= 45)
    # plt.title("TOTAL CALORIES LOST")

    
    # plt.savefig('static/images/plot_of_total.png')

