vi = 5
vi0 = "https://youtu.be/NlM6HC4flaQ"
vi1 = "https://youtu.be/VjQkInMG8F0"
vi2 = "https://youtu.be/dpNaZRy-qB4"
vi3 = "https://youtu.be/sGNjOeVZ8dI"
vi4 = "https://youtu.be/XrjUM1PFacw"
vi5 = "https://youtu.be/zc9Zlpg4Cd4"
vid = (vi0, vi1, vi2, vi3, vi4, vi5)



    
##def main():
##    dict_class = {1:10, 2:20, 3:30}
##    write_dict(dict_class)
##    print (type(dict_class[1]))
##    load_dict()
    
def load_dict():
    dict_class = {}
    with open('dict.txt') as f:
        for i in f.readlines():
            key, val = i.strip().split(':')
            key = int(key)
            val = int(val)
            dict_class[key] = val
    #print (dict_class)
    return dict_class

def write_dict(dict_class):
    with open('dict.txt','w') as out:
        for key,val in dict_class.items():
            out.write('{}:{}\n'.format(key,val))
            
##if __name__ == '__main__':
##    main()
