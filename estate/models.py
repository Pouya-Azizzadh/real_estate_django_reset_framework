from django.db import models
from user.models import CustomUser

from django.core.exceptions import ValidationError

 

class Category(models.Model):
       name=models.CharField(max_length=50,default='')

       def __str__(self) -> str:
              return self.name

class Property(models.Model):
       TYPE_ESTATE_LIST=(('z','زمین'),('m','مسکونی'),('t','تجاری'))
       thumbnail = models.ImageField(null=True,blank=True,upload_to='images/')
       photo1 = models.ImageField(null=True,blank=True,upload_to='images/')
       photo2 = models.ImageField(null=True,blank=True,upload_to='images/')
       photo3 = models.ImageField(null=True,blank=True,upload_to='images/')
       photo4 = models.ImageField(null=True,blank=True,upload_to='images/')
       type = models.CharField(choices=TYPE_ESTATE_LIST,default="z",max_length=20)
       category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='properties_category',blank=True, null=True)
       user = models.ForeignKey(CustomUser,related_name='properties_user',on_delete=models.CASCADE,blank=True, null=True)
       address = models.CharField(max_length=255,default="ادرس را وارد کنید")
       price=models.IntegerField(null=True)
       meterage=models.IntegerField(null=True)
       latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
       longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
       bedrooms = models.IntegerField(blank=True, null=True)
       bathrooms = models.IntegerField(blank=True, null=True)
       garage = models.BooleanField(default=False, null=True)
       # Other fields related to residential property

       def clean(self):
              if type =='z' and self.bedrooms or self.bathrooms or self.garage:
                     raise ValidationError("شما از فیلد هایی استفاده کردید که  مختص زمین نیست ") 