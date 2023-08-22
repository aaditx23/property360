from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
# from website.models import User
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
        insert_user = 'insert into website_user (user_id, username, email, password, address) values (%s, %s, %s, %s, %s)'
        insert_emp = 'insert into website_employee (employee_id, name, email, password, address) values (%s %s %s %s %s) '
        with connection.cursor() as cursor:
            uid = ""
            if usertype=="user":
                cursor.execute(find_user)
                user_list = tuple(cursor.fetchall())
                print(user_list)
                entries = len(user_list)
                uid = createUser((entries+1))
                cursor.execute(insert_user, (uid, name, email, psswd, addrss))
            else:
                cursor.execute(find_agent)
                agent_list = tuple(cursor.fetchall())
                print(agent_list)
                entries = len(agent_list)
                uid = createAgent((entries+1))
                cursor.execute(insert_agent, (uid, name, email, psswd, addrss))
            setLogin(uid)
            cursor.execute(insert, (uid, name, email, psswd, addrss))
        data.update({'user_id': sessionInfo()[0]})
        messages.success(request, 'Signup Successful')
        return render(request, 'user.html', data)
    return render(request, 'user.html')
    

def dashboard(request):
    info = sessionInfo()
    if info[1]=='True':
        if 'agent' in info[0]:
            get_agent= 'select employee_id, name, email, address from website_employee, website_agent where agent_id_id=employee_id and employee_id=%s'
            agent_temp=''
            agent=info[0]
            with connection .cursor() as cursor:
                cursor.execute(get_agent,[agent])
                agent_temp=tuple(cursor.fetchall())[0]
            agent_data={
                'user_id': info[0],
                'agentname':agent_temp[1],
                'email':agent_temp[2],
                'address':agent_temp[3],               
            }
            return render(request, 'user.html', agent_data)
            
        elif 'user' in info[0]:
            get_user = 'select user_id, username, email, address,user_img from website_user where user_id=%s'
            get_prop = 'select * from website_property where user_id_id=%s'
            user_temp = ''
            user_prop = ''
            user = info[0]
            print(user)
            with connection.cursor() as cursor:
                cursor.execute(get_user, [user])
                user_temp = tuple(cursor.fetchall())[0]
                cursor.execute(get_prop,[user])
                user_prop = tuple(cursor.fetchall())
            user_data ={
                'user_id':info[0],
                'username':user_temp[1],
                'email':user_temp[2],
                'address':user_temp[3],
                'user_img':user_temp[4],
                'prop':user_prop, 
            }
            return render(request, 'user.html', user_data)
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
    user = info[0]
    property_retrieve = "select property_id, name, location, size, type, price, status from website_property"
    property_data =  None
    with connection.cursor() as cursor:
        cursor.execute(property_retrieve)
        property_data = tuple(cursor.fetchall())
    print(property_data)
    return render(request, 'property.html', {'data': property_data, 'user_id':user})


def support(request):
    info = sessionInfo()
    login_info = info[1]
    support_retrieve = "select name, type, phone, hiring_price, support_id_id from website_support s, website_employee e where e.employee_id = s.support_id_id"
    support_data =  None
    with connection.cursor() as cursor:
        cursor.execute(support_retrieve)
        support_data = tuple(cursor.fetchall())
    if info[1]=="True":
        return render(request, 'support.html', {'data': support_data,'user_id':info[0]})
        
    else:
        return render(request, 'support.html', {'data': support_data})

