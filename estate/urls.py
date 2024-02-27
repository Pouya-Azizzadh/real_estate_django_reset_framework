from django.urls import path
from . import views
from rest_framework import routers
#CategoryViewSet\
router=routers.DefaultRouter()
router.register('category',views.CategoryViewSet,basename='category')
urlpatterns = [
path('property', views.PropertyRegistrationView.as_view()),
path('properteis', views.PropertyGetView.as_view()),
path('search/address', views.PropertyAddressSearchView.as_view())

]+router.urls

