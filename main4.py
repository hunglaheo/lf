# File này dùng để lấy trạng thái xe đang chạy. Sau đó ghi nhận lại. Nếu quá 4 tiếng thì sẽ thêm vô DB
import json, time, datetime, threading
from geopy.distance import geodesic
file_lock = threading.Lock()

import pymysql
# Cấu hình kết nối MySQL
host = "localhost"
port = 3306
username = "lfgps"
password = "zHUgPyi8Kaf"
database = "linfoxgps"

mydb = pymysql.connect(host=host, port=port, user=username, password=password, db=database)

def select():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM lf_list_of_truck WHERE lot_tinh_trang_xe = 'Đang chạy' AND lot_ngay_di <= CURDATE() AND lot_ngay_di >= CURDATE() - INTERVAL 1 DAY")
    myresult = mycursor.fetchall()
    return myresult
data = select()
def insert(info):
    insertStr = "INSERT INTO `lf_list_over_4h`( `plate`, `start_time`, `end_time`) VALUES ("+"'"+info["BienSoXe"]+"'"+","+"'"+str(info["Batdau"])+"'"+","+"'"+str(info["Ketthuc"])+"'"+") "
    print(insertStr)
    mycursor = mydb.cursor()
    try:
        mycursor.execute(insertStr)
        mydb.commit()
    except Exception as e:
        print("Error inserting data:", e)
with open("xedangchay.json","r") as f:
    listDangchay = json.loads(f.readline())
def update(info):
    mycursor = mydb.cursor()

    # Tạo danh sách các giá trị mới (Lat, Long, Plate) cho các bản ghi tương ứng
    # Tạo câu SQL UPDATE cho từng bản ghi
    updateStr= "UPDATE lf_list_over_4h SET end_time = "+str(info["Ketthuc"] )+" WHERE plate = "+ info["BienSoXe"] +" AND start_time =  "+info["Batdau"]+";"
    
    try:
        mycursor.execute(updateStr)
        mydb.commit()
    except Exception as e:
        print("Error updating data:", e)
while True:
    for x in listDangchay:
        tontai = False
        for y in data:
            y=list(y)
            if x["BienSoXe"] == y[1]:
                tontai = True
                break
        if not tontai:
            listDangchay.remove(x)
    for x in data:
        x = list(x)
        tontai = False
        for y in listDangchay:
            if x[1] == y["BienSoXe"]:
                tontai=True
                break
        if not tontai:
            newX = {}
            newX["BienSoXe"] = x[1]
            newX["Batdau"] = time.time()
            newX["Status"] = False
            newX["Count"] = 0
            listDangchay.append(newX)
        else:
            for y in listDangchay:
                if y["BienSoXe"] == x[1]:
                    if time.time() - y["Batdau"]  > 14400:
                        y["Status"] = True
                        y["Count"] = y["Count"] + 1
                    y["Ketthuc"] = time.time()
                    if y["Status"] == True and y["Count"] == 1:
                        insert(y)
                    if y["Status"] == True and y["Count"] > 1:
                        update(y)
    with open("xedangchay.json","w") as f:
        f.writelines(json.dumps(listDangchay))
    time.sleep(300)