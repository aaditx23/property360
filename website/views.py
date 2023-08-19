from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
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
    info = sessionInfo()
    if request.method=="POST":                  #if signup form filled
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['pswd1']
        password2 = request.POST['pswd2']
        psswd = None
        if password1==password2:
            psswd = password1
        else:
            messages.error(request, "Please retype the password properly")
        if '@property360.agent.com' in email:
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
        messages.success(request, 'Signup Successful')
        return render(request, 'user.html', data)
    else:
        if info[1]=="True":                        #if signup form not filled, but user logged in
            #retrieve data from database here and pass through dictionary
            getdata = 'select * from website_user where user_id=%s'
            getimg = 'select property_img from website_property where user_id_id=%s'
            temp = None
            tempimg=None
            with connection.cursor() as cursor:
                cursor.execute(getdata,[info[0]])
                temp = tuple(cursor.fetchall())[0]
                cursor.execute(getimg,[info[0]])
                tempimg=cursor.fetchall()[0][0]
            data ={
                'user_id':info[0],
                'username':temp[1],
                'email':temp[2],
                'address':temp[4],
                'saved_image':tempimg
            }
            return render(request, 'user.html', data)
        else:                                               #if signup for not filled, also user not logged in
            return render(request, 'user.html')

def home(request):
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
    login_info=info[1]
    agent_retrieve="select agent_id_id, supervisor_id from website_agent"
    agent_data=None
    with connection.cursor() as cursor:
        cursor.execute(agent_retrieve)
        agent_data = tuple(cursor.fetchall())
    print(agent_data)
    #return render(request, 'agents.html', {'data': agent_data})
    if info[1]=="True":
        return render(request, 'agents.html',{'user_id':info[0],'data': agent_data})
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
    property_retrieve = "select property_id, name, location, price, property_img from website_property"
    property_data =  None
    with connection.cursor() as cursor:
        cursor.execute(property_retrieve)
        property_data = tuple(cursor.fetchall())
    print(property_data)
    return render(request, 'property.html', {'data': property_data})

def property_img(request):
    info = sessionInfo()
    login_info = info[1]
    if request.method=='POST':
        image = request.FILES['property_img']
        print(image," image")
        with open('media/' + image.name, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        insert = 'update website_property set property_img=%s where user_id=%s'
        with connection.cursor() as cursor:
            cursor.execute(insert, (image.name,info[0]))
    if info[1]=="True":
        messages.success(request, 'Image uploaded successfully.')
        return redirect('user')
    else:
        return redirect('user')
