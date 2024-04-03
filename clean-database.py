import pymysql
import schedule
import time, datetime

# def your_script():
host = "localhost"
port = 3306
username = "lfgps"
password = "zHUgPyi8Kaf"
database = "linfoxgps"

conn = pymysql.connect(host=host, port=port, user=username, password=password, db=database)
cursor = conn.cursor()

cursor.execute('DELETE FROM lf_list_of_truck WHERE lot_ngay_di < DATE_SUB(CURDATE(), INTERVAL 1 DAY);')# AND lot_status != 1;')

conn.commit()
conn.close()

print(f"Clean database completed at {datetime.datetime.now()}")

# # Lên lịch chạy script vào lúc 00h00p mỗi ngày
# schedule.every().day.at("00:00").do(your_script)

# while True:
    # schedule.run_pending()
    # time.sleep(10000)
    