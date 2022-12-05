import pandas as pd 
def cleanAndPick(path, endpath):
    rawdata = pd.read_csv(path)
    finaldata = pd.read_csv(endpath)
    
    
    row_to_add = rawdata.tail(1)
    if (row_to_add["total_jumps"].values[0] == 0) & (row_to_add["time_running"].values[0] == 0) & (row_to_add["total_squats"].values[0] == 0):
        finaldata.drop_duplicates()
        finaldata.to_csv(endpath, index=False)

    else:
        result_df = pd.concat([finaldata, row_to_add])
        result_df = result_df.drop_duplicates()

        result_df.to_csv(endpath, index=False)



# cleanAndPick('game_history_3.csv','final-data.csv' )