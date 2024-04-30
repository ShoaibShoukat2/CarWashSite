from django.db import models

# Create your models here.

class Signup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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



