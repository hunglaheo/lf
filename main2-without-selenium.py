from gpsLib import GPS
import json, time, datetime, threading
from geopy.distance import geodesic
file_lock = threading.Lock()
import mysql.connector
mydb = mysql.connector.connect(
  host = "localhost",
    port = 3306,
    username = "lfgps",
    password = "zHUgPyi8Kaf",
    database = "linfoxgps",
)
def select():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM lf_list_of_truck WHERE lot_ngay_di <= CURDATE() AND lot_ngay_di >= CURDATE() - INTERVAL 1 DAY")
    myresult = mycursor.fetchall()
    return myresult
def insert(vehicle_list):
    insertStr = "INSERT INTO `lf_list_of_truck`(`lot_bien_so_xe`, `lot_nha_phan_phoi`, `lot_ngay_di`, `lot_gio_di`, `lot_lat`, `lot_long`, `lot_tinh_trang_xe`, `lot_status`) VALUES (%s,NULL,NULL,NULL, %s,%s,NULL,NULL) "
    values = [(vehicle["Plate"], str(vehicle["Lat"]), str(vehicle["Long"])) for vehicle in vehicle_list]
    
    mycursor = mydb.cursor()
    
    try:
        mycursor.executemany(insertStr, values)
        mydb.commit()
    except Exception as e:
        print("Error inserting data:", e)
def update(vehicle_list):
    mycursor = mydb.cursor()

    # Tạo danh sách các giá trị mới (Lat, Long, Plate) cho các bản ghi tương ứng
    update_values = [(vehicle["Lat"], vehicle["Long"],vehicle["status"],vehicle["Odo"],vehicle["EngineStatus"], vehicle["Plate"]) for vehicle in vehicle_list]
    # Tạo câu SQL UPDATE cho từng bản ghi
    sql = "UPDATE lf_list_of_truck SET lot_lat = %s, lot_long = %s, lot_tinh_trang_xe = %s,lot_odo = %s,lot_ignition = %s WHERE lot_bien_so_xe = %s"
    
    try:
        for values in update_values:
            mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        print("Error updating data:", e)
def compare(listb):
    lista = select()
    existing_records = {entry[1].upper().replace(" ", ""): (entry[6], entry[7]) for entry in lista}  # Chuyển plate thành chữ hoa
    processed_plates = set()
    vehicles_to_update = []
    for x in listb:
        x_data = x.GetJson()
        plate = x_data["Plate"].upper()  # Chuyển plate trong x_data thành chữ hoa để so sánh
        if plate in existing_records:
            lat, long = existing_records[plate]
            if lat == None or long == None:
                lat = float(0)
                long = float(0)
            #if abs(float(x_data["Lat"]) - float(lat)) > 0.00005 or abs(float(x_data["Long"]) - float(long)) > 0.00005:
            if geodesic((x_data["Lat"], x_data["Long"]), (lat, long)).meters > 40:
                x_data["status"] = "Đang chạy"
                vehicles_to_update.append(x_data)
            else:
                x_data["status"] = "Dừng chạy"
                vehicles_to_update.append(x_data)

    if vehicles_to_update:
        update(vehicles_to_update)



#xử lý chính
# Đọc file input
with open("web/static/input.json",mode='r') as f:
    data = json.loads(f.read())
listAllVihicle = []
def process_data(x):
    try:
        listVihicle = getattr(GPS(x["taikhoan"], x["ten"], x["password"]), x["donvi"])()
        for z in listVihicle:
            listAllVihicle.append(z)
        x["status"] = True
    except Exception as e:
        print("Error processing data for: " + x["ten"])
        for y in data:
            if y["taikhoan"] == x["taikhoan"] and x["ten"] == y["ten"] and x["password"] == y["password"] and x["donvi"] == y["donvi"]:
                y["status"] = False
        print(e)
threads = []
start_time = time.time()

for x in data:
    thread = threading.Thread(target=process_data, args=(x,))
    threads.append(thread)
    thread.start()
#Wait for all threads to finish
for thread in threads:
    thread.join()
compare(listAllVihicle)
# for xe in listAllVihicle:
    # thongtinxe = xe.GetJson()
    # break
    # if thongtinxe["Plate"].upper()=="51C-15344":
        # print("tontai")
        # break
# with open("data.json", mode='r') as f:
#         dataAll = json.loads(f.read())
with open("input.json",mode='r') as f:
    datanew = json.loads(f.read())
for nccnew in datanew:
    for nccold in data:
        if nccnew["taikhoan"] == nccold["taikhoan"] and nccnew["ten"] == nccold["ten"] and nccnew["donvi"] == nccold["donvi"]:
            nccnew["status"] = nccold["status"]
            break
with open("input.json",mode='w') as f:
    f.write(json.dumps(datanew))
    #f.write(json.dumps(compare(dataAll, listAllVihicle)))
print("All threads have finished processing.")
end_time = time.time()  # Ghi lại thời gian kết thúc
elapsed_time = end_time - start_time  # Tính thời gian hoàn thành
print(f"Thread for completed in {elapsed_time:.2f} seconds")
#end xử lý chính
#Test
# test = GPS("vtc46451","vtc46451","112111")
# result = test.getGiamsathanhtrinh()
#print(result[0].GetJson())

#Lấy dữ liệu trong bảng ghi vào file json
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM lf_list_of_truck WHERE lot_ngay_di <= CURDATE() AND lot_ngay_di >= CURDATE() - INTERVAL 1 DAY")
myresult = mycursor.fetchall()

json_data = json.dumps(myresult, default=str, indent=4)

with open("web/static/truck.json", "w") as f:
    f.write("")
    f.write(json_data)

mydb.close()
