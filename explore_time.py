import pandas as pd
from datetime import datetime, timedelta


def time_list(edges):
    df=pd.read_csv('places.csv')
    df1=pd.read_csv('travel_matrix.csv')

    car_time=[]
    for i in range(len(edges)):
        if i==len(edges)-1:
            pass
        else:
            car_time.append(round((int(df1.iloc[edges[i]][edges[i+1]+1])*3)/10)*10)
    #print(car_time)
    
    spend_time=[]
    for i in range(len(edges)):
        spend_time.append(int(df.iloc[edges[i]]['time_spent']))
    #print(spend_time)
    start_time="10:00am"
    explore_time=[]
    for i in range(len(spend_time)):
        if i==0:
            explore_time.append([start_time,solve(start_time,spend_time[i])])
        else:
            strt=solve(explore_time[i-1][1],round(car_time[i-1]))
            explore_time.append([strt,solve(strt,spend_time[i])])
    #print(explore_time)
    return car_time,spend_time,explore_time   


def solve(s, minutes):
    
    time_instance = datetime.strptime(s, '%I:%M%p')
    
    time_instance += timedelta(minutes=minutes)
    print(time_instance)
    return time_instance.strftime('%I:%M%p').lower()


#print(time_list([23, 4, 9, 18, 17, 0, 3, 28, 27, 30, 10]))

