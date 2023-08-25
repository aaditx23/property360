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
        

def fetch_property(request):
    info = sessionInfo()
    user = info[0]
    if 'user' in user:
        if request.method == "POST":
            property_id = request.POST['property_id']
            request.session['property_id'] = property_id
        return redirect('property_edit_info')
    elif "agent" in user:
        if request.method == 'POST':
            property_id = request.POST['property_id']
            update_status = "update website_property set status = 'for sale' where property_id = %s "
            with connection.cursor() as cursor:
                cursor.execute(update_status, [property_id])
                messages.success (request, 'Property Added To Market')
            request.session['property_id'] = property_id
        return redirect('property')

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
                cursor.execute(insert_emp, (uid, name, email, psswd, addrss))
            setLogin(uid)
            
        data.update({'user_id': sessionInfo()[0]})
        messages.success(request, 'Signup Successful')
        return render(request, 'user.html', data)
    return render(request, 'user.html')




def agent_dashboard(request):
    info = sessionInfo()
    user = info[0]
    if info[1]=='True':
        return render(request, 'agent_dashboard.html',{'user':user})
    # return render(request, 'user.html')


def dashboard(request):
    info = sessionInfo()
    if info[1]=='True':
        if 'agent' in info[0]:
            get_agent= 'select employee_id, name, email, address, phone, supervisor_id, agent_img from website_employee, website_agent where agent_id_id=employee_id and employee_id=%s'
            get_prop = 'select * from website_property where agent_id_id=%s'
            agent_temp=''
            agent_prop = ''
            agent=info[0]
            with connection .cursor() as cursor:
                cursor.execute(get_agent,[agent])
                agent_temp=tuple(cursor.fetchall())[0]
                cursor.execute(get_prop,[agent])
                agent_prop = tuple(cursor.fetchall())
            agent_data={
                'agent_id': info[0],
                'agentname':agent_temp[1],
                'email':agent_temp[2],
                'address':agent_temp[3],               
                'phone' : agent_temp[4],
                'supervisor_id' : agent_temp[5],
                'agent_img': agent_temp[6],
                'prop': agent_prop,
            }
            
            print(agent_data)
            # return render(request, 'agent_dashboard.html',  agent_data)
            return render(request, 'agent_dashboard.html',  {'user_id':info[0],'data': agent_data})
            
        
         



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
                print(user_temp)
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
            print(user_data)
            return render(request, 'user.html', user_data)
    return render(request, 'user.html')



def home(request):
    user = None
    password = None
    if request.method=="POST":
        user = request.POST['uid']
        retrieve_pass = ''
        retrieve_name = ''
        if 'user' in user:
            retrieve_pass = "select password from website_user where user_id= %s"
            retrieve_name = "select username from website_user where user_id = %s"
        elif 'agent' in user:
            retrieve_pass = "select password from website_employee where employee_id= %s"
            retrieve_name = "select name from website_employee where employee_id = %s"
        password = request.POST['pswd']
        pass_data = ""
        name_data = ""
        with connection.cursor() as cursor:
            cursor.execute(retrieve_pass, [user])
            pass_data = tuple(cursor.fetchall())[0][0]
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
   #EXCLUDED AGENT_0000
    agent_retrieve="select agent_id_id, supervisor_id ,name, email ,phone, address from website_agent,website_employee where agent_id_id =employee_id and agent_id_id like 'agent%' and agent_id_id <> 'agent_0000'"
    agent_data=None
    with connection.cursor() as cursor:
        cursor.execute(agent_retrieve)
        agent_data = tuple(cursor.fetchall())
    print(agent_data)
    if info[1]=="True":
        return render(request, 'agents.html',{'user_id':info[0],'data': agent_data})
    else:
        
        return render(request, 'agents.html' , {'data': agent_data})

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
    
    property_retrieve = "select property_id, name,agent_id_id, location, size, type, price, status from website_property where status = 'for sale'"
    property_data =  None
    with connection.cursor() as cursor:
        cursor.execute(property_retrieve)
        property_data = tuple(cursor.fetchall())
    print(property_data)

    if info[1] == 'True':
        return render(request, 'property.html', {'data': property_data, 'user_id':user})
    
    return render(request, 'property.html', {'data': property_data})

