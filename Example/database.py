import sqlite3
file_name = "database_users.db"

def check_init():#проверяет наличие файла базы данных.
# В случае отсутствия файла, создает новый.
    try:

        with open(file_name, 'r') as file:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()

    except FileNotFoundError:
        print ("Ошибка 1. Файл базы не найден. Создаем новую базу")
    #подключение таблицы
        conn = sqlite3.connect(file_name)
        cursor = conn.cursor()
    #Создание таблицы
        cursor.execute("""CREATE TABLE users_db
                    (id integer, name text, last_name text,
                     status text, days_left) """)


def write(list_for_write):
    check_init()
    conn=sqlite3.connect(file_name)
    curs = conn.cursor()
    curs.execute("""INSERT INTO users_db
                    VALUES(?,?,?,?,?)""", list_for_write)
    conn.commit()

def check_user(chat_id):
    check_init()
    conn=sqlite3.connect(file_name)
    curs = conn.cursor()
    
    curs.execute("""SELECT * FROM users_db
                    WHERE id=?""", chat_id)
    result = curs.fetchone()
    if result == None:
        return False
    else: return True

def check_status(chat_id):
    check_init()
    conn=sqlite3.connect(file_name)
    curs = conn.cursor()
    chat_id_list = [chat_id]
    curs.execute("""SELECT * FROM users_db
                    WHERE id=?""", chat_id_list)  
    
    res_list = curs.fetchone()
    return res_list[3]
    
def update_status(chat_id, name, last_name, status, days, time):
    check_init()
    conn=sqlite3.connect(file_name)
    curs = conn.cursor()
    
    chat_id_list = [chat_id]
    list_user = [chat_id, name, last_name, status, days, time]
    
    curs.execute("DELETE FROM users_db WHERE id = ?", chat_id_list) 
    conn.commit()
    
   
    curs.execute( """INSERT INTO users_db
                    VALUES(?,?,?,?,?,?)""", list_user)
    conn.commit()

#Получаем id пользователя... зачем?
def create_id_list():
    check_init()
    conn=sqlite3.connect(file_name)
    curs = conn.cursor()
    list_of_id = []
    for row in curs.execute("""SELECT * FROM users_db id"""):
        list_of_id.append(row[0])
    #print (list_of_id)
    return list_of_id

#создаем словарь пользоватей?
def create_name_dict(id_user_list):
    #Получаем список в виде одного элемента с айди
    
    check_init()
    conn=sqlite3.connect(file_name)
    curs = conn.cursor()
    
    dict_of = {}
    ellist = []

    print(f"Id_user_list =  {id_user_list}")
    #Создаем список для отправки их функции
    list_finish = []
    list_finish.append(str(id_user_list))
    for el in id_user_list:
        ellist = [el]
        curs.execute("""SELECT name FROM users_db WHERE id = ?""", ellist)
        list_finish.append(curs.fetchone())
        
        curs.execute("""SELECT last_name FROM users_db WHERE id = ?""", ellist)
        list_finish.append(curs.fetchone())
        
        curs.execute("""SELECT status FROM users_db WHERE id = ?""", ellist)
        list_finish.append(curs.fetchone())
        

    
    print(list_finish)
    print(f"List_user =  {list_user}")
    return list_finish
    
    #row = curs.execute("""SELECT * FROM users_db WHERE id = ?""", id_user_list)
    #print(dict_of[])    

def update_user_status():
    check_init()
    conn = sqlite3.connect(file_name)
    curs = conn.cursor()
    sql = """
            UPDATE users_db
            SET status = 'WAIT'
            WHERE status = 'DONE'
            """
    curs.execute(sql)
    conn.commit()

#Создает новый словарь при запуске
def create_dict_of_list_users():
    #Проверка наличия словаря
    check_init()
    conn = sqlite3.connect(file_name)
    curs = conn.cursor()
    
    list1 = create_id_list()
    #Здесь мы должны получить словарь со всеми данными

    dict_of_users[list1] = create_name_dict()
    print(f"dict_of_users = {dict_of_users}")
    return dict_of_users
    


    # Функция возвращает словарь со списками всех пользователей.
    # В каждом списке по 4 значения
    # Функция использует функцию create_id_list для получения списка id пользователей
def create_dict_list_allinfo():
    #Проверка наличия словаря
    check_init()

    #Подключение базы данных
    conn = sqlite3.connect(file_name)
    curs = conn.cursor()
    list_of_id = []

    #Создание пустого словаря для передачи данных
    dict_finish = {}
    x=0

    #получение списка id пользователей
    id_list = create_id_list()
    
    #Сканирование всех элементов словаря
    for el in id_list:
        #список с текущим id
        num = []
        num = (el)
        #список со значениями текущего id
        list_now_id = []

        num = el
        
        curs.execute("""SELECT id FROM users_db WHERE id = ?""", (num,))
        list_now_id.append(curs.fetchone()[0])
        curs.execute("""SELECT name FROM users_db WHERE id = ?""", (num,))
        list_now_id.append(curs.fetchone()[0])
        curs.execute("""SELECT last_name FROM users_db WHERE id = ?""", (num,))
        list_now_id.append(curs.fetchone()[0])
        curs.execute("""SELECT status FROM users_db WHERE id = ?""", (num,))
        list_now_id.append(curs.fetchone()[0])
        curs.execute("""SELECT days_left FROM users_db WHERE id = ?""", (num,))
        list_now_id.append(curs.fetchone()[0])
        
    
        #Добавление элементов в словарь
        key = num

           
            
        dict_finish[key] = list_now_id 
        
        

    conn.close()    
    return(dict_finish)


        
