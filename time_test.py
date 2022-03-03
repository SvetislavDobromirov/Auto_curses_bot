def time_from_sec(sec):
    hours = sec//60
    minute = sec%60
    time = f"{hours}:{minute}"
    return time


def time_to_sec(time):
    a = str()
    hour = None
    for el in time:
        if el != ":" and hour == None:
            a = f"{a}{el}"
        elif el == ":":
            hour = int(a)
            a = ""
        elif hour != None:
            a = f"{a}{el}"
    minute = int(a)
    sec = hour*60 + minute
    return sec

sec = 620
time = time_from_sec(sec)
print(time)

print(time_to_sec(time))