def support(request):
    info = sessionInfo()
    login_info = info[1]
    support_retrieve = "select name, type, phone, hiring_price, support_id from website_support s, website_employee e where e.employee_id = s.support_id"
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
    
def propertyId_submit(request):
    info=sessionInfo()
    login_info= info[1]
    user =info[0]
    if info[1]=="True":
        if request.method=='POST':
            agent_id = request.POST['agent_id']
            property_list = ''
            find_property = 'select property_id from website_property where user_id_id=%s and agent_id_id<>%s '
            with connection.cursor() as cursor:
                cursor.execute(find_property,(user,agent_id))
                property_list = tuple(cursor.fetchall())
            dic = {
                'user_id':info[0],
                'agent_id':agent_id,
                'properties':property_list
                }
            return render(request, 'propertyId_submit.html', dic )
    else:
        return render (request,'propertyId_submit.html')
    
def hire_agent(request):
    info=sessionInfo()
    login_info=info[1]
    user=info[0]
    if request.method=='POST':
        password= request.POST['confirm_password']
        property_id=request.POST['prop_id']
        agent_id=request.POST['agent_id']
        password1=''
        user_id=''
        retrieve_pass= 'select password from website_user where user_id= %s'
        retrieve_user_id= 'select user_id_id from website_property where property_id=%s'
        update_agent= 'update website_property set agent_id_id=%s where property_id=%s'
        insert_seller= 'insert into website_seller (seller_id_id ,agent_id_id) values (%s,%s)'
        with connection.cursor() as cursor:
            cursor.execute(retrieve_pass, [user])
            password1= tuple(cursor.fetchall())[0][0]
            cursor.execute(retrieve_user_id,[property_id])
            user_id=tuple(cursor.fetchall())[0][0]
            print(user_id)
            print(agent_id)
            if password==password1 and user==user_id:
                cursor.execute(update_agent, (agent_id,property_id))
                cursor.execute(insert_seller,(user,agent_id))
                messages.success(request, "Agent_Id Updated")
    return redirect('agents')


                

                
                
        

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

        
        property_insert = "INSERT INTO website_property(property_id, status, location, name, size, type, price, agent_id_id, user_id_id, property_img) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
    if '0000' in info[0]:
        return redirect('login')
    
    login_info = info[1]
    user = info[0]

    support = request.POST['support_id']
    property = request.POST['property_id']
    print(user,support,property)
    
    insert_into_hires = "insert into website_hires (user_id_id, support_id_id) values (%s,%s)"
    insert_into_maintains = "insert into website_maintains (property_id_id,support_id_id) values (%s,%s)"
    with connection.cursor() as cursor:
        cursor.execute(insert_into_hires, (user,support))

    return redirect('support')


    
