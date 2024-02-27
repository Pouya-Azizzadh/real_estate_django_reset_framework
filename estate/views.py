from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PropertySerializer,CategoryViewsetSerializers
from .models import Property,Category
from django.core.exceptions import ValidationError
from rest_framework import status
from user.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter


class PropertyRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        property=Property.objects.all()
        serializer=PropertySerializer(property,many=True)
        return Response(data=serializer.data)
    
    def post(self, request):
        property=Property.objects.all()
        serializer=PropertySerializer(property,many=False)
        type =request.data.get('type')
        thumbnail =request.data.get('thumbnail')
        photo1 =request.data.get('photo1')
        photo2 =request.data.get('photo2')
        photo3 =request.data.get('photo3')
        photo4 =request.data.get('photo4')
        category=request.data.get('category')
        user =CustomUser.objects.get(id=request.user.id)
        address =request.data.get('address')
        price=request.data.get('price')
        meterage=request.data.get('meterage')
        latitude =request.data.get('latitude')
        longitude =request.data.get('longitude')
        bedrooms =request.data.get('bedrooms')
        bathrooms =request.data.get('bathrooms')
        garage =request.data.get('garage')
        if type =='z'and (bedrooms or bathrooms or garage):
            return Response({'message':"شما از فیلد هایی استفاده کردید که  مختص زمین نیست "},status=status.HTTP_400_BAD_REQUEST) 
        
            
        else:
            property=Property(type=type,thumbnail=thumbnail,photo1=photo1,photo2=photo2,photo3=photo3,photo4=photo4,category=category,user=user,address=address,price=price,meterage=meterage,latitude=latitude,longitude=longitude,bedrooms=bedrooms,bathrooms=bathrooms,garage=garage)
            property.save()
            return Response(data=serializer.data)
               
    def delete(self, request,pk):
         property=Property.objects.get(id=pk)
         serializer=PropertySerializer(property,many=False)
         property.delete()
         return Response(data=serializer.data)
    
class PropertyGetView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset=Property.objects.all()
  
    def get_queryset(self):
        queryset = Property.objects.all()
        for field in self.request.query_params:
            if field=='latitude' or field=='longitude' or field=='photo1' or field=='photo2' or field=='photo3' or field=='photo4' or field=='thumbnail':
                del field
            
            value = self.request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})
            
        return queryset

    
class PropertyAddressSearchView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset=Property.objects.all()
    search_fields = ['address']
    filter_backends = (SearchFilter,)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryViewsetSerializers
    queryset=Category.objects.all()
   