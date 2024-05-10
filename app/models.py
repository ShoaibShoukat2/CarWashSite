from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Signup(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='user_images/', default='default.jpg')  # Image field
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, default='')
    password = models.CharField(max_length=100, default='')
    vehicle_brand = models.CharField(max_length=50, default='')
    vehicle_model = models.CharField(max_length=50, default='')
    vehicle_type = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    name = models.CharField(max_length=300,default='')
    file = models.FileField(upload_to='vehicle_images/',default='')


    def __str__(self):
        return self.name

class SubscrationDuration(models.Model):
    vehicle_id = models.ForeignKey(Vehicle,on_delete=models.CASCADE,default='')
    subscription_name = models.CharField(max_length=200,default='')


    def __str__(self):
        return f"{self.vehicle_id.name} - {self.subscription_name}"


class Packages(models.Model):
    vehicle_id = models.ForeignKey(Vehicle,on_delete=models.CASCADE,default='')
    subscription_id = models.ForeignKey(SubscrationDuration,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=100,default='')



    def __str__(self):
        return f"{self.vehicle_id.name} - {self.subscription_id.subscription_name} - {self.name}"


class DescriptionPrice(models.Model):
    vehicle_id = models.ForeignKey(Vehicle,on_delete=models.CASCADE,default='')
    subscription_id = models.ForeignKey(SubscrationDuration,on_delete=models.CASCADE,default='')
    package_id = models.ForeignKey(Packages,on_delete=models.CASCADE,default='')
    description = models.TextField(default='')
    price = models.FloatField(default=0.0)



    def __str__(self):
        return f"{self.vehicle_id.name} - {self.subscription_id.subscription_name} - {self.package_id.name}"




class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

class Category(models.Model):
    admin = models.ForeignKey(Admin,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default='')



    def __str__(self):
        return self.name


class Blog(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)    
    title = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='')



    def __str__(self):
            return self.title



class Comments(models.Model):
    blog_id = models.ForeignKey(Blog,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=255,default='')
    comments = models.TextField(max_length=500,default='')



    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user_id = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    subscription = models.CharField(max_length=100, null=True, blank=True)
    package = models.CharField(max_length=100, null=True, blank=True)
    vehicle = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.user_name 


class AppoitmentSchedule(models.Model):
    user_id = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100)
    date = models.DateField()


    def __str__(self):

        return f"Appointment at {self.location} on {self.date}"




