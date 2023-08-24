from django.db import models
# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=12, primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    user_img = models.CharField(max_length=50, default=None)
    auction_status = models.CharField(max_length=15, default=None)


class Employee(models.Model):
    employee_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    supervisor = models.BooleanField(default=0)

class Agent(models.Model):
    agent_id = models.ForeignKey(Employee, on_delete = models.CASCADE, to_field= 'employee_id', primary_key = True)

    supervisor_id = models.CharField(max_length=50)
    agent_img = models.CharField(max_length=50, default=None)



#zabir


class Property(models.Model):
    property_id = models.CharField(max_length = 20, primary_key = True)

    user_id = models.ForeignKey(User, on_delete = models.CASCADE, to_field = 'user_id')
    agent_id = models.ForeignKey(Agent, on_delete = models.CASCADE, to_field = 'agent_id')

    status = models.CharField(max_length = 20)
    location = models.CharField(max_length = 50)
    name = models.CharField(max_length = 20)
    size = models.CharField(max_length=10)
    type = models.CharField(max_length =20)
    price = models.CharField(max_length=15)
    property_img = models.CharField(max_length=50, default=None)

class Auction(models.Model):
    auction_id = models.CharField(max_length = 20, primary_key = True)
    auction_status = models.CharField(max_length=50, default='Inactive')
    auction_running = models.BooleanField()
    
    

class Auction_Property(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE, to_field='auction_id', db_index=True)
    property_id = models.ForeignKey(Property, on_delete = models.CASCADE, to_field = 'property_id', primary_key=True)
    starting_price = models.CharField(max_length=15)
    increment = models.CharField(max_length = 10,default='0')
    selling_price = models.CharField(max_length=15,default='0')
    number_of_bids = models.CharField(max_length=15,default='0')
    
    class Meta:
        unique_together=("auction_id","property_id")

class Admin(models.Model):
    admin_id = models.CharField(max_length = 20, primary_key = True)

    name = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    branch = models.CharField(max_length = 20)

class Buyer(models.Model):
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id', primary_key = True) 

class Buys_From(models.Model):
    buyer_id = models.ForeignKey(Buyer, on_delete = models.CASCADE, to_field = 'buyer_id')
    agent_id = models.ForeignKey(Agent, on_delete = models.CASCADE, to_field = 'agent_id')
    
    commission = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        unique_together = ('buyer_id', 'agent_id')
        

class Bids_In(models.Model):
    buyer_id = models.ForeignKey(Buyer, on_delete = models.CASCADE, to_field = 'buyer_id')
    auction_id = models.ForeignKey(Auction, on_delete = models.CASCADE, to_field = 'auction_id')

    class Meta:
        unique_together = ('buyer_id', 'auction_id')

class Support(models.Model):
    support_id= models.ForeignKey(Employee, on_delete = models.CASCADE, to_field = 'employee_id',default='support_01',primary_key=True)
    type=models.CharField(max_length=20)
    hiring_price=models.CharField(max_length=10, default = 1000)

class Maintains(models.Model):
    property_id = models.ForeignKey(Property, on_delete = models.CASCADE, to_field = 'property_id')
    support_id = models.ForeignKey(Support, on_delete = models.CASCADE, to_field = 'support_id')
    
    class Meta:
        unique_together = ('property_id', 'support_id')
        

class Property_Features(models.Model):
    property_id = models.ForeignKey(Property, on_delete = models.CASCADE, to_field = 'property_id')
    features=models.CharField(max_length=20)
   
    class Meta:
        unique_together= ("property_id","features")


class Organizes(models.Model):
    admin_id = models.ForeignKey(Admin, on_delete = models.CASCADE, to_field = 'admin_id')
    auction_id = models.ForeignKey(Auction, on_delete = models.CASCADE, to_field = 'auction_id')

    class Meta:
        unique_together=("admin_id","auction_id")


class Agents_Clients(models.Model):
    

    agent_id = models.ForeignKey(Agent, on_delete = models.CASCADE, to_field = 'agent_id')
    client=models.CharField(max_length=20)

    class Meta:
        unique_together=("agent_id","client")


class Hires(models.Model):
    user_id=models.ForeignKey(User, on_delete = models.CASCADE, to_field = 'user_id', db_index=True)
    support_id=models.ForeignKey(Employee, on_delete = models.CASCADE, to_field = 'employee_id', primary_key = True)

    class Meta:
        unique_together=("support_id","user_id")



class Seller(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id', null=True) 
    agent_id = models.ForeignKey(Agent, on_delete=models.CASCADE, to_field='agent_id', null=True) 

    hiring_price = models.CharField(max_length=50)

    class Meta:
        unique_together = ('seller_id','agent_id')


class Dependent(models.Model):
    agent_id = models.ForeignKey(Agent, on_delete=models.CASCADE, to_field='agent_id', primary_key = True) 
    
    name = models.CharField(max_length=50)
    relation = models.CharField(max_length=50)

class Session(models.Model):
    user = models.CharField(max_length = 12, primary_key=True)
    login = models.CharField(max_length = 5)

