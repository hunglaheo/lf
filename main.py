import fastapi, json
import pymysql
import datetime
import uvicorn
import hashlib
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import re

def get_db_connection():
    # Cấu hình kết nối MySQL
    host = "localhost"
    port = 3306
    username = "lfgps"
    password = "zHUgPyi8Kaf"
    database = "linfoxgps"
    
    conn = pymysql.connect(host=host, port=port, user=username, password=password, db=database)
    
    return conn

def clean_string(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s)

# Định nghĩa API
app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class provider(BaseModel):
    donvi: str
    nvt: str
    taikhoan: str
    ten: str
    password: str
    def getJson(self):
        return {"donvi":self.donvi,"taikhoan":self.taikhoan,"ten":self.ten,"password":self.password}
class npp(BaseModel):
    manpp: str
    tennpp: str
    region: str
    lat: str
    long: str
    status: int
    def npptojson(self):
        return {"manpp":self.manpp,"tennpp":self.tennpp,"region":self.region,"lat":self.lat,"long":self.long,"status":self.status}
class InsertData(BaseModel):
    lot_bien_so_xe: str
    lot_nha_phan_phoi: str
    lot_nha_van_tai: str = ""
    lot_ngay_di: datetime.date
    lot_gio_di: datetime.time
    lot_region: str = "Miền Nam"
    lot_gio_vao: datetime.time
    lot_npp_id: str = ""

@app.post("/insert")
def insert_data(data: list[InsertData]):
    # Tạo kết nối MySQL
    connection = get_db_connection()

    # Thực hiện truy vấn
    cursor = connection.cursor()
    
    values_list = []
    flat_data = []
    
    #Lấy toàn bộ xe có trong bảng truck_master để đối chiếu
    cursor.execute("SELECT bien_so_xe FROM lf_truck_master")
    car_check = [row[0] for row in cursor.fetchall()]
    
    for item in data:
        biensoxe = item.lot_bien_so_xe.upper().replace(" ", "").replace(".", "")
        
        if 8 <= len(biensoxe) <= 10:
            lot_status = 0
            if biensoxe not in car_check:
                lot_status = 3
            
            lot_id = clean_string(item.lot_bien_so_xe+item.lot_npp_id+item.lot_ngay_di.strftime("%m-%d-%Y")+item.lot_gio_di.strftime("%H:%M"))
            
            values_list.append("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            flat_data.extend([
                #hashlib.md5((item.lot_bien_so_xe+item.lot_nha_phan_phoi+item.lot_nha_van_tai+item.lot_ngay_di.strftime("%m-%d-%Y")+item.lot_gio_di.strftime("%H:%M")).encode()).hexdigest(),
                lot_id,
                biensoxe,  
                item.lot_nha_phan_phoi,
                item.lot_nha_van_tai,
                item.lot_ngay_di,
                item.lot_gio_di,
                item.lot_region,
                item.lot_gio_vao,
                lot_status,
                item.lot_npp_id
            ])
    
    values = ", ".join(values_list)
    
    query = f"""
        INSERT INTO lf_list_of_truck 
        (lot_id, lot_bien_so_xe, lot_nha_phan_phoi, lot_nha_van_tai, lot_ngay_di, lot_gio_di, lot_region, lot_gio_vao, lot_status, lot_npp_id)  
        VALUES {values}
        ON DUPLICATE KEY UPDATE lot_gio_vao = COALESCE(VALUES(lot_gio_vao), lot_gio_vao)
        """

    cursor.execute(query, flat_data)

    connection.commit()
    connection.close()

    return {"message": "Đã thêm dữ liệu thành công"}
@app.get("/endTruck/{auth_code}")
def endTruck(auth_code: str):
    connection = get_db_connection()
    mycursor = connection.cursor()
    mycursor.execute("UPDATE lf_list_of_truck SET lot_status=2 WHERE lot_id=\""+auth_code+"\"")
    connection.commit()
    connection.close()
    #return redirect('/list-truck')
@app.get("/delTruck/{auth_code}")
def endTruck(auth_code: str):
    connection = get_db_connection()
    mycursor = connection.cursor()
    mycursor.execute("DELETE FROM lf_list_of_truck WHERE lot_id=\""+auth_code+"\"")
    connection.commit()
    connection.close()
    #return redirect('/list-truck')
