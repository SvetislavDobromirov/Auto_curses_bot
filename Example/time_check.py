import datetime
import time

def time_check(goal_time):
    goal_hour = goal_time[0:2]
    goal_minute = goal_time[3:5]
    
    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    current_time = str(current_time)
    hour = current_time[0:2]
    minute = current_time[3:5]
    second = current_time[6:8]
    second = int(second)
    
    if hour == goal_hour and minute == goal_minute:
        return True
    else:
        return False
    

