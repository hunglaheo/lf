import pymysql
import time, datetime

# Cấu hình kết nối MySQL
host = "localhost"
port = 3306
username = "lfgps"
password = "zHUgPyi8Kaf"
database = "linfoxgps"

while True:
    # Tạo kết nối MySQL
    conn = pymysql.connect(host=host, port=port, user=username, password=password, db=database)

    # Kết nối và lấy dữ liệu từ MySQL
    cursor = conn.cursor()
    cursor.execute("SELECT lot_id, lot_bien_so_xe FROM lf_list_of_truck WHERE lot_status < 2 AND CONCAT_WS(' ', lot_ngay_di, lot_gio_di) <= NOW() ORDER BY lot_bien_so_xe, CONCAT_WS(' ', lot_ngay_di, lot_gio_di) DESC")
    assets = cursor.fetchall()

    check_bien_so_xe = ''

    for item in assets:
        if check_bien_so_xe != '':
            if check_bien_so_xe == item[1]:
                cursor.execute("UPDATE lf_list_of_truck SET lot_status=2 WHERE lot_id='"+item[0]+"'")
                conn.commit()
            else:
                cursor.execute("UPDATE lf_list_of_truck SET lot_status=1 WHERE lot_id='"+item[0]+"'")
                conn.commit()
        else:
            cursor.execute("UPDATE lf_list_of_truck SET lot_status=1 WHERE lot_id='"+item[0]+"'")
            conn.commit()
        check_bien_so_xe = item[1]
        
    cursor.execute("UPDATE lf_list_of_truck SET lot_status=3 WHERE lot_tinh_trang_xe IS NULL")
    conn.commit()

    conn.close()
    
    print(f"Update status completed at {datetime.datetime.now()}")
    
    time.sleep(5000)
