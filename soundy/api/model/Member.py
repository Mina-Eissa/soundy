from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
import uuid
import re
from django.core.exceptions import ValidationError

def validate_name(value):
    pattern = r'^[A-Za-z0-9_-]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            "Name can only contain letters, numbers, underscores (_), and hyphens (-)."
        )

def member_image(instance, filename):
    # Generate a unique filename using UUID
    ext = filename.split('.')[-1]
    return f"Members_Images/{instance.username}-{instance.id}.{ext}"

class Member(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,verbose_name="Member ID")
    username = models.CharField(max_length=50,validators=[validate_name],verbose_name="Member Name")
    email = models.EmailField(unique=True,verbose_name="Member Email")
    birth_date = models.DateField(verbose_name="Member Birth Date",null=True,blank=True)
    personal_img = models.ImageField(upload_to=member_image,verbose_name="Member Image",blank=True,null= True)
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