@app.post("/UpdateGPSProvider")
async def UpdateGPSProvider(provider:provider):
    tontai = False
    
    with open("web/static/input.json",mode='r') as f:
        data = json.loads(f.read())
    for x in data:

        if x["donvi"] == provider.donvi:
            if x["ten"] == provider.ten:
                tontai= True
                x["donvi"] = provider.donvi
                x["nvt"] = provider.nvt
                x["ten"] = provider.ten
                x["taikhoan"] = provider.taikhoan
                x["password"] = provider.password
                with open("web/static/input.json",mode='w') as f:
                    f.write(json.dumps(data))
                return {"result":"Thành công"}
    if not tontai:
        return {"result":"Không thành công"}
@app.post("/InssertGPSProvider")
async def InssertGPSProvider(provider:provider):
    tontai = False
    with open("web/static/input.json",mode='r') as f:
        data = json.loads(f.read())
    for x in data:
        if x["donvi"] == provider.donvi:
            if x["ten"] == provider.ten:
                if x["taikhoan"] == provider.taikhoan:
                    tontai= True
                    return {"result":"Đơn vị đã tồn tại"}
    if not tontai:
        data.append(provider.getJson())
        with open("web/static/input.json",mode='w') as f:
            f.write(json.dumps(data))
    return {"result":"Thành công"}
def select(plate = "All"):
    # Tạo kết nối MySQL
    connection = get_db_connection()

    # Thực hiện truy vấn
    mycursor = connection.cursor()
    if plate != "All":
        mycursor.execute("SELECT `lot_bien_so_xe`,`lot_lat`,`lot_long`  FROM lf_list_of_truck where lot_bien_so_xe = \""+plate+"\"")
    else:
        mycursor.execute("SELECT `lot_bien_so_xe`,`lot_lat`,`lot_long` FROM lf_list_of_truck")
        
    myresult = mycursor.fetchall()  
    connection.close()
    return myresult
def selectAll():
    # Tạo kết nối MySQL
    connection = get_db_connection()

    # Thực hiện truy vấn
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM lf_list_of_truck")
    myresult = mycursor.fetchall()
    connection.close()
    return myresult
@app.get("/GetListVehicle")
async def GetListVehicle():
    return {"data":selectAll(),"sum":len(selectAll())}
@app.get("/GetListVehicleForUser/{auth_code}")
async def GetListVehicleForUser(auth_code: str):
    decoded = base64.b64decode(auth_code)

    # Tạo kết nối MySQL
    connection = get_db_connection()

    # Thực hiện truy vấn
    cursor = connection.cursor()
    
    query = "SELECT user_query FROM lf_user WHERE user_name=%s"
    cursor.execute(query, (decoded,))
    user = cursor.fetchone()
    
    vehicles = None
    
    if user:
        try:
            data = json.loads(user[0].replace("'", "\""))
            
            params = []
            conditions = []
            
            if data['lot_region'] != '':
                regions = tuple(data['lot_region'].split(","))
                conditions.append("lot_region IN %s")
                params.append(regions)

            if data['lot_npp_id'] != '':
                npp_ids = tuple(data['lot_npp_id'].split(","))
                conditions.append("lot_npp_id IN %s")
                params.append(npp_ids)
              
            if data['lot_nha_van_tai'] != '':
                carriers = tuple(data['lot_nha_van_tai'].split(","))
                conditions.append("lot_nha_van_tai IN %s")
                params.append(carriers)
                
            # Xây dựng câu truy vấn SQL dựa trên điều kiện có sẵn
            query = "SELECT * FROM lf_list_of_truck"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            query += " ORDER BY lot_region, lot_npp_id, lot_nha_van_tai, lot_ngay_di DESC, lot_gio_di"
              
            cursor.execute(query, tuple(params))
            
            vehicles = cursor.fetchall()
        except json.JSONDecodeError as e:
            print("Invalid JSON format", e)
            
    connection.close()
    return vehicles

