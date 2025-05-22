from django.db import models
from PIL import Image
from django.contrib.auth.models import User




# Create your models here
class Vendor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)   #connects with django's user model
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

class TourStatus(models.Model):
    
    status=models.CharField(max_length=100,unique=True,choices=[('draft','Draft'),('submitted','Submitted'),('pending approval','Pending Approval'),('rejected','Rejected'),('approved','Approved')],default='submitted')
    

    def __str__(self):
        return self.status
    
class TourPackages(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=1200,blank=False,null=False,default="")
    price=models.CharField(max_length=500)
    location=models.CharField(max_length=50)
    available_from=models.DateField()
    available_to=models.DateField()
    duration_days=models.IntegerField(editable=False)
    duration_text=models.CharField(max_length=50,editable=False)
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='package_images/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    expiry_date=models.DateField(null=True,blank=True)
    status=models.ForeignKey(TourStatus,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img = img.resize((800, 800))  # Resize to 800x800 pixels
        img.save(self.image.path)
    
    class Meta:
        unique_together=('vendor','title')

    
    def __str__(self):
        return self.title
    
    def save_expire(self,*args,**kwargs):
        if not self.expiry_date:
            self.expiry_date=self.available_to
        super().save(*args,**kwargs)
    
    def save(self,*args,**kwargs):
        if self.available_from and self.available_to:
            days=(self.available_to-self.available_from).days
            nights=days-1 if days>0 else 0
            self.duration_days=days
            self.duration_text= f"{days} day{'s' if days !=1 else ''} {nights} night{'s' if nights !=1 else ''}"
        super().save(*args,**kwargs)
        

class Booking(models.Model):
    package = models.ForeignKey(TourPackages, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)
    no_of_people = models.PositiveIntegerField(null=False,blank=False)
    phone_number = models.CharField(max_length=15,default='please provide')
    address = models.TextField(default='please fill')
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        
    ],
    default='pending'

    )
    
    def __str__(self):
        return f"Booking by {self.customer.username} for {self.package.title}"


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username



   
