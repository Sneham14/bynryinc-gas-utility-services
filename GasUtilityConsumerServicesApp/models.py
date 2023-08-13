from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



# Create your models here.

STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed')
    ]
class CustomerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=120, unique=True)
    requests=models.OneToOneField('ServiceRequestModel',on_delete=models.CASCADE, null=True, default=None, blank=True)
    contact=models.CharField(max_length=20, unique=True, null=True)
    full_name = models.CharField(max_length=150, null=True)  

    def __str__(self):
        return self.full_name or self.username
    

class ServiceRequestModel(models.Model):
    
    request_type = models.CharField(max_length=120)
    request_details = models.TextField()
    request_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    requested_on = models.DateTimeField(auto_now_add=True)
    resolved_on= models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey('CustomerModel', on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"{self.request_type} - {self.customer}"
    
    def save(self, *args, **kwargs):
        if self.request_status == 'Resolved' and not self.resolved_on:
            self.resolved_on = timezone.now()  # Import timezone if not already imported
        super().save(*args, **kwargs)