@app.get("/GetListVehicleForMap/{auth_code}")
async def GetListVehicleForMap(auth_code: str):
    decoded = base64.b64decode(auth_code)
    # Tạo kết nối MySQL
    connection = get_db_connection()

    # Thực hiện truy vấn
    cursor = connection.cursor()
    
    query = "SELECT user_query FROM lf_user WHERE user_name=%s"
    cursor.execute(query, (decoded,))
    user = cursor.fetchone()
    
    vehicles = None
    
    if user:
        try:
            data = json.loads(user[0].replace("'", "\""))
            
            params = []
            conditions = []
            
            if data['lot_region'] != '':
                regions = tuple(data['lot_region'].split(","))
                conditions.append("lot_region IN %s")
                params.append(regions)

            if data['lot_npp_id'] != '':
                npp_ids = tuple(data['lot_npp_id'].split(","))
                conditions.append("lot_npp_id IN %s")
                params.append(npp_ids)
              
            if data['lot_nha_van_tai'] != '':
                carriers = tuple(data['lot_nha_van_tai'].split(","))
                conditions.append("lot_nha_van_tai IN %s")
                params.append(carriers)
                
            # Xây dựng câu truy vấn SQL dựa trên điều kiện có sẵn
            query = "SELECT * FROM lf_list_of_truck"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                query += " AND "
            else:                
                query += " WHERE "
                
            query += "lot_status < 3 ORDER BY lot_region DESC, lot_npp_id, lot_nha_van_tai, lot_ngay_di DESC, lot_gio_di"
            
            #print(query)
            
            cursor.execute(query, tuple(params))
            
            vehicles = cursor.fetchall()
        except json.JSONDecodeError as e:
            print("Invalid JSON format", e)
            
    connection.close()
    return vehicles

@app.get("/UpdateMasterCar")
async def UpdateMasterCar():
    from gpsLib import GPS

    # Tạo kết nối MySQL
    connection = get_db_connection()
    mycursor = connection.cursor()
    mycursor.execute("TRUNCATE lf_truck_master")
    connection.commit()
    
    with open("input.json",mode='r') as f:
        data = json.loads(f.read())
    
    for x in data:
        try:
            if x["status"] == True:
                listVihicle = getattr(GPS(x["taikhoan"], x["ten"], x["password"]), x["donvi"])()
                
                car_data = []
                values_list = []
                
                for z in listVihicle:
                    car = z.GetJson()
                    if car["Plate"] not in car_data:
                        values_list.append("(%s, %s)")
                        car_data.extend([
                            car["Plate"][:10].upper().replace("_", ""),
                            x["ten"]
                        ])
                
                values = ", ".join(values_list)
                query = f"""
                    INSERT INTO lf_truck_master 
                    (bien_so_xe, nha_van_tai)  
                    VALUES {values}
                """
                mycursor.execute(query, car_data)
                connection.commit()
        except Exception as e:
            print("Error processing data for: " + x["ten"])
        
    connection.close()

@app.get("/ListNPP")
async def ListNPP():
    connection = get_db_connection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM lf_npp")
    myresult = mycursor.fetchall()
    connection.close()
    return myresult

@app.post("/InsertNPP")
async def InsertNPP(npp:npp):
    #check xem npp đã tồn tại chưa
    connection = get_db_connection()
    mycursor = connection.cursor()
    query = f"""
        REPLACE INTO lf_npp 
        (npp_id, npp_region, npp_name, npp_lat, npp_long, npp_status)  
        VALUES {npp.manpp, npp.region, npp.tennpp, npp.lat, npp.long, npp.status}
    """
    mycursor.execute(query)
    connection.commit()
    connection.close()

    return {"result":"Thành công"}
    
@app.post("/UpdateNPP")
async def UpdateNPP(npp:npp):
    tontai = False
    with open("npp.json",mode='r') as f:
        data = json.loads(f.read())
    for x in data:
        if x["manpp"] == npp.manpp:
            tontai= True
            x["tennpp"] = npp.tennpp
            x["region"] = npp.region
            x["lat"] = npp.lat
            x["long"] = npp.long
            x["status"] = npp.status
            with open("npp.json",mode='w') as f:
                f.write(json.dumps(data))
            return {"result":"Thành công"}
    if not tontai:
        return {"result":"Không thành công"}

# Chạy API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    