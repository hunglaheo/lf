import requests, re
import json
from bs4 import BeautifulSoup
import urllib3, hashlib
import time, html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Tắt cảnh báo TLS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Vehicle:
    def __init__(self,Plate,VehicleTypeName,Lat,Long,Localtion,Speed, Odo="0", EngineStatus="None") -> None:
        Plate = Plate.replace(".","").replace("-","").replace(" ","").upper()
        if "LD" in Plate:
            Plate = Plate[:4]+"-"+Plate[4:]
        else:
            Plate = Plate[:3]+"-"+Plate[3:]
        self.Plate = Plate
        self.VehicleTypeName = VehicleTypeName
        try:
            Odo = int(float(Odo))
        except:
            Odo = 0
        self.Odo = str(Odo)
        self.EngineStatus = str(EngineStatus)
        self.Lat = str(Lat)
        self.Long = str(Long)
        self.Localtion = Localtion
        try:
            self.Speed = float(Speed)
        except:
            self.Speed = 0
    def GetJson(self):
        return {
            "Plate": self.Plate,
            "VehicleTypeName": self.VehicleTypeName,
            "Lat": self.Lat,
            "Long": self.Long,
            "Localtion": self.Localtion,
            "Speed": self.Speed,
            "Odo": self.Odo,
            "EngineStatus":self.EngineStatus
        }
