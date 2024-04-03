import json
import requests
import pymysql
import time
from datetime import datetime
from pytz import timezone

# Lấy múi giờ Asia/Ho_Chi_Minh
ho_chi_minh = timezone('Asia/Ho_Chi_Minh') 

# Lấy thời gian hiện tại theo múi giờ Ho Chi Minh
now = ho_chi_minh.localize(datetime.now())

# Chuyển đổi thành timestamp (giây)
timestamp = int(time.mktime(now.timetuple()))

# Cấu hình kết nối MySQL
host = "localhost"
port = 3306
username = "lfgps"
password = "zHUgPyi8Kaf"
database = "linfoxgps"

# Tạo kết nối MySQL
conn = pymysql.connect(host=host, port=port, user=username, password=password, db=database)

def send_data(multiassets):
  url = "https://adamsapi.glsiweb.com/Event/SendEvents"
  
  for assets in multiassets:
      payload = json.dumps(assets)
      # print(payload)
      headers = {
        'x-api-key': 'de2816d59a58bab6747aedf4f366aab0',
        'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      # print(response.text)
      results = json.loads(response.text)
      updatestatusfalse = ''
      updatestatustrue = ''
      for key, result in enumerate(results):
        bien_so_xe = assets[key]['assetName']
        
        if result['Status'] == False:
          #Chuyển tình trạng 1 xe có lot_status là 1 sang 2
          query = f"""
            UPDATE lf_list_of_truck
            SET lot_status = 2
            WHERE lot_bien_so_xe = '{bien_so_xe}'
            AND lot_status = 1
            LIMIT 1
          """
          cursor = conn.cursor()
          cursor.execute(query)
          conn.commit()
          #print(type(assets[key]))
          #updatestatusfalse += "'"+assets[key]['assetName']+"',"
        else:
          #Chuyển tình trạng 1 xe có lot_status là 0 sang 1
          query = f"""
            UPDATE lf_list_of_truck
            SET lot_status = 1
            WHERE lot_bien_so_xe = '{bien_so_xe}'
            AND lot_status = 0
            LIMIT 1
          """
          cursor = conn.cursor()
          cursor.execute(query)
          conn.commit()
          #updatestatustrue += "'"+assets[key]['assetName']+"',"
      #print(updatestatus)
      #updatestatusfalse = updatestatusfalse.rstrip(",")
      #updatestatustrue = updatestatustrue.rstrip(",")
      # if updatestatustrue != '':
          # queryfalse = f"""
            # UPDATE lf_list_of_truck
            # SET lot_status = 2
            # WHERE lot_bien_so_xe IN ({updatestatusfalse})
          # """
          # cursor = conn.cursor()
          # cursor.execute(queryfalse)
          # conn.commit()
      # if updatestatustrue != '':
          # querytrue = f"""
            # UPDATE lf_list_of_truck
            # SET lot_status = 1
            # WHERE lot_bien_so_xe IN ({updatestatustrue})
          # """
          # cursor = conn.cursor()
          # cursor.execute(querytrue)
          # conn.commit()
    
#while True:

# Kết nối và lấy dữ liệu từ MySQL
cursor = conn.cursor()
cursor.execute("SELECT lot_bien_so_xe, lot_lat, lot_long, lot_odo, lot_ignition FROM lf_list_of_truck WHERE lot_status < 2 AND lot_lat IS NOT NULL AND lot_long IS NOT NULL GROUP BY lot_bien_so_xe")
assets = cursor.fetchall()

data = []

# Tách mỗi 50 xe một đợt 
batch_size = 50

for i, item in enumerate(assets):

  # Xác định chỉ số của mảng con
  batch_index = i // batch_size
  
  # Nếu mảng con chưa tồn tại thì khởi tạo
  if batch_index >= len(data):
    data.append([])

  data[batch_index].extend([
    {
      "senderIdentifier": "LFXVNUNLV_MIDDLEWARE",
      "deviceId": 0,
      "driverlicenseno": "0",
      "assetName": item[0],
      "timestamp": timestamp,
      "odometer": item[3],
      "ignition": item[4],
      "latitude": item[1],
      "longitude": item[2],
      "altitude": 0,
      "accuracy": 0,
      "heading": 0,
      "speed": 0,
      "internalBatteryVoltage": 0,
      "fuellevel": 0,
      "totalfuelused": 0
    }
  ])

#print(data)
# Gọi hàm gửi dữ liệu
send_data(data)

conn.close()
  # Delay 5 phút
  #time.sleep(60*5)