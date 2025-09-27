from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
import uuid
import os
from ..validators import *

def member_image(instance, filename):
    # Generate a unique filename using UUID
    ext = filename.split('.')[-1]
    return f"Members_Images/{instance.username}-{instance.id}.{ext}"

class Member(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,verbose_name="Member ID")
    username = models.CharField(max_length=50,validators=[validate_name],verbose_name="Member Name")
    email = models.EmailField(unique=True,verbose_name="Member Email")
    birth_date = models.DateField(verbose_name="Member Birth Date",null=True,blank=True)
    personal_img = models.ImageField(upload_to=member_image,verbose_name="Member Image",validators=[validate_image_mime],blank=True,null= True)
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Member Creation")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Member Update")
    password = models.CharField(max_length=255,verbose_name="Member Password")
   
    USERNAME_FIELD='email' 
    REQUIRED_FIELDS = ['username']
    @property
    def age(self):
        today = date.today()
        currentage = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            currentage -= 1
        return currentage
    
    
    def delete(self,*args,**kwargs):
        if self.personal_img and os.path.isfile(self.personal_img.path):
            os.remove(self.personal_img.path)
        super().delete(*args,**kwargs)