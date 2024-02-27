from .models import Property,Category
from rest_framework import serializers
from user.serializers import UserSerializer


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'name']

class PropertySerializer(serializers.ModelSerializer):
    user=UserSerializer(many=False,read_only=True)
    category=CategorySerializers(many=True,read_only=True)
 
    class Meta:
        model = Property
        fields = ['id','type','user','thumbnail','photo1','photo2','photo3','photo4','category','address', 'latitude', 'longitude','price','meterage','bedrooms','bathrooms','garage']
    
    def validate(self, data):
        # Custom validation logic for the entire serializer
        type=data.get('bedrooms')
        if type=='z':
            unrelated_fields=['bedrooms', 'bathrooms', 'garage']
            for field in unrelated_fields:
                if data.get(field):
                    print("field",data.get(field))
                    serializers.ValidationError("شما از فیلد هایی استفاده کردید که  مختص زمین نیست ") 
        return data


class CategoryViewsetSerializers(serializers.ModelSerializer):
    properties_category=PropertySerializer(many=True,read_only=True)
    class Meta:
        model=Category
        fields=['id', 'name','properties_category']