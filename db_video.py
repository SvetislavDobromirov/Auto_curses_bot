def load_id_video(num_video):
    print ("load enter\n")
    dict_class = {}
    with open('video_db.txt') as f:
        print ("file open\n")
        for i in f.readlines():
            key, val = i.strip().split(':')
            key = int(key)
            dict_class[key] = val
    ret = dict_class[num_video]
    return ret

def write_new_video(video_id):
    num_line = 0
    with open('video_db.txt') as f:
        for i in f.readlines():
            num_line = num_line +1
    print (f"Количество строк в файле с видео = {num_line}")
        
    num_line = num_line - 1
    with open('video_db.txt','a') as file:
        link = f"{num_line+1}:{video_id}\n"
        file.write(link)


if __name__ == '__main__':
    print ("x")
    print(f"{load_id_video(1)}")
    print(f"{load_id_video(1)}")
    print(f"{load_id_video(1)}")
