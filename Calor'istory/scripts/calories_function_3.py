import pandas as pd
import numpy as np
from pandas import Timestamp
import matplotlib.pyplot as plt

def jump_calories_count(df):


    joao = pd.read_csv("final-data.csv")
    joao["Calories_jumping"] = joao["total_jumps"]/6 #adding the column calories spent jumping
    joao["Calories_running"] = joao["time_running"]/6.41 #adding the column calories spent jumping
    joao["Calories_squating"] = joao["total_squats"]/3.125 #adding the column calories spent squating 

    plt.figure(figsize=(15, 5))

    plt.subplot(131) 
    plt.plot(joao["date"], joao["Calories_jumping"], color="green", marker="$J$")
    plt.ylabel("calories lost jumping")
    plt.xlabel("date")
    plt.xticks(fontsize=5, rotation= 45)
    plt.title("JUMPING")

    plt.subplot(132) 
    plt.plot(joao["date"], joao["Calories_running"], color="blue", marker="$R$")
    plt.xlabel("date")
    plt.ylabel("calories lost running")
    plt.xticks(fontsize=5, rotation= 45)
    plt.title("RUNNING")

    plt.subplot(133)
    plt.plot(joao["date"], joao["Calories_squating"], color="orange", marker="$S$")
    plt.xlabel("date")
    plt.ylabel("calories lost squating")
    plt.xticks(fontsize=5, rotation=45)
    plt.title("SQUATING")
    
    plt.suptitle('CALORIES LOST per EXERCISE', horizontalalignment='center', verticalalignment='center_baseline', fontsize = 15, weight="bold")

    plt.savefig('static/images/3plots.png', transparent=True)