class GPS:
    def __init__(self,taikhoan,ten,matkhau) -> None:
        self.taikhoan = taikhoan
        self.ten = ten
        self.matkhau = matkhau
    def getThpQuanlyoto(self):
        chrome_options1 = Options()
        chrome_options1.add_argument("--headless=new")
        chrome_options1.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chrome_options1)
        #driver = webdriver.Chrome()
        driver.get("http://thp.quanlyoto.vn/signin.aspx")
        driver.find_element(By.CSS_SELECTOR,"#SignIn1_txtUserId").send_keys(self.ten)
        driver.find_element(By.CSS_SELECTOR,"#SignIn1_txtPassword").send_keys(self.matkhau)
        driver.find_element(By.CSS_SELECTOR,"#SignIn1_cmdSignIn").click()
        driver.get("http://thp.quanlyoto.vn/GoogleMap/GoogleMap.aspx")
        
        driver.get("http://thp.quanlyoto.vn/GoogleMap/GoogleMap.aspx")
        time.sleep(5)
        data = driver.execute_script('''return _MapGlobal_.map.lstCarAddTmp''')
        driver.quit()
        result = []
        
        for x in data:
            dong_co_value = "None"
            tong_km_value = "None"
            address_tag = "None"
            html_string = x["content"]
            soup = BeautifulSoup(html_string, 'html.parser')
            # Tìm văn bản bắt đầu bằng "Động cơ" sau đó theo sau là dấu '=' và lấy giá trị nằm trong dấu ngoặc đơn
            dong_co_match = re.search(r"Động cơ</b>=([^,]+)", str(soup))
            if dong_co_match:
                dong_co_value = dong_co_match.group(1)
                if dong_co_value =="Tắt":
                    dong_co_value = "False"
                else:
                    dong_co_value="True"
            # Tìm văn bản bắt đầu bằng "Tổng Km" sau đó theo sau là dấu '=' và lấy giá trị nằm trong dấu ngoặc đơn
            tong_km_match = re.search(r"Tổng Km</b>=([^km]+)", str(soup))
            if tong_km_match:
                tong_km_value = tong_km_match.group(1)
            address_tag = soup.find('span', id=re.compile(r'^maps_carinfo_khuvuc_'))
            if address_tag:
                address_text = address_tag.get_text()
            if tong_km_match:
                tong_km_value = tong_km_match.group(1)
            ve = Vehicle(x["mataisoxe"],"None",x["lat"],x["lon"],address_text,"None",tong_km_value,dong_co_value)
            result.append(ve)
        return result
    def getTransinQuanlyoto(self):
        chrome_options1 = Options()
        chrome_options1.add_argument("--headless=new")
        chrome_options1.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chrome_options1)
        #driver = webdriver.Chrome()
        driver.get("http://transin.quanlyoto.vn/signin.aspx")
        driver.find_element(By.CSS_SELECTOR,"#SignIn1_txtUserId").send_keys(self.ten)
        driver.find_element(By.CSS_SELECTOR,"#SignIn1_txtPassword").send_keys(self.matkhau)
        driver.find_element(By.CSS_SELECTOR,"#SignIn1_cmdSignIn").click()
        driver.get("http://transin.quanlyoto.vn/GoogleMap/GoogleMap.aspx")
        
        driver.get("http://transin.quanlyoto.vn/GoogleMap/GoogleMap.aspx")
        time.sleep(5)
        data = driver.execute_script('''return _MapGlobal_.map.lstCarAddTmp''')
        driver.quit()
        result = []
        for x in data:
            dong_co_value = "None"
            tong_km_value = "None"
            address_tag = "None"
            html_string = x["content"]
            soup = BeautifulSoup(html_string, 'html.parser')
            # Tìm văn bản bắt đầu bằng "Động cơ" sau đó theo sau là dấu '=' và lấy giá trị nằm trong dấu ngoặc đơn
            dong_co_match = re.search(r"Động cơ</b>=([^,]+)", str(soup))
            if dong_co_match:
                dong_co_value = dong_co_match.group(1)
                if dong_co_value =="Tắt":
                    dong_co_value = "False"
                else:
                    dong_co_value="True"
            # Tìm văn bản bắt đầu bằng "Tổng Km" sau đó theo sau là dấu '=' và lấy giá trị nằm trong dấu ngoặc đơn
            tong_km_match = re.search(r"Tổng Km</b>=([^km]+)", str(soup))
            if tong_km_match:
                tong_km_value = tong_km_match.group(1)
            address_tag = soup.find('span', id=re.compile(r'^maps_carinfo_khuvuc_'))
            if address_tag:
                address_text = address_tag.get_text()
            if tong_km_match:
                tong_km_value = tong_km_match.group(1)
            ve = Vehicle(x["mataisoxe"],"None",x["lat"],x["lon"],address_text,"None",tong_km_value,dong_co_value)
            result.append(ve)
        return result
    def getDinhviht(self):
        chrome_options1 = Options()
        chrome_options1.add_argument("--headless=new")
        chrome_options1.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chrome_options1)
        driver.get("https://dinhviht.com/index.php?m=login")
        #driver.find_element(By.CSS_SELECTOR,"body > div.ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-draggable.ui-resizable > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix.ui-draggable-handle > button").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,"#txtUserName").send_keys(self.ten)
        driver.find_element(By.CSS_SELECTOR,"#txtUserPassword").send_keys(self.matkhau)
        driver.find_element(By.CSS_SELECTOR,"#tbl_login > tbody > tr:nth-child(9) > td > input").click()
        time.sleep(4)
        data = driver.execute_script('''var danhSach=[];
        for (let x in _global.devTracking.arrDevice){
    var xe ={};
    xe["name"] = _global.devTracking.arrDevice[x]["name"];
    xe["driver"] = _global.devTracking.arrDevice[x]["driver"];
    xe["driverphone"] = _global.devTracking.arrDevice[x]["driverphone"];
    xe["latitute"] = _global.devTracking.arrDevice[x]["latitude"];
    xe["longtitute"] = _global.devTracking.arrDevice[x]["longitude"];
    xe["position"] = _global.devTracking.arrDevice[x]["position"];
    xe["sim_no"] = _global.devTracking.arrDevice[x]["sim_no"];
    xe["speed"] = _global.devTracking.arrDevice[x]["real_speed"];
    xe["enginestatus"] = _global.devTracking.arrDevice[x]["input5"];                            
    danhSach.push(xe)};
return danhSach;''')
        driver.quit()
        result = []
        for x in data:
            if x["enginestatus"] == 0:
                engineStatus = "False"
            else:
                engineStatus="True"
            ve = Vehicle(x["name"],"None",x["latitute"],x["longtitute"],x["position"],x["speed"],EngineStatus=engineStatus)
            result.append(ve)
        return result
    def getCTMS(self):
        url = "http://slt.ctms.vn/Eup_Login_SOAP/Eup_Login_SOAP"
        payload = "Param={\"MethodName\":\"Login\",\"CoName\":\""+self.taikhoan+"\",\"Account\":\""+self.ten+"\",\"Password\":\""+self.matkhau+"\",\"DeviceType\":1,\"ProgVer\":\"v1.0.15.328\",\"Cust_SystemKind\":null}"
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'http://www.ctms.vn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Cookie': 'SERVER=s2'
        }
        responseLogin = json.loads(requests.request("POST", url, headers=headers, data=payload).text)
        url = "http://slt.ctms.vn/Eup_Login_SOAP/Eup_Login_SOAP"
        payload = "Param={\"custImid\":\""+responseLogin["result"][0]["Cust_IMID"]+"\",\"Cust_IMID\":\""+responseLogin["result"][0]["Cust_IMID"]+"\",\"Cust_ID\":\""+responseLogin["result"][0]["Cust_ID"]+"\",\"Team_ID\":\""+responseLogin["result"][0]["Team_ID"]+"\",\"teamId\":\""+responseLogin["result"][0]["Team_ID"]+"\",\"SESSION_ID\":\""+responseLogin["SESSION_ID"]+" \",\"Car_Unicode\":null,\"MethodName\":\"GetCarData\"}"
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'http://www.ctms.vn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Cookie': 'SERVER=s2'
        }
        responseHasPlate = json.loads(requests.request("POST", url, headers=headers, data=payload).text)
        url = "http://slt.ctms.vn/Eup_RealTime_SOAP/Eup_RealTime_SOAP"
        payload = "Param={\"custImid\":\""+responseLogin["result"][0]["Cust_IMID"]+"\",\"Cust_IMID\":\""+responseLogin["result"][0]["Cust_IMID"]+"\",\"Cust_ID\":\""+responseLogin["result"][0]["Cust_ID"]+"\",\"Team_ID\":\""+responseLogin["result"][0]["Team_ID"]+"\",\"teamId\":\""+responseLogin["result"][0]["Team_ID"]+"\",\"SESSION_ID\":\""+responseLogin["SESSION_ID"]+" \",\"Car_Unicode\":null,\"MethodName\":\"GetCarStatus\"}"
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'http://www.ctms.vn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Cookie': 'SERVER=s2'
        }
        response = json.loads(requests.request("POST", url, headers=headers, data=payload).text)

        result = []
        for x in response["result"]:
            for y in responseHasPlate["result"]:
                try:
                    if x["Car_Unicode"] == y["Car_Unicode"]:
                        ve = Vehicle(y["Car_Number"],"None",x["Log_GISY"],x["Log_GISX"],x["Address"],x["Log_Speed"])
                        result.append(ve)
                        break
                except Exception as e:
                    print(e)
        return result

    def getAdSun(self):
        url = "http://auth.adsun.vn/Auth/Login"
        payload = json.dumps({
        "username": self.ten,
        "pwd": self.matkhau
        })
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://dinhvi.adsun.vn',
        'Referer': 'https://dinhvi.adsun.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'token': 'undefined',
        'x-access-token': 'undefined'
        }

        # Tạo một Session để duy trì trạng thái của phiên làm việc
        session = requests.Session()
        # session.verify = False
        # # Gửi yêu cầu đăng nhập và kiểm tra chuyển hướng
        token = json.loads(session.post(url=url, data=payload, allow_redirects=False,headers=headers).text)
        headersnew = headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://dinhvi.adsun.vn',
        'Referer': 'https://dinhvi.adsun.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'token': token["Token"],
        'x-access-token': token["Token"]
        }
        #print(response.text)
        comanyInfo = json.loads(session.get(url="https://systemroute.adsun.vn/api/Company/GetAllCompany", data=payload, allow_redirects=False,headers=headersnew).text)
        listCompanyId=[]
        for x in comanyInfo["CompanyList"]:
            listCompanyId.append(x["Id"])
        listVehicleAll = []
        for x in listCompanyId:
            listVehicle = json.loads(session.get(url="https://systemroute.adsun.vn/api/Device/GetDeviceStatusByCompanyId?companyId="+str(x), data=payload, allow_redirects=False,headers=headersnew).text)
            for y in listVehicle["Datas"]:
                listVehicleAll.append(y)
        result = []
        for x in listVehicleAll:
            Address = json.loads(session.get(url="https://geocode.adsun.vn/Geocode/GetAddress?lat="+str(x["Location"]["Lat"])+"&lng="+str(x["Location"]["Lng"]), data=payload, allow_redirects=False,headers=headersnew).text)
            ve = Vehicle(x["Bs"],x["modeltype"],x["Location"]["Lat"],x["Location"]["Lng"],Address["Address"],x["speed"],EngineStatus=x["trangThaiMay"])
            result.append(ve)
        return result
    def getQuanlyxe(self):
        # Thông tin đăng nhập
        url = "https://quanlyxe.vn/Account.aspx/LogOn"
        payload = 'UserName='+self.ten+'&Password='+self.matkhau+'&login=%C4%90%C4%83ng%20Nh%E1%BA%ADp&RememberMe=false'
        headers = {
        'authority': 'quanlyxe.vn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://quanlyxe.vn',
        'referer': 'https://quanlyxe.vn/Account.aspx/LogOn',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        # Tạo một Session để duy trì trạng thái của phiên làm việc
        session = requests.Session()

        # Gửi yêu cầu đăng nhập và kiểm tra chuyển hướng
        response = session.post(url=url, data=payload, allow_redirects=False, headers=headers)


        # Tiếp tục gửi các yêu cầu sau đó bằng cách sử dụng session đã lưu cookie
        # Ví dụ: gửi yêu cầu đến trang khác sau khi đăng nhập
        response = session.post("http://quanlyxe.vn/Monitor.aspx/RefreshVehicle")
        vehicleList = session.post("http://quanlyxe.vn/Monitor.aspx/VehicleList")
        # Xử lý phản hồi từ trang khác ở đây
        # Ví dụ: in ra nội dung của trang khác
        result = []

        jsonRespond = json.loads(response.text)
        for x in range(len(jsonRespond["Data"])):
            if x==0:
                continue
            VehicleTypeName=""
            for y in json.loads(vehicleList.text):
                try:
                    if y[0] == jsonRespond["Data"][x][0]:
                        VehicleTypeName=y[6]
                except:
                    pass
            odo = str(jsonRespond["Data"][x][10])[:-2]
            engineStatus = "True" if jsonRespond["Data"][x][8] == 1 else "False"
            lat = str(jsonRespond["Data"][x][3])[:-6]+"."+str(jsonRespond["Data"][x][3])[-6:]
            long = str(jsonRespond["Data"][x][2])[:-6]+"."+str(jsonRespond["Data"][x][2])[-6:]
            ve = Vehicle(jsonRespond["Data"][x][32].replace("-","").replace(".",""),VehicleTypeName,lat,long,jsonRespond["Data"][x][7],jsonRespond["Data"][x][4]/100,odo,engineStatus)
            result.append(ve)
        return result
    def getDientutct(self):
        # Thông tin đăng nhập
        url = "https://dientutct.com/Logins/Login_TCT.aspx"
        payload = '__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKMTQyNzM0NTY2NA9kFgICAw9kFgRmD2QWBgIDDw8WAh4HVmlzaWJsZWhkZAIHDw8WAh4EVGV4dGVkZAIOD2QWBAIBDxYCHgRocmVmBTRodHRwczovL2FwcHMuYXBwbGUuY29tL3ZuL2FwcC90Y3QtZ3BzLTIvaWQxNDYyODc0MDk3FgICAQ8WAh4DYWx0BQdHUFMgVENUZAIDDxYCHwIFRWh0dHBzOi8vcGxheS5nb29nbGUuY29tL3N0b3JlL2FwcHMvZGV0YWlscz9pZD12bi52aWV0bmFtY25uLmdwc21vYmlsZRYCAgEPFgIfAwUHR1BTIFRDVGQCAQ9kFgQCCw8PFgIfAWVkZAIPD2QWBAIBDxYCHwIFRWh0dHBzOi8vcGxheS5nb29nbGUuY29tL3N0b3JlL2FwcHMvZGV0YWlscz9pZD12bi52aWV0bmFtY25uLmdwc21vYmlsZRYCAgEPFgIfAwUHR1BTIFRDVGQCAw8WAh8CBTRodHRwczovL2FwcHMuYXBwbGUuY29tL3ZuL2FwcC90Y3QtZ3BzLTIvaWQxNDYyODc0MDk3FgICAQ8WAh8DBQdHUFMgVENUZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBwUQY3RsMDckYnRuVmlldE5hbQUNY3RsMDckYnRuTGFvcwUTY3RsMDckY2hrUmVtZW1iZXJNZQUjY3RsMDckbm90aWNlTG9naW4kY2JWaXNpYmxlTmV4dFRpbWUFDmN0bDA4JGJ0bkxvZ2luBRJjdGwwOCRJbWFnZUJ1dHRvbjEFI2N0bDA4JG5vdGljZUxvZ2luJGNiVmlzaWJsZU5leHRUaW1lm6ZXUOBdGFHqz3U%2Fu6f5harC1yE%3D&__VIEWSTATEGENERATOR=C597E453&__EVENTTARGET=&__EVENTARGUMENT=&__EVENTVALIDATION=%2FwEdAAumMYmDAR8fOJ6OqSEY7%2Fxkl7pvftZYTqWJhs239c%2BnwZ8BymfLYzwIZR7XDhwN9pu0uFgSxBdnIuwi0EiBJw1bIX43A9gDj6hyLCM4QcndNpclYpvdeDfuTiQkwtgVBkjVI45niRLCZIY%2FiJ9Gq4XpumsRw1M4cFsN4mzMZb6GovmEWFPKes9tmEIywvjfEpMAjm5GPgEUC3BIvLSoymbs6rQQkZBLiMNrKNgKh%2BF9SHLxlHlUZbf2zrFoRaRcrUpwyF3E&ctl07%24txtLoginUserName='+self.ten+'&ctl07%24txtLoginPassword='+self.matkhau+'&ctl07%24chkRememberMe=on&ctl07%24btnLogin1=%C4%90%C4%83ng%20nh%E1%BA%ADp'
        headers = {
  'authority': 'dientutct.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
  'cache-control': 'max-age=0',
  'content-type': 'application/x-www-form-urlencoded',
  'cookie': 'CultureInfo=vi-VN; ResourceVersion=20230914v1; ASP.NET_SessionId=xaqej1wwb3lwgebi3nfwg1gz; __AntiXsrfToken=cc6008422159465386c12bfc6ed5051c',
  'dnt': '1',
  'origin': 'https://dientutct.com',
  'referer': 'https://dientutct.com/Logins/Login_TCT.aspx',
  'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

        # Tạo một Session để duy trì trạng thái của phiên làm việc
        session = requests.Session()

        # Gửi yêu cầu đăng nhập và kiểm tra chuyển hướng
        response = session.post(url=url, data=payload, allow_redirects=False, headers=headers)
        #print(response.status_code)
        # # Kiểm tra mã trạng thái của phản hồi
        # if response.status_code == 302 and 'Location' in response.headers:
        #     # Chuyển hướng đã xảy ra, bạn có thể lấy đường dẫn chuyển hướng
        #     redirect_url = response.headers['Location']
        #     print(f"Chuyển hướng đến: {redirect_url}")
        #     # Tiếp tục thực hiện các yêu cầu khác nếu cần
        # else:
        #     # Đăng nhập không thành công hoặc không có chuyển hướng
        #     print("Đăng nhập không thành công hoặc không có chuyển hướng")

        # Tiếp tục gửi các yêu cầu sau đó bằng cách sử dụng session đã lưu cookie
        # Ví dụ: gửi yêu cầu đến trang khác sau khi đăng nhập
        headers = {
  'authority': 'dientutct.com',
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
  'content-type': 'application/x-www-form-urlencoded',
  'cookie': 'CultureInfo=vi-VN; ResourceVersion=20230914v1; ASP.NET_SessionId=xaqej1wwb3lwgebi3nfwg1gz; __AntiXsrfToken=cc6008422159465386c12bfc6ed5051c',
  'dnt': '1',
  'origin': 'https://dientutct.com',
  'referer': 'https://dientutct.com/OnlineM.aspx',
  'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}
        payload='method=initListVehicleLite'
        response = json.loads(session.post("https://dientutct.com/HttpHandlers/OnlineHandler.ashx",data=payload,headers=headers).text)
        result = []
        for x in response["data"]:
            try:
                ve = Vehicle(x["_2"],"",x["_11"],x["_10"],x["_86"],x["_12"])
            except:
                ve = Vehicle(x["_2"],"",x["_11"],x["_10"],x["_86"],"0")
            result.append(ve)
        return result
    def getBinhAnh(self):
        url = "https://gps.binhanh.vn/"

        payload = '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTE0MzY3Njk0NjMPZBYCAgMPZBYCAgEPZBYGZg9kFgJmD2QWAgIBD2QWAgIBDw8WAh4EVGV4dGVkZAIBD2QWAmYPZBYCAgEPZBYCAgEPDxYCHwBlZGQCAg9kFgJmD2QWCGYPFgIeB2xpbmtBZHMFrgFodHRwOi8vYmluaGFuaC52bi9iYWZtP3V0bV9zb3VyY2U9QmluaEFuaCZ1dG1fbWVkaXVtPWJhbm5lckJBZm0mdXRtX3Rlcm09QyVFMSVCQSVBM20lMjBiaSVFMSVCQSVCRm4lMjBuaGklQzMlQUFuJTIwbGklRTElQkIlODd1JnV0bV9jb250ZW50PWJhbm5lckxlZnQmdXRtX2NhbXBhaWduPUFkUHJvZHVjdHNkAgEPFgIfAQWpAWh0dHA6Ly9iaW5oYW5oLnZuL2NhbWVyYS1oYW5oLXRyaW5oP3V0bV9zb3VyY2U9QmluaEFuaCZ1dG1fbWVkaXVtPWJhbm5lckNhbVJvdXRlJnV0bV90ZXJtPUNhbWVyYSUyMGglQzMlQTBuaCUyMHRyJUMzJUFDbmgmdXRtX2NvbnRlbnQ9YmFubmVyUmlnaHQmdXRtX2NhbXBhaWduPUFkUHJvZHVjdHNkAgMPDxYCHwBlZGQCCw9kFgQCAQ8WAh4EaHJlZgVAaHR0cHM6Ly9wbGF5Lmdvb2dsZS5jb20vc3RvcmUvYXBwcy9kZXRhaWxzP2lkPXZuLmJhZ3BzLmdwc21vYmlsZRYCAgEPFgIeA2FsdAULR1BTIEJpbmhBbmhkAgMPFgIfAgU2aHR0cHM6Ly9hcHBzLmFwcGxlLmNvbS91cy9hcHAvYmEtZ3BzL2lkMTQ2NjIwNjE3OD9scz0xFgICAQ8WAh8DBQtHUFMgQmluaEFuaGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgUFKFVzZXJMb2dpbjMkbm90aWNlTG9naW4kY2JWaXNpYmxlTmV4dFRpbWUFGFVzZXJMb2dpbjMkY2hrUmVtZW1iZXJNZQUoVXNlckxvZ2luMSRub3RpY2VMb2dpbiRjYlZpc2libGVOZXh0VGltZQUYVXNlckxvZ2luMSRjaGtSZW1lbWJlck1lBRhVc2VyTG9naW4yJGNoa1JlbWVtYmVyTWWoqph%2F%2FTpZGvTCoNOaI0W%2Fxwo3ZQ%3D%3D&__VIEWSTATEGENERATOR=CA0B0334&__EVENTVALIDATION=%2FwEdAA3E48aroPyJdyHZf824ZfW%2F5oL51HOhsK0yjO%2FazyxkA%2BBjjdA3Dg8N%2FV2000HwiozE%2BuDIMhHH48vXGrCg9KyEu%2FywhDIVWqARBaMCAe9VFAh3jmbLy0mw7qpyRmMJAnRccAprFGJV2Uy%2B4js6UeoH0CYyw0vJwAFpBvxAYNhrX3Xh8ejTDdD5XuDz7GJi%2BvxLBSSEiGR%2BlG%2F%2Bf2MoEMipRVK6TbGDFRDxsO3EPDRsi7eZ2Cpp3Jzy%2F5W7LpvlkgZHwrY%2BNgqXIJOMWfeqUKqj2cU23874SIIPYpCOJEChe0SOHLY%3D&UserLogin1%24txtLoginUserName='+self.ten+'&UserLogin1%24txtLoginPassword='+self.matkhau+'&UserLogin1%24hdfPassword=&UserLogin1%24chkRememberMe=on&UserLogin1%24btnLogin=%C4%90%C4%83ng%20nh%E1%BA%ADp&UserLogin1%24txtPhoneNumberOtp=&UserLogin1%24txtOTPClient=&UserLogin1%24hdfOTPServer=&UserLogin1%24hdfTimeoutOTP='
        headers = {
        'authority': 'gps.binhanh.vn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://gps.binhanh.vn',
        'referer': 'https://gps.binhanh.vn/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        session = requests.Session()
        # Gửi yêu cầu đăng nhập và kiểm tra chuyển hướng
        response = session.post(url=url, data=payload, allow_redirects=False, headers=headers, timeout=5)
        #print(response.status_code)
        payload='method=initListVehicleLite'
        response = json.loads(session.post("https://gps.binhanh.vn/HttpHandlers/OnlineHandler.ashx",data=payload,headers=headers).text)
        result = []
        for x in response["data"]:
            try:
                ve = Vehicle(x["_2"],"",x["_11"],x["_10"],x["_86"],x["_12"])
            except:
                ve = Vehicle(x["_2"],"",x["_11"],x["_10"],x["_86"],"0")
            result.append(ve)
        return result
    def getAdagps(self):
        url = "http://v4.adagps.com/index.php/auth/login/loginAction"
        payload = "autoLogin=on&password="+hashlib.md5(self.matkhau.encode('utf-8')).hexdigest()+"&user_name="+self.ten
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'http://v4.adagps.com',
        'Referer': 'http://v4.adagps.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
        session = requests.Session()

        response = session.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        # xử lý tiếp
        url = "http://v4.adagps.com/index.php/maps/loadTrackingDevicesAction"
        payload = "status_running=1&status_stoping=1&status_loss_gps=1&status_loss_gprs=1&status_inactive=1&status_loss_gprs=1&status_is_camera=&hdnTrackingDevicesList=&json_data=%7B%22inActiveList%22:%5B%5D,%22fixAddressList%22:%5B%5D%7D"
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Authorization': 'Bearer '+data["data"]["token"],
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': response.headers._store["set-cookie"][1],
        'DNT': '1',
        'Origin': 'http://v4.adagps.com',
        'Referer': 'http://v4.adagps.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'screen_id': 'maps'
        }
        response = json.loads(session.request("POST", url, data=payload,headers=headers).text)
        result = []
        for x in response["data"]["records"]:
            enginestatus = "True" if x["engine"] == "1" else "False"
            ve = Vehicle(x["plate"],"None",float(x["latitude"]),float(x["longitude"]),x["address"],x["speed"].split(".")[0],Odo=x["mileage"].split(".")[0],EngineStatus=enginestatus)
            result.append(ve)
        return result
    def getEposi(self):
        url = "http://fms.eposi.vn/j_spring_security_check"
        session = requests.Session()
        payload = 'j_username='+self.ten+'&j_password='+self.matkhau+''
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Origin': 'http://fms.eposi.vn',
        'Referer': 'http://fms.eposi.vn/login.action?request_locale=vi_VN',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }

        session.request("POST", url, headers=headers, data=payload)
        url = "http://fms.eposi.vn/tracking/logRecent.action"
        response=session.request("GET",url=url)
        json_input = html.unescape(response.text)
        json_input = json.loads(json_input)
        result = []
        for x in json_input:
            latlong = x[9].split()
            engineStatus = "True" if x[22] == 1 else "False"
            ve = Vehicle(x[0],x[2],latlong[0],latlong[1],x[12],x[10],EngineStatus=engineStatus)
            result.append(ve)
        return result
    def getGiamsathanhtrinh(self):
        # đăng nhập
        url = "http://giamsathanhtrinh.vn/home/Logon"
        payload = "UserName="+self.ten+"&Password="+self.matkhau+"&X-Requested-With=XMLHttpRequest"
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'http://giamsathanhtrinh.vn',
        'Referer': 'http://giamsathanhtrinh.vn/home',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
        session = requests.Session()
        response = session.request("POST", url, headers=headers, data=payload)
        url = "http://giamsathanhtrinh.vn/Home/GetCarSignalByUserId1"
        thongtin1 = json.loads(session.request("POST",url=url).text)
        url = "http://giamsathanhtrinh.vn/Home/GetCarSignalByUserId2"
        thongtin2 = json.loads(session.request("POST",url=url).text)
        result = []
        for x in thongtin1:
            for y in thongtin2:
                if x["CarID"] == y["CarID"]:
                    engineStatus = "True" if (y["Sensor"] & 1) == 1 else "False"
                    ve = Vehicle(x["CarPlate"],x["CarTypeName"],y["Lat"],y["Lng"],y["Address"],y["Speed"],EngineStatus= engineStatus)
                    result.append(ve)
        return result