import pymysql
import hashlib

def get_db_connection():
    # Cấu hình kết nối MySQL
    host = "localhost"
    port = 3306
    username = "lfgps"
    password = "zHUgPyi8Kaf"
    database = "linfoxgps"
    
    conn = pymysql.connect(host=host, port=port, user=username, password=password, db=database)
    
    return conn

def string_to_sha256(input_string):
    # Tạo một đối tượng băm SHA-256
    sha256 = hashlib.sha256()

    # Chuyển đổi chuỗi đầu vào thành dạng bytes (ví dụ: utf-8)
    input_bytes = input_string.encode('utf-8')

    # Cập nhật đối tượng băm với dữ liệu đầu vào
    sha256.update(input_bytes)

    # Lấy giá trị băm SHA-256 dưới dạng chuỗi hex
    sha256_hash = sha256.hexdigest()

    return sha256_hash
def inserUser(info):
    ten=info["ten"]
    password = string_to_sha256(info["password"])
    khuvuc = info["khuvuc"]
    masonpp = info["masonpp"]
    nvt = info["nvt"]
    permission = info["permission"]
    listUser = getListUser()
    userExits = False
    for x in listUser:
        if x[1] == ten:
            userExits = True
        
    if userExits or password == "":
        return False
    else:
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        querystring =  str({'lot_region':khuvuc,'lot_npp_id':masonpp,'lot_nha_van_tai':nvt})
        sql = 'INSERT INTO lf_user (user_name, user_password,user_permission, user_query) VALUES (%s, %s,%s, %s)'
        val = (ten,password,permission,querystring)
        mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        if(mycursor.rowcount!= 0):
            return True
        else:
            return False
def updateUser(info):
    mydb = get_db_connection()
    ten=info["ten"]
    khuvuc = info["khuvuc"]
    masonpp = info["masonpp"]
    nvt = info["nvt"]
    permission = info["permission"]
    mycursor = mydb.cursor()
    querystring =  str({'lot_region':khuvuc,'lot_npp_id':masonpp,'lot_nha_van_tai':nvt})
    if info["password"] !="":
        password = string_to_sha256(info["password"])
        sql = 'UPDATE lf_user SET user_password = %s,user_permission = %s,user_query = %s WHERE user_name = %s'
        val = (password,permission,querystring,ten)
    else:
        sql = 'UPDATE lf_user SET user_permission = %s,user_query = %s WHERE user_name = %s'
        val = (permission,querystring,ten)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    if(mycursor.rowcount!= 0):
        return True
    else:
        return False
def getListUser():
    mydb = get_db_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM lf_user")
    myresult = mycursor.fetchall()
    #mydb.commit()
    mydb.close()
    return myresult
def checkInfoLogin(username, password):
    mydb = get_db_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM lf_user WHERE user_name = '"+username+"' AND user_password = '"+string_to_sha256(password)+"'")
    myresult = mycursor.fetchall()
    mydb.close()
    return myresult
def readHTMLUser():
    with open("templates/user.html",encoding="utf-8") as f:
        htmlString = f.read()
    return htmlString
def readHTMLMap():
    with open("templates/map.html",encoding="utf-8") as f:
        htmlString = f.read()
    return htmlString
def readHTMLNCC():
    with open("templates/ncc.html",encoding="utf-8") as f:
        htmlString = f.read()
    return htmlString
def readHTMLNPP():
    with open("templates/npp.html",encoding="utf-8") as f:
        htmlString = f.read()
    return htmlString
def readHTMLListTruck():
    with open("templates/list-truck.html",encoding="utf-8") as f:
        htmlString = f.read()
    return htmlString
def readHTMLIndex():
    with open("templates/index.html",encoding="utf-8") as f:
        htmlString = f.read()
    return htmlString
def readHTMLLogin():
    with open("templates/login.html",encoding="utf-8") as f:
        htmlString = f.read()
    return htmlString