def property_registration(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        agent_list = ''
        with connection.cursor() as cursor:
            cursor.execute("select employee_id,name from website_employee where employee_id like 'agent%'")
            agent_list = tuple(cursor.fetchall())
        print(agent_list)
        return render(request, 'property_registration.html', {'user_id':info[0], 'agents':agent_list})
        
    else:
        return render(request, 'property_registration.html')


def property_save(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if request.method == 'POST':
        name = request.POST['property_name']
        location = request.POST['location']
        size = request.POST['size']
        price = request.POST['price']
        status = request.POST['status']
        type = request.POST['type']
        image = request.FILES['property_img']
        prop_agent = request.POST['hired_agent']
        print(prop_agent,'-----------23423423')
        with open('media/' + image.name, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        all_properties = 'select property_id from website_property'
        with connection.cursor() as cursor:
            cursor.execute(all_properties)
            property_tuple = tuple(cursor.fetchall())
            entries = len(property_tuple)
            property_id = createProp((entries+1))

        
        property_insert = "INSERT INTO website_property(property_id, status, location, name, size, type, price, agent_id_id, user_id_id,property_img) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        with connection.cursor() as cursor:
            cursor.execute(property_insert, (property_id, status, location, name, size, type, price, prop_agent, user,image.name))
            messages.success(request, "Property Submitted")
    return redirect('dashboard')


def property_list(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    property_retrieve = "select image, property_id, name, size, type, price, agent_id_id, status from website_property where user_id_id = %s"    
    property_data =  None
    
    with connection.cursor() as cursor:
        cursor.execute(property_retrieve, user)
        property_data = tuple(cursor.fetchall())[0]

    return redirect('support')
    # if info[1]=="True":
    #     return render(request, 'user.html', {'data': property_data,'user_id':user})
    # else:
    #     return render(request, 'user.html', {'data': property_data})



 

def hire_support(request):
    
    info = sessionInfo()
    login_info = info[1]
    user = info[0]

    support = request.POST['support_id']
    print(user,support)
    
    insert_into_hires = "insert into website_hires (user_id, support_id) values (%s,%s)"
    with connection.cursor() as cursor:
        cursor.execute(insert_into_hires, (user,support))

    return redirect('support')
    
def user_edit_profile(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    
    if request.method == 'POST':
        
        retrieve_user_info = "select username, address, email, password,user_img from website_user where user_id = %s"
        user_data = None
        with connection.cursor() as cursor:
            cursor.execute(retrieve_user_info, [user])
            user_data = tuple(cursor.fetchall())[0]
        old_dict = {
            'username' : user_data[0],
            'address' : user_data[1],
            'email' : user_data[2],
            'password' : user_data[3],
            'user_img': user_data[4]
        }
        image  = request.FILES['user_image']
        with open("media/" + image.name, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        new_dict = {
            'username' : request.POST['username'],
            'address' : request.POST['address'],
            'email' : request.POST['email'],
            'password' : request.POST['password'],
            'user_pic':image.name
        }
        dict={}
        for keys in new_dict.keys():
            if len(new_dict[keys]) != 0:
                dict[keys] = new_dict[keys]
            else:
                dict[keys] = old_dict[keys]
        print(dict,old_dict,new_dict)
        update_user = 'update website_user set username = %s, email= %s,address = %s,password =%s, user_img=%s where user_id = %s '
        with connection.cursor() as cursor:
            cursor.execute(update_user, (dict['username'],dict['email'], dict['address'],dict['password'],dict['user_pic'],user))
            messages.success(request, "Profile Updated")
    return render(request, 'user_edit_profile.html', {'user_id': user})


def auction(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        return render(request, 'auction.html', {'user_id':info[0]})
    else:
        return render(request, 'auction.html')

def join_auction(request):
    pass

def agent_img(request):
    info = sessionInfo()
    login_info = info[1]
    if request.method=='POST':
        image = request.FILES['agent_img']
        print(image," image")
        with open('media/' + image.name, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        insert = 'update website_agent set agent_img=%s where agent_id=%s'
        with connection.cursor() as cursor:
            cursor.execute(insert, (image.name,info[0]))
    if info[1]=="True":
        messages.success(request, 'Image uploaded successfully.')
        return redirect('user')
    else:
        return redirect('user')

# --------------------
# use this template when you need to implement different views for different types of users
# --------------------
# usertype = "user"
# info = sessionInfo()
# if request.method=="POST":
#     if '@property360.agent.com' in email:
#         usertype = "agent"
#     elif '@property360.support.com' in email:
#         usertype = "support"

    # return redirect
    # render render(request, 'website_name.html')