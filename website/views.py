from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from website.models import User
from django.db import connection
# Create your views here.

def createUser(n):
    if len(str(n))<4:
        return ("user_"+("0"*(4-len(str(n)))) + str(n))
    else:
        return "user_"+str(n)

def createAgent(n):
    if len(str(n))<4:
        return ("agent_"+("0"*(4-len(str(n)))) + str(n))
    else:
        return "agent_"+str(n)

def createProp(n):
    if len(str(n))<4:
        return ("prop_"+("0"*(4-len(str(n)))) + str(n))
    else:
        return "prop_"+str(n)

def sessionInfo():
    retrieve_login = "select * from website_session"
    with connection.cursor() as cursor:
        cursor.execute(retrieve_login)
        temp = tuple(cursor.fetchall())[0]
        return temp
    
def setLogin(user):
    setlogin = "update website_session set user=%s, login = 'True' where user='user_0000'"
    with connection.cursor() as cursor:
        cursor.execute(setlogin, [user])

def setLogout():
    setlogout = "update website_session set user='user_0000', login = 'False' where login='True'"
    with connection.cursor() as cursor:
        cursor.execute(setlogout)
    

def login(request):
    return render(request, 'login.html')

def logout(request):
    setLogout()
    return render(request, 'home.html')


def user(request):
    usertype = "user"
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['pswd1']
        password2 = request.POST['pswd2']
        psswd = None
        if password1==password2:
            psswd = password1
        else:
            messages.error(request, "Please retype the password properly")
        if '@property360.com' in email:
            usertype = "agent"

        addrss = request.POST['address']
        data = {
            'user_name' : name,
            'user_email': email,
            'user_address': addrss
        }
        find_agent = "select user_id from website_user where user_id like 'agent%'"
        find_user = "select user_id from website_user where user_id like 'user%'"
        insert = 'insert into website_user (user_id, username, email, password, address) values (%s, %s, %s, %s, %s)'
        with connection.cursor() as cursor:
            uid = ""
            if usertype=="user":
                cursor.execute(find_user)
                user_list = tuple(cursor.fetchall())
                print(user_list)
                entries = len(user_list)
                uid = createUser((entries+1))
            else:
                cursor.execute(find_agent)
                agent_list = tuple(cursor.fetchall())
                print(agent_list)
                entries = len(agent_list)
                uid = createAgent((entries+1))
            setLogin(uid)
            cursor.execute(insert, (uid, name, email, psswd, addrss))
        data.update({'user_id': sessionInfo()[0]})
        return render(request, 'user.html', data)
    if sessionInfo()[1]=="True":
        return render(request, 'user.html', sessionInfo()[1])
    else:
        return render(request, 'user.html')

def home(request, args=None):
    user = None
    password = None
    if request.method=="POST":
        user = str(request.POST['uid'])
        password = str(request.POST['pswd'])
        retrieve_pass = "select password from website_user where user_id= %s"
        retrieve_name = "select username from website_user where user_id = %s"
        pass_data = ""
        name_data = ""
        with connection.cursor() as cursor:
            cursor.execute(retrieve_pass, [user])
            temp = tuple(cursor.fetchall())
            print("--------------------------", temp)
            pass_data = temp[0][0]
            cursor.execute(retrieve_name,[user])
            name_data = tuple(cursor.fetchall())[0][0]
        if pass_data==password:
            setLogin(user)
            info = sessionInfo()
            arg = {'user_id':info[0], 'user_name': name_data, 'user_id':info[0]}
            return render(request, 'home.html', arg)
    else:
        info = sessionInfo()
        print(info)
        if info[1]=="True":
            return render(request, 'home.html', {'user_id':info[0]})
        return render(request, 'home.html')
    

def agents(request):
    info = sessionInfo()
    if info[1]=="True":
        return render(request, 'agents.html',{'user_id':info[0]})
    else:
        return render(request, 'agents.html')

def about(request):
    info = sessionInfo()
    login_info = info[1]
    if info[1]=="True":
        return render(request, 'about.html',{'user_id': info[0]})
    else:
        return render(request, 'about.html')

def property(request):
    info = sessionInfo()
    login_info = info[1]
    property_retrieve = "select property_id, name, location, price from website_property"
    property_data =  None
    with connection.cursor() as cursor:
        cursor.execute(property_retrieve)
        property_data = tuple(cursor.fetchall())
    print(property_data)
    if info[1]=="True":
        return render(request, 'property.html', {'data': property_data,'user_id':info[0]})
    else:
        return render(request, 'property.html', {'data': property_data})