from flask import Flask,request,render_template_string, session,redirect
from XL_3L import *
import base64

protected_routes = ['/', '/map','/user','/list-truck','/api/listUser','/api/adduser','/ncc']
Ung_dung=Flask(__name__)
Ung_dung.secret_key='123456789'
@Ung_dung.before_request
def checkSession():
    if request.path not in protected_routes:
        return
    if not session.get("user"):
        return redirect('/login',code=302)
    else:
        #update permision
        listUser = getListUser()
        for x in listUser:
            if session.get("user") == x[1]:
                session["permission"] = x[3]
@Ung_dung.route('/',methods=['GET'])
def index():
    stringHTML = readHTMLIndex()
    if (int(session.get("permission"))) & 1:
        #stringHTML = stringHTML.replace("show_ncc","none")
        return redirect('/ncc',code=302)
    if (int(session.get("permission"))) & 4:
        #stringHTML = stringHTML.replace("show_listtruck","none")
        return redirect('/list-truck',code=302)
    if (int(session.get("permission"))) & 8:
        #stringHTML = stringHTML.replace("show_map","none")
        return redirect('/map',code=302)
    if (int(session.get("permission"))) & 16:
        #stringHTML = stringHTML.replace("show_user","none")
        return redirect('/user',code=302)
    return render_template_string(stringHTML)
@Ung_dung.route('/map',methods=['GET'])
def map():
    if (int(session.get("permission"))) & 8:
        stringHTML = readHTMLMap()
        
        auth_code = base64.b64encode(session.get("user").encode('utf-8'))
        auth_code = auth_code.decode('utf-8')
        stringHTML = stringHTML.replace("AUTH_CODE",auth_code)
        
        return render_template_string(stringHTML)
    else:
        return redirect('/',code=302)
@Ung_dung.route('/user',methods=['GET'])
def user():
    if (int(session.get("permission"))) & 16:
        stringHTML = readHTMLUser()
        if not (int(session.get("permission"))) & 1:
            stringHTML = stringHTML.replace("show_ncc","none")
        if not (int(session.get("permission"))) & 4:
            stringHTML = stringHTML.replace("show_listtruck","none")
        if not (int(session.get("permission"))) & 8:
            stringHTML = stringHTML.replace("show_map","none")
        if not (int(session.get("permission"))) & 16:
            stringHTML = stringHTML.replace("show_user","none")
        return render_template_string(stringHTML)
    else:
        return redirect('/',code=302)
@Ung_dung.route('/ncc',methods=['GET'])
def ncc():
    if (int(session.get("permission"))) & 1:
        stringHTML = readHTMLNCC()
        if not (int(session.get("permission"))) & 1:
            stringHTML = stringHTML.replace("show_ncc","none")
        if not (int(session.get("permission"))) & 4:
            stringHTML = stringHTML.replace("show_listtruck","none")
        if not (int(session.get("permission"))) & 8:
            stringHTML = stringHTML.replace("show_map","none")
        if not (int(session.get("permission"))) & 16:
            stringHTML = stringHTML.replace("show_user","none")
        if (int(session.get("permission"))) & 2:
            stringHTML = stringHTML.replace("disabled","")
        return render_template_string(stringHTML)
    else:
        return redirect('/',code=302)
@Ung_dung.route('/npp',methods=['GET'])
def npp():
    stringHTML = readHTMLNPP()
    if not (int(session.get("permission"))) & 1:
        stringHTML = stringHTML.replace("show_ncc","none")
    if not (int(session.get("permission"))) & 4:
        stringHTML = stringHTML.replace("show_listtruck","none")
    if not (int(session.get("permission"))) & 8:
        stringHTML = stringHTML.replace("show_map","none")
    if not (int(session.get("permission"))) & 16:
        stringHTML = stringHTML.replace("show_user","none")
    return render_template_string(stringHTML)
@Ung_dung.route('/list-truck',methods=['GET'])
def listtruck():
    if (int(session.get("permission"))) & 4:
        stringHTML = readHTMLListTruck()
        if not (int(session.get("permission"))) & 1:
            stringHTML = stringHTML.replace("show_ncc","none")
        if not (int(session.get("permission"))) & 4:
            stringHTML = stringHTML.replace("show_listtruck","none")
        if not (int(session.get("permission"))) & 8:
            stringHTML = stringHTML.replace("show_map","none")
        if not (int(session.get("permission"))) & 16:
            stringHTML = stringHTML.replace("show_user","none")

        auth_code = base64.b64encode(session.get("user").encode('utf-8'))
        auth_code = auth_code.decode('utf-8')
        stringHTML = stringHTML.replace("AUTH_CODE",auth_code)

        return render_template_string(stringHTML)
    else:
        return redirect('/',code=302)
    
@Ung_dung.route('/login',methods=['get'])
def getLogin():
    htmlString = readHTMLLogin()
    htmlString = htmlString.replace("thong_bao","")
    return render_template_string(htmlString)
@Ung_dung.route('/login',methods=['post'])
def postLogin():
    htmlString = readHTMLLogin()
    Ten_Dang_nhap=request.form.get('username')
    Mat_khau=request.form.get('password')
    result = checkInfoLogin(username=Ten_Dang_nhap,password=Mat_khau)
    if result:
        session["user"] = Ten_Dang_nhap
        session["permission"] = result[0][3]
        session["query"] = result[0][4]
        return redirect('./',code=302)
    else:
        htmlString = htmlString.replace('thong_bao',"Sai tên đăng nhập hoặc mật khẩu!")
        return render_template_string(htmlString)
@Ung_dung.route("/logout")
def Dang_xuat():
  session['user'] = False
  return redirect("/login")
# Đoạn này xử lý để cấp API
@Ung_dung.route('/api/listUser',methods=['get'])
def apiListUser():
    dataUser = getListUser()
    dataUser = list(dataUser)
    return dataUser
@Ung_dung.route('/api/updateuser',methods=['post'])
def apiUpdateUser():
    if (int(session.get("permission"))) & 16:
        data = request.json
        result = updateUser(data)
        if(result):
            return "Thành công"
        else:
            return "Thất bại"
    else:
        return "Thất bại"
@Ung_dung.route('/api/adduser',methods=['post'])
def apiadduser():
    if (int(session.get("permission"))) & 16:
        data = request.json
        result = inserUser(data)
        if(result):
            return "Thành công"
        else:
            return "Thất bại"
    else:
        return "Thất bại"
if __name__ == '__main__':
    Ung_dung.run(host='0.0.0.0', port=8000)