def user_edit_profile(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if 'user' in user:
            
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
                'user_img':image.name
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
                cursor.execute(update_user, (dict['username'],dict['email'], dict['address'],dict['password'],dict['user_img'],user))
                messages.success(request, "Profile Updated")
            return redirect('dashboard')

        return render(request, 'user_edit_profile.html', {'user_id': user})
    
    elif 'agent' in user:
        if request.method == 'POST':
            
            retrieve_agent_info = "select name, email, address,password, phone, agent_img from website_employee, website_agent where agent_id_id=employee_id and employee_id= %s"
            agent_data = None
            with connection.cursor() as cursor:
                cursor.execute(retrieve_agent_info, [user])
                agent_data = tuple(cursor.fetchall())[0]
            old_dict = {
                'agentname' : agent_data[0],
                'email' : agent_data[1],
                'address' : agent_data[2],
                'password' : agent_data[3],
                'phone' : agent_data[4],
                'agent_img': agent_data[5]
            }
            image  = request.FILES['agent_image']
            with open("media/" + image.name, 'wb') as f:
            
                for chunk in image.chunks():
                    f.write(chunk)
            
            new_dict = {
                'agentname' : request.POST['agentname'],
                'email' : request.POST['email'],
                'address' : request.POST['address'],
                'password' : request.POST['password'],
                'phone' : request.POST['phone'],
                'agent_img':image.name
            }
            dict={}
            for keys in new_dict.keys():
                if len(new_dict[keys]) != 0:
                    dict[keys] = new_dict[keys]
                else:
                    dict[keys] = old_dict[keys]
            print(dict,old_dict,new_dict)


            # update_user = 'update website_user set agentname = %s, email= %s,address = %s,password =%s, user_img=%s where user_id = %s '
            update_agent = 'UPDATE website_employee AS emp JOIN website_agent AS agent ON emp.employee_id = agent.agent_id_id SET emp.name = %s, emp.email = %s, emp.address = %s, emp.password = %s, emp.phone = %s, agent.agent_img = %s WHERE emp.employee_id = %s'
            with connection.cursor() as cursor:
                cursor.execute(update_agent, (dict['agentname'],dict['email'], dict['address'],dict['password'],dict['phone'],dict['agent_img'],user))
                messages.success(request, "Profile Updated")
            return redirect('dashboard')

        return render(request, 'agent_edit_profile.html', {'user_id': user})




def property_edit_info(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
  
    if request.method == 'POST':
        property_id = request.POST['property_id']
    
        print(property_id)
        retrieve_property_info = "select name,location,size,type,price,property_img from website_property where property_id = %s"
        property_data = None
        with connection.cursor() as cursor:
            cursor.execute(retrieve_property_info, [property_id])
            property_data = tuple(cursor.fetchall())[0]
        print(property_data)
        old_dict = {
            'p_name' : property_data[0],
            
            'location' : property_data[1],
            'size' : property_data[2],
            'type' : property_data[3],
            'price' :property_data[4],
            'property_img': property_data[5]
        }
        image  = request.FILES['property_image']
        with open("media/" + image.name, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        print(old_dict)
        new_dict = {
            'p_name' : request.POST['p_name'],
            'location' : request.POST['location'],
            'size' : request.POST['size'],
            'type' : request.POST['type'],
            'price' : request.POST['price'],
            'property_img':image.name
        }
        print(new_dict)
        dict={}
        for keys in new_dict.keys():
            if len(new_dict[keys]) != 0:
                dict[keys] = new_dict[keys]
            else:
                dict[keys] = old_dict[keys]
        print(dict,old_dict,new_dict)
        update_property = 'update website_property set name =%s,location=%s,size=%s,type=%s,price=%s,property_img = %s where property_id = %s '
        with connection.cursor() as cursor:
            cursor.execute(update_property, (dict['p_name'], dict['location'],dict['size'],dict['type'],dict['price'],dict['property_img'],property_id))
            messages.success(request, "Property Info Updated")
        
    return render(request, 'property_edit_info.html', {'user_id': user,})



def auction(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        auction_id = ''
        property_data = ''
        user_status = ''
        auction_running_status = ''
        find_user_status = 'select auction_status from website_user where user_id=%s'
        find_auction = "select auction_id, auction_running from website_auction where auction_status='active'"
        find_property = """ 
                        select p.property_id, p.location, p.name, p.size, p.type, p.price
                        from website_auction as a
                        inner join website_auction_property as ap on a.auction_id = ap.auction_id_id
                        inner join website_property as p on ap.property_id_id = p.property_id
                        where a.auction_status = 'active' 
                        """
        with connection.cursor() as cursor:
            cursor.execute(find_auction)
            temp = tuple(cursor.fetchall())[0]
            auction_id = temp[0]
            auction_running_status = temp[1]
            print(auction_running_status,'---------------------')
            cursor.execute(find_property)
            property_data = tuple(cursor.fetchall())
            cursor.execute(find_user_status, [info[0]])
            user_status = tuple(cursor.fetchall())[0][0]
            dic = {
                'user_id':info[0], 
                'auct_id':auction_id,
                'data': property_data,
                'user_status' : user_status,
                'running_status': auction_running_status
                }
        return render(request, 'auction.html', dic )
    else:
        return render(request, 'auction.html')

def join_auction(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        if request.method=='POST':
            insert_pass = request.POST['confirm_password']
            retrieve_pass='select password from website_user where user_id=%s'
            add_auction_to_user = "update website_user set auction_status='joined' where user_id=%s"
            psw=''
            with connection.cursor() as cursor:
                cursor.execute(retrieve_pass, [info[0]])
                psw = tuple(cursor.fetchall())[0][0]
                if insert_pass==psw:
                    cursor.execute(add_auction_to_user, [info[0]])
                    messages.success(request, 'Succesfully joined Auction')
    return redirect('auction')

def leave_auction(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        if request.method=='POST':
            insert_pass = request.POST['confirm_password']
            retrieve_pass='select password from website_user where user_id=%s'
            remove_auction_from_user = "update website_user set auction_status='not_joined' where user_id=%s"
            psw=''
            with connection.cursor() as cursor:
                cursor.execute(retrieve_pass, [info[0]])
                psw = tuple(cursor.fetchall())[0][0]
                if insert_pass==psw:
                    cursor.execute(remove_auction_from_user, [info[0]])
                    messages.warning(request, 'Left Auction')
    return redirect('auction')
    
def auction_property_submission(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        if request.method=='POST':
            auct_id = request.POST['auc_id']
            property_list = ''
            find_property = 'select property_id, name from website_property where user_id_id=%s and property_id not in (select property_id_id from website_auction_property)'
            with connection.cursor() as cursor:
                cursor.execute(find_property,[info[0]])
                property_list = tuple(cursor.fetchall())
            print(property_list)
            dic = {
                'user_id':info[0],
                'auct_id':auct_id,
                'properties':property_list
                }
            return render(request, 'confirm_property.html', dic )
    else:
        return render(request, 'confirm_property.html')

def auction_property_removal(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        if request.method=='POST':
            property_list = ''
            find_property = 'select property_id_id from website_auction_property where owner_id_id=%s '
            with connection.cursor() as cursor:
                cursor.execute(find_property,[info[0]])
                property_list = tuple(cursor.fetchall())
            dic = {
                'user_id':info[0],
                'properties':property_list
                }
            return render(request, 'remove_auction_property.html', dic )
    else:
        return render(request, 'remove_auction_property.html')

def add_auction_property(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        if request.method=='POST':
            insert_prop = request.POST['prop_id']
            insert_starting_price = request.POST['starting_price']
            insert_pass = request.POST['confirm_password']
            auction_id = request.POST['auct_id']
            retrieve_pass='select password from website_user where user_id=%s'
            update_user = "update website_user set auction_status='joined'"
            insert_property = 'insert into website_auction_property (auction_id_id, owner_id_id, property_id_id, starting_price,selling_price,number_of_bids,increment) values (%s, %s,%s,%s,%s, %s, %s)'
            psw=''
            user=''
            with connection.cursor() as cursor:
                cursor.execute(retrieve_pass, [info[0]])
                psw = tuple(cursor.fetchall())[0][0]
                if insert_pass==psw:
                    cursor.execute(insert_property, (auction_id, info[0], insert_prop, insert_starting_price,'0','0','0'))
                    messages.success(request, 'Property Added to Auction')
    return redirect('auction')


def remove_auction_property(request):
    info = sessionInfo()
    login_info = info[1]
    user = info[0]
    if info[1]=="True":
        if request.method=='POST':
            delete_prop = request.POST['prop_id']
            insert_pass = request.POST['confirm_password']
            retrieve_pass='select password from website_user where user_id=%s'
            update_user = "update website_user set auction_status='joined'"
            delete_property = 'delete from website_auction_property where property_id_id = %s'
            psw=''
            user=''
            with connection.cursor() as cursor:
                cursor.execute(retrieve_pass, [info[0]])
                psw = tuple(cursor.fetchall())[0][0]
                if insert_pass==psw:
                    cursor.execute(delete_property, [delete_prop])
                    messages.error(request, 'Property Removed from Auction')
    return redirect('auction')


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
# for every button function insert this code snippet at the very beginning
# --------------------

    # info = sessionInfo()
    # if '0000' in info[0]:
    #     return redirect('login')

def countdown(request):
    return render(request, 'countdown.html')