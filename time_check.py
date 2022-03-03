import datetime
import time

def time_check(goal_time):
    goal_time = goal_time.split(":")
    
    goal_hour = int(goal_time[0])
    goal_minute = int(goal_time[1])
    goal_fulltime_minute =  (goal_hour*60) + goal_minute
    
    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    current_time = str(current_time)

    current_time = current_time.split(":")
    hour = int(current_time[0])
    minute = int(current_time[1])
    current_fulltime_minute = (hour*60) + minute
    #print(f"Timenow = {goal_fulltime_minute}")
    #print(f"Timecurrent = {current_fulltime_minute}")
    
    
    if goal_fulltime_minute == current_fulltime_minute:
        return True
    else:
        return False
    

def hour_2_check(start_time):
    start_time = start_time.split(":")
    start_hour = start_time[0]
    start_minute = start_time[1]
    in_minute_start_time = (int(start_hour)*60) + int(start_minute)

    minute_finish_time = in_minute_start_time + 120

    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    current_time = str(current_time)
    current_time = current_time.split(":")
    hour = current_time[0]
    minute = current_time[1]
    in_minute_current_time = (int(hour)*60)+int(minute)
    a = in_minute_current_time - in_minute_start_time
    print(a)
    if a <120:
        return True
    else:
        return False


def time_comparison(time):
    time = time.split(":")
    hour = time[0]
    minute = time[1]
    in_minute_time = (int(hour)*60) + int(minute)

    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    current_time = str(current_time)
    current_time = current_time.split(":")
    hour = current_time[0]
    minute = current_time[1]
    in_minute_current_time = (int(hour)*60)+int(minute)
    f = "future"
    p = "past"
    if in_minute_time > in_minute_current_time:
        return f
    else: return p

def split(time):
    time = time.split(":")
    #print(time)
    hour= int(time[0])
    minute = int(time[1])
    #print(f"{hour}:{minute}")

def time_now():   
    time = str(datetime.datetime.now().time())
    time = time.split(".")[0]
    return time
